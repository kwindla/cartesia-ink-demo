#
# Copyright (c) 2025, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import json
import os
import random
import sys
import time

from dotenv import load_dotenv
from loguru import logger
from typing import Dict

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.serializers.twilio import TwilioFrameSerializer
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.cartesia.stt import CartesiaSTTService
from pipecat.services.google.llm import GoogleLLMService
from pipecat.transports.network.fastapi_websocket import (
    FastAPIWebsocketParams,
    FastAPIWebsocketTransport,
)
from pipecat.transports.network.small_webrtc import SmallWebRTCTransport
from pipecat.transports.base_transport import BaseTransport, TransportParams
from pipecat.transports.services.daily import DailyParams, DailyTransport
from pipecatcloud.agent import (
    DailySessionArguments,
    SessionArguments,
    WebSocketSessionArguments,
)
from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import RedirectResponse
from pipecat_ai_small_webrtc_prebuilt.frontend import SmallWebRTCPrebuiltUI
from pipecat.transports.network.webrtc_connection import SmallWebRTCConnection

import uvicorn

from image_utils import png_file_to_data_url

load_dotenv(override=True)
logger.remove()
logger.add(sys.stderr, level="DEBUG")


with open("llms-txt/ink-blog-post.md", "r") as f:
    ink_blog_post = f.read()


async def main(transport: BaseTransport):
    session_id = f"{int(time.time())}-{random.randint(0, 1000)}"
    logger.info(f"Starting conversation with session ID: {session_id}")

    #
    # Set up services: Cartesia for STT and TTS, Google Gemini 2.0 Flash for the LLM
    #

    stt = CartesiaSTTService(api_key=os.getenv("CARTESIA_API_KEY"))

    llm = GoogleLLMService(api_key=os.getenv("GOOGLE_API_KEY"), model="gemini-2.0-flash")

    tts = CartesiaTTSService(
        api_key=os.getenv("CARTESIA_API_KEY"),
        voice_id="71a7ad14-091c-4e8e-a314-022ece01c121",  # British Reading Lady
    )

    #
    # Initialize the conversation system instruction and core context. We pass
    # the blog post about Ink as background context, along with the two tables
    # showing Ink's performance metrics (from the blog post). We pass the tables
    # as images.
    #

    context = OpenAILLMContext(
        [
            {
                "role": "system",
                "content": f"""You are a helpful and friendly AI participating in a voice conversation.
                
Because you are participating in a voice conversation, do not use any formatting or emojis in your responses. Use only plain text. Keep your responses concise, short, and to the point
unless specifically asked to elaborate on a topic.

You can speak multiple languages. Accept input in any language, and output in whatever language the user requests. Start in English.

Your job is to answer questions about the Cartesia Ink speech-to-text model. 

Here is a detailed technical blog post about the Cartesia Ink speech-to-text model.

----

{ink_blog_post}
""",
            },
            {
                "role": "user",
                "content": [
                    # pull in the llms-txt/time-to-completion-table.png file as base64 data URL
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": png_file_to_data_url("llms-txt/time-to-completion-table.png")
                        },
                    },
                    # pull in the llms-txt/word-error-rate-table.png file as base64 data URL
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": png_file_to_data_url("llms-txt/word-error-rate-table.png")
                        },
                    },
                    {
                        "type": "text",
                        "text": "Here are two tables providing statistics about the Cartesia Ink speech-to-text model. Wait for further questions.",
                    },
                ],
            },
        ],
    )

    context_aggregator = llm.create_context_aggregator(context)

    #
    # Set up the pipeline; start it when a client connects.
    #

    pipeline = Pipeline(
        [
            transport.input(),
            stt,
            context_aggregator.user(),
            llm,
            tts,
            context_aggregator.assistant(),
            transport.output(),
        ]
    )

    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            allow_interruptions=True,
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
        conversation_id=session_id,
    )

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info(f"Client connected: {client}")
        # Kick off the conversation
        await task.queue_frames([context_aggregator.user().get_context_frame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info(f"Client disconnected: {client}")
        await task.cancel()

    runner = PipelineRunner(handle_sigint=False, force_gc=True)

    await runner.run(task)


#
# ---- Functions to run the bot. ----
#
# In a production application the logic here could be separated
# out into utility modules.
#


# Run the bot in the cloud. Pipecat Cloud or your hosting infrastructure calls this
# function with either Twilio or Daily session arguments.
async def bot(args: SessionArguments):
    try:
        if isinstance(args, WebSocketSessionArguments):
            logger.info("Starting WebSocket bot")

            start_data = args.websocket.iter_text()
            await start_data.__anext__()
            call_data = json.loads(await start_data.__anext__())
            stream_sid = call_data["start"]["streamSid"]
            transport = FastAPIWebsocketTransport(
                websocket=args.websocket,
                params=FastAPIWebsocketParams(
                    audio_in_enabled=True,
                    audio_out_enabled=True,
                    add_wav_header=False,
                    vad_analyzer=SileroVADAnalyzer(),
                    serializer=TwilioFrameSerializer(stream_sid),
                ),
            )
        elif isinstance(args, DailySessionArguments):
            logger.info("Starting Daily bot")
            transport = DailyTransport(
                args.room_url,
                args.token,
                "Respond bot",
                DailyParams(
                    audio_in_enabled=True,
                    audio_out_enabled=True,
                    transcription_enabled=False,
                    vad_analyzer=SileroVADAnalyzer(),
                ),
            )

        await main(transport)
        logger.info("Bot process completed")
    except Exception as e:
        logger.exception(f"Error in bot process: {str(e)}")
        raise


# Run the bot locally. This is useful for testing and development.
def local():
    try:
        app = FastAPI()

        # Store connections by pc_id
        pcs_map: Dict[str, SmallWebRTCConnection] = {}

        ice_servers = ["stun:stun.l.google.com:19302"]
        app.mount("/client", SmallWebRTCPrebuiltUI)

        @app.get("/", include_in_schema=False)
        async def root_redirect():
            return RedirectResponse(url="/client/")

        @app.post("/api/offer")
        async def offer(request: dict, background_tasks: BackgroundTasks):
            pc_id = request.get("pc_id")

            if pc_id and pc_id in pcs_map:
                pipecat_connection = pcs_map[pc_id]
                logger.info(f"Reusing existing connection for pc_id: {pc_id}")
                await pipecat_connection.renegotiate(
                    sdp=request["sdp"],
                    type=request["type"],
                    restart_pc=request.get("restart_pc", False),
                )
            else:
                pipecat_connection = SmallWebRTCConnection(ice_servers)
                await pipecat_connection.initialize(sdp=request["sdp"], type=request["type"])

                @pipecat_connection.event_handler("closed")
                async def handle_disconnected(
                    webrtc_connection: SmallWebRTCConnection,
                ):
                    logger.info(f"Discarding peer connection for pc_id: {webrtc_connection.pc_id}")
                    pcs_map.pop(webrtc_connection.pc_id, None)

                transport = SmallWebRTCTransport(
                    webrtc_connection=pipecat_connection,
                    params=TransportParams(
                        audio_in_enabled=True,
                        audio_out_enabled=True,
                        vad_enabled=True,
                        vad_analyzer=SileroVADAnalyzer(),
                        vad_audio_passthrough=True,
                    ),
                )
                background_tasks.add_task(main, transport)

            answer = pipecat_connection.get_answer()
            # Updating the peer connection inside the map
            pcs_map[answer["pc_id"]] = pipecat_connection

            return answer

        uvicorn.run(app, host="0.0.0.0", port=7860)

    except Exception as e:
        logger.exception(f"Error in local bot process: {str(e)}")
        raise


if __name__ == "__main__":
    local()

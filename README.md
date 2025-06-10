# Talk to Cartesia Ink STT about Cartesia Ink STT

This is a demo of Cartesia Ink STT. Ink is a streaming speech-to-text service optimized for conversational voice AI applications.

Detailed technical information about Ink is available in the launch blog post and the API reference docs:

  - [Launch blog post](https://cartesia.ai/blog/introducing-ink-speech-to-text)
  - [API reference docs](https://docs.cartesia.ai/2025-04-16/api-reference/stt/stt)

You can go read the blog post, or, with [Pipecat](https://pipecat.ai/)'s help, you can just talk to Ink about Ink.!

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This bot uses Cartesia for text-to-speech and speech-to-text, and Google Gemini 2.0 Flash for the LLM.

Copy `env.example` to `.env`, then add your Cartesia and Google API keys to `.env`.

```bash
CARTESIA_API_KEY=...
GOOGLE_API_KEY=...
```

## Run

```bash
python bot.py
```

## Interact

Open http://localhost:7860 in your browser and start a conversation about Ink.

## Notes

The code in bot.py is short and heavily commented.

Note that Gemini 2.0 Flash is happy to take both text and images as input, so we set up the conversation context by passing in the blog post about Ink as text, and the two tables showing Ink's performance metrics as images.

When you run this bot on your dev machine and connect to it via `localhost:7860`, the web browser client sets up a local, peer-to-peer WebRTC connection to the bot.

You can also deploy this bot to Pipecat Cloud and access it via cloud WebRTC or wire it up directly to a Twilio phone number using the Twilio MediaStream WebSocket transport. See the [Pipecat Cloud docs](https://docs.pipecat.daily.co/introduction) for more information.

# Introducing Ink: speech-to-text models for real-time conversation

Today we’re introducing Ink, a new family of streaming speech-to-text (STT) models for developers building real-time voice applications. Our debut model is Ink-Whisper, a variant of OpenAI’s Whisper, specifically optimized for low-latency transcription in conversational settings. Available today, Ink-Whisper is the fastest, most affordable STT model–designed for enterprise-grade voice agents.

## Sonic to Ink: from voice-out to voice-in

With Sonic, we've become the preferred text-to-speech (TTS) provider for builders who prioritize speed, quality, and reliability. This comes as no surprise, given Sonic's market leadership in ultra-low latency, enabling customers to create the most realistic interactive voice experiences. Now, we’re turning our attention to the other side of the conversation (STT) with Ink.

## Reimagining Whisper for real-time

For our STT release, we looked at what developers are already using and what might be broken. That led us to OpenAI’s whisper-large-v3-turbo. It is widely used for good reasons–Whisper performs comparably in conversational transcription accuracy to other proprietary speech-to-text providers, it is open source, and can be inferenced efficiently. 

Most of the innovation around Whisper has focused on improving throughput, which is how quickly we can transcribe huge datasets (measured by real-time factor, or RTF). That’s great for post-processing long audio files, but standard Whisper falls short on speed and accuracy when it comes to powering real-time voice agents where transcription quality needs to be high on every call, not just in aggregate. Plus, standard Whisper wasn’t designed for challenging real-world conditions. 

Ultimately, Whisper was fundamentally made for bulk processing, not live dialogue. So, we rearchitected it into Ink-Whisper, purpose-building it for real-time voice AI, with speed and real-world context at its core.

## Ink-Whisper is built for real-world conversations 

In enterprise use cases, voice AI agents need to transcribe speech as it happens–and do it reliably across a wide range of variable real-world environments. We built Ink-Whisper with those challenges in mind, focusing on accuracy in the types of conditions that typically trip up standard speech-to-text systems:

 - Telephony artifacts: Low-bandwidth, compressed audio adds distortion
 - Proper nouns and domain terms: Names of products, drugs, or financial instruments require clarity
 - Background noise: Traffic, restaurant chatter, crying babies, and static make clean transcription difficult
 - Disfluencies and silence: Fillers like "um" and pauses confuse standard Whisper implementation
 - Accents and variation: Voices come in all kinds, and STT models need to adapt

One of our core improvements on standard Whisper is dynamic chunking. Standard Whisper performs best on full 30-second chunks. But conversational AI deals in much smaller, more fragmented audio segments. We've modified Whisper to handle variable-length chunks that end at semantically meaningful points. That means fewer errors and less hallucination, especially during silence or audio gaps.

To ensure the Ink-Whisper actually works better in the wild, we created a suite of evaluation datasets that reflect those common challenges in voice AI:

 - Background Noise Dataset: Conversations recorded in noisy environments like traffic, cafes, or offices
 - Proper Noun Dataset: 100 samples from SPGISpeech with dense financial terms and brand names
 - Speech Accent Dataset: Transcripts featuring a range of English accents, to test robustness across demographics

Across these datasets, Ink-Whisper outperforms baseline whisper-large-v3-turbo in accuracy based on word error rate (WER). The WER for Ink-Whisper is also competitive with other streaming speech-to-text models–and critically, it’s optimized for production-grade, real-time performance: 

[ Table: Word Error Rate ]

## Ink-Whisper is the fastest streaming model

Beyond accuracy, streaming transcription must deliver ultra-speed to achieve realistic conversation. With Ink-Whisper, we emphasize a new metric: time-to-complete-transcript (TTCT). This is how quickly the full transcript is ready once the user stops talking. TTCT determines how fast the entire system can respond, in a way that mimics a live, attentive listener. 

A dead giveaway of an unnatural bot is the lag in its reply. Those lags break the rhythm of natural conversation. They lead to dropped calls, frustrated users, and lost revenue. Having the absolute lowest TTCT is about speed, yes, and ultimately, it’s about making the interaction feel human.

We’re proud to share that Ink-Whisper outperforms the baseline whisper-large-v3-turbo on TTCT. In fact, Ink-Whisper delivers the fastest TTCT of any streaming speech-to-text model we’ve tested:  

[ Table: Time to Complete Transcription ]

Standard Whisper remains one of the most versatile open STT models, but it wasn’t made for real-time.  Ink-Whisper changes that with optimizations for conversational accuracy and ultra-low latency. Ink-Whisper delivers the fastest TTCT we’ve seen, with strong performance across noisy, accented, and dynamic speech. We evaluated Ink-Whisper in the real-world conditions one encounters with voice agents–not the controlled environment of a lab or studio.

## Ink-Whisper is the most affordable streaming model

Voice is the future–and we’re committed to this belief by making Ink-Whisper accessible to builders of voice solutions. Ink-Whisper is both the fastest and most affordable streaming STT model available. At just 1 credit per second (or $0.13/hr on our Scale plan), Ink-Whisper delivers top-tier real-time transcription at the lowest price. 

Getting started with Ink-Whisper is as seamless as the experiences it powers: 

- Ink-Whisper easily integrates with Vapi, Pipecat, and LiveKit, so you can start streaming voice interactions in minutes
- With 99.9% uptime and enterprise-grade compliance (SOC 2 Type II, HIPAA, PCI), you can deploy at scale with confidence

Start here: https://cartesia.ai/pricing
Or explore the docs: https://docs.cartesia.ai/2025-04-16/api-reference/stt/stt

## The future of voice AI with Cartesia

We’re seeing surging demand for voice agents. The most effective ones rely on state-of-the-art audio AI like our Sonic text-to-speech model. Now with Ink-Whisper, we’re meeting that demand on the other side, enabling fast, natural conversations. Today’s release is an early glimpse into how we’re reimagining the real-time voice stack. More to come.
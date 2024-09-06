---
title: "Talk Summary: Building Reliable Voice Agents with Open Source Tools"
date: 2024-09-13
author: "ZanSara"
featuredImage: "/posts/2024-09-13-odsc-europe-voice-agents-talk-summary/cover.png"
draft: true
---

*This is a summary of my recent talk at ODSC Europe 2024.*

---

In the last few years, the world of voice agents saw dramatic leaps forward in the state of the art of all its most basic components. Thanks mostly to OpenAI, bots are now able to understand human speech almost like a human would, they're able to speak back with completely naturally sounding voices, and are able to hold a free conversation that feels extremely natural.

But building voice bots is far from a solved problem. These improved capabilities are raising the quality bar, and even users accustomed to the simpler capabilities of old bots now expect a whole new level of quality when it comes to interacting with them.

In this post we're going to discuss how building a voice agent today looks like, from the very basics up to advanced prompting strategies to keep your LLM-based bots under control, and we're also going to see how to build such bots in practice from the ground up using a newly released library, Pipecat.

# Outline

- [What is a voice agent?](#what-is-a-voice-agent)
- New challenges
- Let's build a voice bot
- Looking forward


# What is a voice agent?

As the name says, voice agents are programs that are able to carry on a task and/or take actions and decisions on behalf of a user ("software agents") by using voice as their primary mean of communication (as poopsed to the much more common text chat format). Voice agents are inherently harder to build than their text based counterparts: computers operate primarily with text, and the art of making machines understand human voices has been an elusive problem for decades.

The basic architecture of a voice agent can be decomposed into three main fundamental building blocks:

- a **speech-to-text (STT)** component, tasked to translate an audio stream into readable text,
- the **bot's logic engine**, which works entirely with text only,
- a **text-to-speech (TTS)** component, which converts the bot's text responses back into an audio stream of synthetic speech.

![](/posts/2024-09-13-odsc-europe-voice-agents-talk-summary/structure-of-a-voice-bot.png)

## Speech to text (STT)

Speech-to-text software is able to convert the audio stream of a person saying something and produce a transcription of what the voice said. Speech-to-text engines have a long history, but their limitations have always been quite severe: they used to require fine-tuning on each individual speaker, have a rather high word error rate (WER) and they mainly worked strictly with native speakers of major languages, failing hard on foreign and uncommon accents and native speakers of less mainstream languages.

With the [first release of OpenAI's Whisper models](https://openai.com/index/whisper/) in late 2022, the state of the art improved dramatically. Whisper enabled transcription (and even direct translation) of speech from many languages with an impressively low WER, finally comparable to the performance of a human, all with relatively low resources, higher then realtime speed, and no finetuning required. Not only, but the model was free to use, as OpenAI open-sourced it.

Since then, speech-to-text models kept improving at a steady pace. Nowadays the Whisper's family of models sees some competition for the title of best STT model from the offering of companies such as [Deepgram](https://deepgram.com/), but it's still one of the best options in terms of open-source models.

## Text-to-speech (TTS)

Text-to-speech model perform the exact opposite task than speech-to-text models: their goal is to convert written text into an audio stream of synthetic speech. Text-to-speech has historically been an easier feat than speech-to-text, but it also saw drastic improvements in the quality of the synthetic voices, to the point that it could nearly be considered a solved problem in its most basic form.

Today many companies (such as OpenAI, [Cartesia](https://cartesia.ai/sonic), [ElevenLabs](https://elevenlabs.io/), Azure and many others) offer TTS software with voices that sound indistinguishable to a human nearly all the time. They also have the capability to clone a specific human voice with remarkably little training data (just a few seconds of speech) and to tune accents, inflections, even emotion and tone.

TTS is also improving by the day, but due to the incredibly high quality of the output competition now tends to focus on price and performance.

## Bot's logic











<p class="fleuron"><a href="https://www.zansara.dev/posts/2024-05-06-teranoptia/">F]</a></p>

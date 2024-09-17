---
title: "Building Reliable Voice Agents with Open Source Tools"
date: 2024-09-13
author: "ZanSara"
featuredImage: "/posts/2024-09-13-odsc-europe-voice-agents/cover.png"
draft: true
---

*This is a write-up of my talk at [ODSC Europe 2024](/talks/2024-09-05-odsc-europe-voice-agents/).*

---

In the last few years, the world of voice agents saw dramatic leaps forward in the state of the art of all its most basic components. Thanks mostly to OpenAI, bots are now able to understand human speech almost like a human would, they're able to speak back with completely naturally sounding voices, and are able to hold a free conversation that feels extremely natural.

But building voice bots is far from a solved problem. These improved capabilities are raising the quality bar, and even users accustomed to the simpler capabilities of old bots now expect a whole new level of quality when it comes to interacting with them.

In this post we're going to discuss how building a voice agent today looks like, from the very basics up to advanced prompting strategies to keep your LLM-based bots under control, and we're also going to see how to build such bots in practice from the ground up using a newly released library, Pipecat.

# Outline

- [What is a voice agent?](#what-is-a-voice-agent)
  - [Speech-to-text (STT)](#speech-to-text-stt)
  - [Text-to-speech (TTS)](#text-to-speech-tts)
  - [Logic engine](#logic-engine)
    - [Tree-based](#tree-based)
    - [Intent-based](#intent-based)
    - [LLM-based](#llm-based)
- [New challenges](#new-challenges)
- [Let's build a voice bot](#)
- [Looking forward](#)


# What is a voice agent?

As the name says, voice agents are programs that are able to carry on a task and/or take actions and decisions on behalf of a user ("software agents") by using voice as their primary mean of communication (as poopsed to the much more common text chat format). Voice agents are inherently harder to build than their text based counterparts: computers operate primarily with text, and the art of making machines understand human voices has been an elusive problem for decades.

Today, the basic architecture of a modern voice agent can be decomposed into three main fundamental building blocks:

- a **speech-to-text (STT)** component, tasked to translate an audio stream into readable text,
- the agent's **logic engine**, which works entirely with text only,
- a **text-to-speech (TTS)** component, which converts the bot's text responses back into an audio stream of synthetic speech.

![](/posts/2024-09-13-odsc-europe-voice-agents/structure-of-a-voice-bot.png)

Let's see the details of each.

## Speech to text (STT)

Speech-to-text software is able to convert the audio stream of a person saying something and produce a transcription of what the person said. Speech-to-text engines have a [long history](https://en.wikipedia.org/wiki/Speech_recognition#History), but their limitations have always been quite severe: they used to require fine-tuning on each individual speaker, have a rather high word error rate (WER) and they mainly worked strictly with native speakers of major languages, failing hard on foreign and uncommon accents and native speakers of less mainstream languages. These issues limited the adoption of this technology for anything else than niche software and research applications.

With the [first release of OpenAI's Whisper models](https://openai.com/index/whisper/) in late 2022, the state of the art improved dramatically. Whisper enabled transcription (and even direct translation) of speech from many languages with an impressively low WER, finally comparable to the performance of a human, all with relatively low resources, higher then realtime speed, and no finetuning required. Not only, but the model was free to use, as OpenAI [open-sourced it](https://huggingface.co/openai) together with a [Python SDK](https://github.com/openai/whisper), and the details of its architecture were [published](https://cdn.openai.com/papers/whisper.pdf), allowing the scientific community to improve on it.

![](/posts/2024-09-13-odsc-europe-voice-agents/whisper-wer.png)

_The WER (word error rate) of Whisper was extremely impressive at the time of its publication (see the full diagram [here](https://github.com/openai/whisper/assets/266841/f4619d66-1058-4005-8f67-a9d811b77c62))._


Since then, speech-to-text models kept improving at a steady pace. Nowadays the Whisper's family of models sees some competition for the title of best STT model from  companies such as [Deepgram](https://deepgram.com/), but it's still one of the best options in terms of open-source models.

## Text-to-speech (TTS)

Text-to-speech model perform the exact opposite task than speech-to-text models: their goal is to convert written text into an audio stream of synthetic speech. Text-to-speech has [historically been an easier feat](https://en.wikipedia.org/wiki/Speech_synthesis#History) than speech-to-text, but it also recently saw drastic improvements in the quality of the synthetic voices, to the point that it could nearly be considered a solved problem in its most basic form.

Today many companies (such as OpenAI, [Cartesia](https://cartesia.ai/sonic), [ElevenLabs](https://elevenlabs.io/), Azure and many others) offer TTS software with voices that sound nearly indistinguishable to a human. They also have the capability to clone a specific human voice with remarkably little training data (just a few seconds of speech) and to tune accents, inflections, tone and even emotion.

{{< raw >}}
<div>
<audio controls src="/posts/2024-09-13-odsc-europe-voice-agents/sonic-tts-sample.wav" style="width: 100%"></audio>
</div>
{{< /raw >}}

_[Cartesia's Sonic](https://cartesia.ai/sonic) TTS example of a gaming NPC. Note how the model subtly reproduces the breathing in between sentences._

TTS is still improving in quality by the day, but due to the incredibly high quality of the output competition now tends to focus on price and performance.

## Logic engine

Advancements in the agent's ability to talk to users goes hand in hand with the progress of natural language understanding (NLU), another field with a [long and complicated history](https://en.wikipedia.org/wiki/Natural_language_understanding#History). Until recently, the bot's ability to understand the user's request has been severely limited and often available only for major languages.

Based on the way their logic is implemented, today you may come across bots that rely on three different categories.

### Tree-based

Tree-based (or rule-based) logic is one of the earliest method of implementing chatbot's logic, still very popular today for its simplicity. Tree-based bots don't really try to understand what the user is saying, but listen to the user looking for a keyword or key sentence that will trigger the next step. For example, a customer support chatbot may look for the keyword "refund" to give the user any infomation about how to perform a refund, or the name of a discount campaign to explain the user how to take advantage of that.

Tree-based logic, while somewhat functional, doesn't really resemble a conversation and can become very frustrating to the user when the conversation tree was not designed with care, because it's difficult for the end user to understand which option or keyword they should use to achieve the desired outcome. It is also unsuitable to handle real questions and requests like a human would. 

One of its most effective usecases is as a first-line screening to triage incoming messages.

![](/posts/2024-09-13-odsc-europe-voice-agents/tree-based-logic.png)

_Example of a very simple decision tree for a chatbot. While rather minimal, this bot already has several flaws: there's no way to correct the information you entered at a previous step, and it has no ability to recognize synonyms ("I want to buy an item" would trigger the fallback route.)_

### Intent-based

In intent-based bots, **intents** are defined roughtly as "actions the users may want to do". With respect to a strict, keyword-based tree structure, intent-based bots may switch from an intent to another much more easily (because they lack a strict tree-based routing) and may use advanced AI techniques to understand what the user is actually trying to accomplish and perform the required action.

Advanced voice assistants such as Siri and Alexa use variations of this intent-based system. However, as their owners are usually familiar with, interacting with an intent-based bot doesn't always feel natural, especially when the available intents don't match the user's expectation and the bot ends up triggering an unexpected action. In the long run, this ends with users carefully second-guessing what words and sentence structures activate the response they need and eventually leads to a sort of "magical incantation" style of prompting the agent, where the user has to learn what is the "magical sentence" that the bot will recognize to perform a specific intent without misunderstandings.

![](/posts/2024-09-13-odsc-europe-voice-agents/amazon-echo.webp)

_Modern voice assistants like Alexa and Siri are often built on the concept of intent (image from Amazon)._

### LLM-based

The introduction of instruction-tuned GPT models like ChatGPT revolutionized the field of natural languahe understanding and, with it, the way bots can be built today. LLMs are naturally good at conversation and can formulate natural replies to any sort of question, making the conversation feel much more natural than with any technique that was ever available earlier.

However, LLMs tend to be harder to control. Their very ability of generating naturally souding responses for anything makes them behave in ways that are often unexpected to the developer of the chatbot: for example, users can get the LLM-based bot to promise them anything they ask for, or they can be convinced to say something incorrect or even occasionally lie.

The problem of controlling the conversation, one that traditionally was always on the user's side, is now entirely on the shoulders of the developers and can easily backfire.

![](/posts/2024-09-13-odsc-europe-voice-agents/chatgpt-takesies-backsies.png)

_In a rather [famous instance](https://x.com/ChrisJBakke/status/1736533308849443121), a user managed to convince a Chevrolet dealership chatbot to promise selling him a Chevy Tahoe for a single dollar._


# New challenges

Thanks to all these recent improvements, it would seem that making natural-sounding, smart voice bots is getting easier and easier. It is indeed much simpler to make a simple bot sound better, understand more and respond appropriately, but there's still a long way to go before users can interact with these new bots as they would with a human.

The issue lays in the fact that users expectations grow with the quality of the bot. It's not enough for the bot to have a voice that shoulds human: users want to be able to interact with it in a way that it feels human too, which is far more rich and interactive than what the rigid tech of earlier chatbots made us assume.

What does this mean in practice? What are the expectations that users might have from our bots?

## Real speech is not turn-based

Traditional bots can only handle turn-based conversations: the user talks, then the bot talks as well, then the user talks some more, and so on. A conversation with another human, however, has no such limitation: people may talk over each other, interrupt each other and give audible feedback in several ways.

Here are some examples of this richer interaction style:

- **Interruptions**. Interruptions occur when a person is talking and another one starts talking at the same time. It is expected that the first person stops talking, at least for a few seconds, to understand what the interruption was about, while the second person continue to talk.

- **Back-channeling**: Back-channeling is the practice of saying "ok", "sure", "right" while the other p





<p class="fleuron"><a href="https://www.zansara.dev/posts/2024-05-06-teranoptia/">F]</a></p>

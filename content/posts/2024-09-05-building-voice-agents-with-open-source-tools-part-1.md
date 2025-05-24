---
title: "Building Reliable Voice Bots with Open Source Tools - Part 1"
date: 2024-09-20
author: "ZanSara"
featuredImage: "/posts/2024-09-05-building-voice-agents-with-open-source-tools/cover.png"
aliases:
- /posts/2024-09-05-odsc-europe-voice-agents-part-1
- /posts/2024-09-05-voice-bots-1/
---

{{< audio 
    audioFile="/posts/2024-09-05-building-voice-agents-with-open-source-tools/Building Reliable Voice Bots with Open Source Tools - Part 1.mp3" 
    speechifyLink="https://app.speechify.com/share/56beca57-948d-4084-8d8c-b704e94a5a2b"
>}}

*This is part one of the write-up of my talk at [ODSC Europe 2024](/talks/2024-09-05-building-voice-agents-with-open-source-tools/) and [ODSC West 2024](/talks/2024-10-29-odsc-west-voice-agents/).*

---

In the last few years, the world of voice agents saw dramatic leaps forward in the state of the art of all its most basic components. Thanks mostly to OpenAI, bots are now able to understand human speech almost like a human would, they're able to speak back with completely naturally sounding voices, and are able to hold a free conversation that feels extremely natural.

But building voice bots is far from a solved problem. These improved capabilities are raising the bar, and even users accustomed to the simpler capabilities of old bots now expect a whole new level of quality when it comes to interacting with them.

In this post we're going to focus mostly on **the challenges**: we'll discuss the basic structure of most voice bots today, their shortcomings and the main issues that you may face on your journey to improve the quality of the conversation.

In [Part 2](/posts/2024-10-30-building-voice-agents-with-open-source-tools-part-2/) we are going to focus on **the solutions** that are available today, and we are going to build our own voice bot using [Pipecat](https://www.pipecat.ai), a recently released open-source library that makes building these bots a lot simpler.

# Outline

- [What is a voice agent?](#what-is-a-voice-agent)
  - [Speech-to-text (STT)](#speech-to-text-stt)
  - [Text-to-speech (TTS)](#text-to-speech-tts)
  - [Logic engine](#logic-engine)
    - [Tree-based](#tree-based)
    - [Intent-based](#intent-based)
    - [LLM-based](#llm-based)
  - [Audio-to-audio models](#audio-to-audio)
- [New challenges](#new-challenges)
  - [Real speech is not turn-based](#real-speech-is-not-turn-based)
  - [Real conversation flows are not predictable](#real-conversation-flows-are-not-predictable)
  - [LLMs bring their own problems](#llms-bring-their-own-problems)
  - [The context window](#the-context-window)
  - [Working in real time](#working-in-real-time)

_Continues in [Part 2](/posts/2024-10-30-building-voice-agents-with-open-source-tools-part-2/)._


# What is a voice agent?

As the name says, voice agents are programs that are able to carry on a task and/or take actions and decisions on behalf of a user ("software agents") by using voice as their primary mean of communication (as opposed to the much more common text chat format). Voice agents are inherently harder to build than their text based counterparts: computers operate primarily with text, and the art of making machines understand human voices has been an elusive problem for decades.

Today, the basic architecture of a modern voice agent can be decomposed into three main fundamental building blocks:

- a **speech-to-text (STT)** component, tasked to translate an audio stream into readable text,
- the agent's **logic engine**, which works entirely with text only,
- a **text-to-speech (TTS)** component, which converts the bot's text responses back into an audio stream of synthetic speech.

![](/posts/2024-09-05-building-voice-agents-with-open-source-tools/structure-of-a-voice-bot.png)

Let's see the details of each.

## Speech to text (STT)

Speech-to-text software is able to convert the audio stream of a person saying something and produce a transcription of what the person said. Speech-to-text engines have a [long history](https://en.wikipedia.org/wiki/Speech_recognition#History), but their limitations have always been quite severe: they used to require fine-tuning on each individual speaker, have a rather high word error rate (WER) and they mainly worked strictly with native speakers of major languages, failing hard on foreign and uncommon accents and native speakers of less mainstream languages. These issues limited the adoption of this technology for anything else than niche software and research applications.

With the [first release of OpenAI's Whisper models](https://openai.com/index/whisper/) in late 2022, the state of the art improved dramatically. Whisper enabled transcription (and even direct translation) of speech from many languages with an impressively low WER, finally comparable to the performance of a human, all with relatively low resources, higher then realtime speed, and no finetuning required. Not only, but the model was free to use, as OpenAI [open-sourced it](https://huggingface.co/openai) together with a [Python SDK](https://github.com/openai/whisper), and the details of its architecture were [published](https://cdn.openai.com/papers/whisper.pdf), allowing the scientific community to improve on it.

![](/posts/2024-09-05-building-voice-agents-with-open-source-tools/whisper-wer.png)

_The WER (word error rate) of Whisper was extremely impressive at the time of its publication (see the full diagram [here](https://github.com/openai/whisper/assets/266841/f4619d66-1058-4005-8f67-a9d811b77c62))._


Since then, speech-to-text models kept improving at a steady pace. Nowadays the Whisper's family of models sees some competition for the title of best STT model from  companies such as [Deepgram](https://deepgram.com/), but it's still one of the best options in terms of open-source models.

## Text-to-speech (TTS)

Text-to-speech model perform the exact opposite task than speech-to-text models: their goal is to convert written text into an audio stream of synthetic speech. Text-to-speech has [historically been an easier feat](https://en.wikipedia.org/wiki/Speech_synthesis#History) than speech-to-text, but it also recently saw drastic improvements in the quality of the synthetic voices, to the point that it could nearly be considered a solved problem in its most basic form.

Today many companies (such as OpenAI, [Cartesia](https://cartesia.ai/sonic), [ElevenLabs](https://elevenlabs.io/), Azure and many others) offer TTS software with voices that sound nearly indistinguishable to a human. They also have the capability to clone a specific human voice with remarkably little training data (just a few seconds of speech) and to tune accents, inflections, tone and even emotion.

{{< raw >}}
<div>
<audio controls src="/posts/2024-09-05-building-voice-agents-with-open-source-tools/sonic-tts-sample.wav" style="width: 100%"></audio>
</div>
{{< /raw >}}

_[Cartesia's Sonic](https://cartesia.ai/sonic) TTS example of a gaming NPC. Note how the model subtly reproduces the breathing in between sentences._

TTS is still improving in quality by the day, but due to the incredibly high quality of the output competition now tends to focus on price and performance.

## Logic engine

Advancements in the agent's ability to talk to users goes hand in hand with the progress of natural language understanding (NLU), another field with a [long and complicated history](https://en.wikipedia.org/wiki/Natural_language_understanding#History). Until recently, the bot's ability to understand the user's request has been severely limited and often available only for major languages.

Based on the way their logic is implemented, today you may come across bots that rely on three different categories.

### Tree-based

Tree-based (or rule-based) logic is one of the earliest method of implementing chatbot's logic, still very popular today for its simplicity. Tree-based bots don't really try to understand what the user is saying, but listen to the user looking for a keyword or key sentence that will trigger the next step. For example, a customer support chatbot may look for the keyword "refund" to give the user any information about how to perform a refund, or the name of a discount campaign to explain the user how to take advantage of that.

Tree-based logic, while somewhat functional, doesn't really resemble a conversation and can become very frustrating to the user when the conversation tree was not designed with care, because it's difficult for the end user to understand which option or keyword they should use to achieve the desired outcome. It is also unsuitable to handle real questions and requests like a human would. 

One of its most effective usecases is as a first-line screening to triage incoming messages.

![](/posts/2024-09-05-building-voice-agents-with-open-source-tools/tree-based-logic.png)

_Example of a very simple decision tree for a chatbot. While rather minimal, this bot already has several flaws: there's no way to correct the information you entered at a previous step, and it has no ability to recognize synonyms ("I want to buy an item" would trigger the fallback route.)_

### Intent-based

In intent-based bots, **intents** are defined roughly as "actions the users may want to do". With respect to a strict, keyword-based tree structure, intent-based bots may switch from an intent to another much more easily (because they lack a strict tree-based routing) and may use advanced AI techniques to understand what the user is actually trying to accomplish and perform the required action.

Advanced voice assistants such as Siri and Alexa use variations of this intent-based system. However, as their owners are usually familiar with, interacting with an intent-based bot doesn't always feel natural, especially when the available intents don't match the user's expectation and the bot ends up triggering an unexpected action. In the long run, this ends with users carefully second-guessing what words and sentence structures activate the response they need and eventually leads to a sort of "magical incantation" style of prompting the agent, where the user has to learn what is the "magical sentence" that the bot will recognize to perform a specific intent without misunderstandings.

![](/posts/2024-09-05-building-voice-agents-with-open-source-tools/amazon-echo.webp)

_Modern voice assistants like Alexa and Siri are often built on the concept of intent (image from Amazon)._

### LLM-based

The introduction of instruction-tuned GPT models like ChatGPT revolutionized the field of natural language understanding and, with it, the way bots can be built today. LLMs are naturally good at conversation and can formulate natural replies to any sort of question, making the conversation feel much more natural than with any technique that was ever available earlier.

However, LLMs tend to be harder to control. Their very ability of generating naturally sounding responses for anything makes them behave in ways that are often unexpected to the developer of the chatbot: for example, users can get the LLM-based bot to promise them anything they ask for, or they can be convinced to say something incorrect or even occasionally lie.

The problem of controlling the conversation, one that traditionally was always on the user's side, is now entirely on the shoulders of the developers and can easily backfire.

![](/posts/2024-09-05-building-voice-agents-with-open-source-tools/chatgpt-takesies-backsies.png)

_In a rather [famous instance](https://x.com/ChrisJBakke/status/1736533308849443121), a user managed to convince a Chevrolet dealership chatbot to promise selling him a Chevy Tahoe for a single dollar._

## Audio-to-audio models

On top of all these changes, OpenAI recently made a step further. They latest flagship model, [GPT 4o](https://openai.com/index/hello-gpt-4o/), was allegedly able to understand audio natively, taking away the need for a dedicated speech-to-text model, and to produce audio responses directly, making text-to-speech engines also redundant. 

For a long time these capabilities were heavily restricted to a limited number of partners, but as of the 1st of October 2024, they eventually made such capabilities generally available through their new [Realtime API](https://openai.com/index/introducing-the-realtime-api/).

At a first glance, the release of such model seemed to shake the foundations of how we build voice bots today. However, at the time of writing, there are still a number of hurdles that prevents immediate adoption, the main one being **price**.

![](/posts/2024-09-05-building-voice-agents-with-open-source-tools/realtime-api-pricing.png)

_[Pricing of the Realtime API](https://openai.com/api/pricing/) at the time of writing (October 2024)_

The problem here is that voice bots built with the traditional stack can be more than sufficient to cover the most common usecases for a fraction of the price of GPT 4o, and while the latter can indeed handle cases that are impossible to address for a traditional voice bot, in most practical situations such capabilities are not necessary to achieve a smooth and effective interaction.

However, GPT 4o is surely a step further on the evolutionary path of modern voice bots. With potential future price changes, a model like this could easily become a valid competitor to the architecture we're going to explore in the rest of the post, with its own pros and cons.

# New challenges

Thanks to all these recent improvements, it would seem that making natural-sounding, smart bots is getting easier and easier. It is indeed much simpler to make a simple bot sound better, understand more and respond appropriately, but there's still a long way to go before users can interact with these new bots as they would with a human.

The issue lays in the fact that **users expectations grow** with the quality of the bot. It's not enough for the bot to have a voice that sounds human: users want to be able to interact with it in a way that it feels human too, which is far more rich and interactive than what the rigid tech of earlier chatbots allowed so far.

What does this mean in practice? What are the expectations that users might have from our bots?

## Real speech is not turn-based

Traditional bots can only handle turn-based conversations: the user talks, then the bot talks as well, then the user talks some more, and so on. A conversation with another human, however, has no such limitation: people may talk over each other, give audible feedback without interrupting, and more.

Here are some examples of this richer interaction style:

- **Interruptions**. Interruptions occur when a person is talking and another one starts talking at the same time. It is expected that the first person stops talking, at least for a few seconds, to understand what the interruption was about, while the second person continue to talk.

- **Back-channeling**. Back-channeling is the practice of saying "ok", "sure", "right" while the other person is explaining something, to give them feedback and letting them know we're paying attention to what is being said. The person that is talking is not supposed to stop: the aim of this sort of feedback is to let them know they are being heard.

- **Pinging**. This is the natural reaction a long silence, especially over a voice-only medium such as a phone call. When one of the two parties is supposed to speak but instead stays silent, the last one that talked might "ping" the silent party by asking "Are you there?", "Did you hear?", or even just "Hello?" to test whether they're being heard. This behavior is especially difficult to handle for voice agents that have a significant delay, because it may trigger an ugly vicious cycle of repetitions and delayed replies.

- **Buying time**. When one of the parties know that it will stay silent for a while, a natural reaction is to notify the other party in advance by saying something like "Hold on...", "Wait a second...", "Let me check..." and so on. This message has the benefit of preventing the "pinging" behavior we've seen before and can be very useful for voice bots that may need to carry on background work during the conversation, such as looking up information.

- **Audible clues**. Not everything can be transcribed by a speech-to-text model, but audio carries a lot of nuance that is often used by humans to communicate. A simple example is pitch: humans can often tell if they're talking to a child, a woman or a man by the pitch of their voice, but STT engines don't transcribe that information. So if a child picks up the phone, the model won't pick up the obvious audible clue and will likely assume it is talking to an adult. Similar considerations should be made for tone (to detect mood, sarcasm, etc) or other sounds like laughter, sobs, and more. **Audio-to-audio models** such as GPT 4o don't have this intrinsic limitation, but while they surely can pick up these clues, their ability to use them effectively should not be taken for granted.

## Real conversation flows are not predictable

Tree-based bots, and to some degree intent-based too, work on the implicit assumption that conversation flows are largely predictable. Once the user said something and the bot replied accordingly, they can only follow up with a fixed set of replies and nothing else.

This is often a flawed assumption and the primary reason why talking to chatbots tends to be so frustrating.

In reality, natural conversations are largely unpredictable. For example, they may feature:

- **Sudden changes of topic**. Maybe user and bot were talking about making a refund, but then the user changes their mind and decides to ask for assistance finding a repair center for the product. Well designed intent-based bots can deal with that, but most bots are in practice unable to do so in a way that feels natural to the user.

- **Unexpected, erratic phrasing**. This is common when users are nervous or in a bad mood for any reason. Erratic, convoluted phrasing, long sentences, rambling, are all very natural ways of expressing themselves, but such outbursts very often confuse bots completely.

- **Non native speakers**. Due to the nature la language learning, non native speakers may have trouble pronouncing words correctly, they may use highly unusual synonyms, or structure sentences in complicated ways. This is also difficult for bots to handle, because understanding the sentence is harder and transcription issues are far more likely.

- _**Non sequitur**_. _Non sequitur_ is an umbrella term for a sequence of sentences that bear no relation to each other in a conversation. A simple example is the user asking the bot "What's the capital of France" and the bot replies "It's raining now". When done by the bot, this is often due to a severe transcription issue or a very flawed conversation design. When done by the user, it's often a malicious intent to break the bot's logic, so it should be handled with some care.

## LLMs bring their own problems

It may seem that some of these issues, especially the ones related to conversation flow, could be easily solved with an LLM. These models, however, bring their own set of issues too:

- **Hallucinations**. This is a technical term to say that LLMs can occasionally mis-remember information, or straight up lie. The problem is that they're also very confident about their statements, sometimes to the point of trying to gaslight their users. Hallucinations are a major problem for all LLMs: although it may seem to get more manageable with larger and smarter models, the problem only gets more subtle and harder to spot.

- **Misunderstandings**. While LLMs are great at understanding what the user is trying to say, they're not immune to misunderstandings. Unlike a human though, LLMs rarely suspect a misunderstanding and they rather make assumptions that ask for clarifications, resulting in surprising replies and behavior that are reminiscent of intent-based bots.

- **Lack of assertiveness**. LLMs are trained to listen to the user and do their best to be helpful. This means that LLMs are also not very good at taking the lead of the conversation when we would need them to, and are easily misled and distracted by a motivated user. Preventing your model to give your user's a literary analysis of their unpublished poetry may sound silly, but it's a lot harder than many suspect.

- **Prompt hacking**. Often done with malicious intent by experienced users, prompt hacking is the practice of convincing an LLM to reveal its initial instructions, ignore them and perform actions they are explicitly forbidden from. This is especially dangerous and, while a lot of work has gone into this field, this is far from a solved problem.

## The context window

LLMs need to keep track of the whole conversation, or at least most of it, to be effective. However, they often have a limitation to the amount of text they can keep in mind at any given time: this limit is called **context window** and for many models is still relatively low, at about 2000 tokens **(between 1500-1800 words)**. 

The problem is that this window also need to include all the instructions your bot needs for the conversation. This initial set of instructions is called **system prompt**, and is slightly distinct from the other messages in the conversation to make the LLM understand that it's not part of it, but it's a set of instructions about how to handle the conversation.

For example, a system prompt for a customer support bot may look like this:

```
You're a friendly customer support bot named VirtualAssistant. 
You are always kind to the customer and you must do your best 
to make them feel at ease and helped.

You may receive a set of different requests. If the users asks
you to do anything that is not in the list below, kindly refuse
to do so.

# Handle refunds

If the user asks you to handle a refund, perform these actions:
- Ask for their shipping code
- Ask for their last name
- Use the tool `get_shipping_info` to verify the shipping exists
...

# Handle subscriptions

If the user asks you to subscribe to a service, perform these actions:
- Ask what subscription are they interested in
- Ask if they have a promo code
- Ask for their username
...

```
and so on.

Although very effective, system prompts have a tendency to become huge in terms of tokens. Adding information to it makes the LLM behave much more like you expect (although it's not infallible), hallucinate less, and can even shape its personality to some degree. But if the system prompt becomes too long (more than 1000 words), this means that the bot will only be able to exchange about 800 words worth of messages with the user before it starts to **forget** either its instructions or the first messages of the conversation. For example, the bot will easily forget its own name and role, or it will forget the user's name and initial demands, which can make the conversation drift completely.

## Working in real time

If all these issues weren't enough, there's also a fundamental issue related to voice interaction: **latency**. Voice bots interact with their users in real time: this means that the whole pipeline of transcription, understanding, formulating a reply and synthesizing it back but be very fast.

How fast? On average, people expect a reply from another person to arrive within **300-500ms** to sound natural. They can normally wait for about 1-2 seconds. Any longer and they'll likely ping the bot, breaking the flow.

This means that, even if we had some solutions to all of the above problems (and we do have some), these solutions needs to operate at blazing fast speed. Considering that LLM inference alone can take the better part of a second to even start being generated, latency is often one of the major issues that voice bots face when deployed at scale.

![](/posts/2024-09-05-building-voice-agents-with-open-source-tools/ttft.jpg)

_Time to First Token (TTFT) stats for several LLM inference providers running Llama 2 70B chat. From [LLMPerf leaderboard](https://github.com/ray-project/llmperf-leaderboard). You can see how the time it takes for a reply to even start being produced is highly variable, going up to more than one second in some scenarios._  


# To be continued...

_Interested? Check out [Part 2](/posts/2024-10-30-building-voice-agents-with-open-source-tools-part-2)!_ 


<p class="fleuron"><a href="https://www.zansara.dev/posts/2024-05-06-teranoptia/">F]</a></p>

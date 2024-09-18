---
title: "Building Reliable Voice Bots with Open Source Tools - Part 2"
date: 2024-09-20
author: "ZanSara"
featuredImage: "/posts/2024-09-05-odsc-europe-voice-agents/cover.png"
draft: true
---

*This is part two of the write-up of my talk at [ODSC Europe 2024](/talks/2024-09-05-odsc-europe-voice-agents/).*

---

In the last few years, the world of voice agents saw dramatic leaps forward in the state of the art of all its most basic components. Thanks mostly to OpenAI, bots are now able to understand human speech almost like a human would, they're able to speak back with completely naturally sounding voices, and are able to hold a free conversation that feels extremely natural.

But building voice bots is far from a solved problem. These improved capabilities are raising the bar, and even users accustomed to the simpler capabilities of old bots now expect a whole new level of quality when it comes to interacting with them.

In [Part 1](/posts/2024-09-05-odsc-europe-voice-agents-part-1/) we've seen mostly **the challenges** related to building such bot: we discussed the basic structure of most voice bots today, their shortcomings and the main issues that you may face on your journey to improve the quality of the conversation.

In this post instead we will focus on **the solutions** that are available today and we are going to build our own voice bot using [Pipecat](www.pipecat.ai), a recently released open-source library that makes building these bots a lot simpler.

# Outline

_Start from [Part 1](/posts/2024-09-05-odsc-europe-voice-agents-part-1/)._

- [Let's build a voice bot](#lets-build-a-voice-bot)
  - [Voice Activity Detection](#voice-activity-detection-vad)
  - [Blend intent's control with LLM's fluency](#blend-intents-control-with-llms-fluency)
    - [Intent detection](#intent-detection)
    - [Prompt building](#prompt-building)
    - [Reply generation](#reply-generation)
  - [What about latency](#what-about-latency)
- [The code](#the-code)
- [Looking forward](#looking-forward)


# Let's build a voice bot

At this point we have a comprehensive view of the issues that we need to solve to create a reliable, usable and natural-sounding voice agents. How can we actually build one?

First of all, let's take a look at the structure we defined earlier and see how we can improve on it.

![](/posts/2024-09-05-odsc-europe-voice-agents/structure-of-a-voice-bot.png)

## Voice Activity Detection (VAD)

One of the simplest improvements to this simple pipeline is the addition of a robust Voice Activity Detection (VAD) model. VAD gives the bot the ability to hear interruptions from the user and react to them accordingly, helping to break the classic, rigid turn-based interactions of old-style bots.

![](/posts/2024-09-05-odsc-europe-voice-agents/structure-of-a-voice-bot-vad.png)

However, on its own VAD models are not enough. To make a bot truly interruptible we also need the rest of the pipeline to be aware of the possibility of an interruption and be ready to handle it: speech-to-text models need to start transcribing and the text-to-speech component needs to stop speaking as soon as the VAD picks up speech. 

The logic engine also needs to handle a half-spoken reply in a graceful way: it can't just assume that the whole reply it planned to deliver was received, and neither it can drop the whole reply as it never started happening. LLMs can handle this scenario, however implementing it in practice is often not straightorward.

The quality of your VAD model matters a lot, as well as tuning its parameters appropriately. You don't want the bot to interrupt itself at every ambient sound it detects, but you also want the interruption to happen promptly.

Some of the best and most used models out there are [Silero](https://github.com/snakers4/silero-vad)'s VAD models, or alternatively [Picovoice](https://picovoice.ai/)'s [Cobra](https://picovoice.ai/platform/cobra/) models.

## Blend intent's control with LLM's fluency

Despite the distinctions we made at the start, often the logic of voice bots is implemented in a blend of more than one style. Intent-based bots may contain small decision trees, as well as LLM prompts. Often these approaches deliver the best results by taking the best of each approach to compensate for the weaknesss of the others.

One of the most effective approaches is to use intent detection to help control the flow of an LLM conversation. Let's see how.

![](/posts/2024-09-05-odsc-europe-voice-agents/structure-of-a-voice-bot-intent.png)

Suppose we're building a general purpose customer support bot.

A bot like this needs to be able to handle a huge variety of requests: helping the user renew subscriptions, buy or return items, update them on the state of a shipping, telling the opening hours of the certified repair shop closer to their home, explaining the advantages of a promotion, and more. 

If we decide to implement this chatbot based on intents, many intent may end up looking so similar that the bot will have trouble deciding which one suits a specific request the best: for example, a user that wants to know if there's any repair shop within a hour's drive from their home, otherwise they'll return the item.

However, if we decide to implement this chatbot with an LLM, it becomes really hard to check its replies and make sure that the bot is not lying, because the amount of information it needs to handle is huge. The bot may also perform actions that it is not supposed to, like letting users return an item they have no warranty on anymore.

There is an intermediate solution: **first try to detect intent, then leverage the LLM**.

### Intent detection

Step one is detecting the intention of the user. Given that this is a hybrid approach, we don't need to micromanage the model here and we can stick to macro-categories safely. No need to specify "opening hours of certified repair shops in New York", bur rather "information on certified repair shops" in general will suffice.

This first steps narrows down drastically the information the LLM needs to handle, and it can be repeated at every message, to make sure the user is still talking about the same topic and didn't change subject completely.

Intent detection can be performed with several tools, but it can be done with an LLM as well. Large models like GPT 4o are especially good at this sort of classification even when queried with a simple prompt like the following:

```
Given the following conversation, select what the user is currently talking about, 
picking an item from the "topics" list. Output only the topic name.

Topics: 

[list of all the expected topics + catchall topics]

Conversation: 

[conversation history]
```

### Prompt building

Once we know more or less what the request is about, it's time to build the real prompt that will give us a reply for the user.

With the general intent identified, we can equip the LLM strictly with the tools and information that it needs to proceed. If the user is asking about repair shops in their area, we can provide the LLM with a tool to search repair shops by zip code, a tool that would be useless if the user was asking about a shipment or a promotional campaign. Same for the background information: we don't need to tell the LLM that "you're a customer support bot", but we can narrow down its personality and background knowledge to make it focus a lot more on the task at hand, which is to help the user locating a suitable repair shop. And so on.

This can be done by mapping each expected intent to a specific system prompt, pre-compiled to match the intent. At the prompt building stage we simply pick from our library of prompts and **replace the system prompt** with the one that we just selected.

### Reply generation

With the new, more appropriate system prompt in place at the head of the conversation, we can finally prompt the LLM again to generate a reply for the user. At this point the LLM, following the instructions of the updated prompt, has an easier time following its instructions (because they're simpler and more focused) and generated better quality answers for both the users and the developers.

## What about latency?

# The code



# Looking forward


<p class="fleuron"><a href="https://www.zansara.dev/posts/2024-05-06-teranoptia/">F]</a></p>

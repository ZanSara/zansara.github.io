---
title: "Beyond the hype of reasoning models: debunking three common misunderstandings"
description: "This is a teaser for my upcoming talk at ODSC East 2025, \"LLMs that Think: Demystifying Reasoning Models\". If you want to learn more, join the webinar!"
date: 2025-05-12
author: "ZanSara"
featured-image: "/posts/2025-05-12-beyond-hype-reasoning-models/cover.png"
---

With the release of OpenAI’s o1 and similar models such as DeepSeek R1, Gemini 2.0 Flash Thinking, Phi 4 Reasoning and more, a new type of LLMs entered the scene: the so-called reasoning models. With their unbelievable scores in the toughest benchmarks for machine intelligence, reasoning models immediately got the attention of most AI enthusiasts, sparking speculations about their capabilities and what those could mean for the industry.

However, as often in the field of Generative AI, the hype makes it very difficult to understand at a glance what these models can really do. But before we jump into the details let’s clarify what we’re talking about.

## What is a reasoning model?

Reasoning models are LLMs that are able to “think”. Instead of generating a reply immediately after the user’s prompt, like every other LLM, they first generate a series of “reasoning tokens”, which is nothing more than the model thinking out loud, breaking down a complex problem into smaller steps, checking all its assumptions, asking itself whether it made any mistakes, double-checking its results, and so on. Once the model is satisfied by its conclusions, it starts generating actual response tokens that summarize the conclusions reached during the reasoning phase and presents those tokens to the user.

In the case of some models such as OpenAI’s, the reasoning tokens are hidden from the user. In otner models, such as most open source ones, the reasoning output can be returned to the user as well. However, this trace is not optimized to be read by people, so it often looks odd and contrived even when it reaches the correct conclusions.

Now that we understand better what a reasoning model is, let’s discuss a few common misunderstandings related to them.

## Are reasoning models AGI?

AGI stands for Artificial General Intelligence, and it’s one of the most ill-defined terms in Generative AI. Several people have tried to offer a more precise definition of this term, out of which my favourite is the following:

> AGI is an AI that is better than any human at any economically valuable task.

Under this light it’s clear that no current LLM, not even the most advanced reasoning model, it yet at the level where it could replace any human at any task. They can surely offer very valuable help with their vast knowledge and their growing ability to reason, but they’re not yet at the point where they can take onto any job without further specialization and complex tooling around them.

## Are reasoning models AI agents?

An AI agent is usually defined as any application that can use tools to achieve complex goals. Considering that reasoning models are usually able to use tools, it’s natural to think that they themselves may be considered AI agents.

In practice, however, reasoning models on their own hardly qualify as agents. Many powerful agents systems do have an LLM at their core: they use it to understand the user’s request and plan the actions to take to achieve the goal they’re set to. Reasoning models are a perfect fit as the minds of agents like that, due to their advanced capabilities to break down problems into smaller, manageable parts and self-correct their strategy on the fly if something goes wrong. Taken in isolation, though, reasoning models can’t be called AI agents.

## Are reasoning models glorified CoT prompts?

If you have worked with AI agents and other LLM systems designed to solve problems, you’ve surely come across Chain of Thought prompting. In short, this technique involves adding in the system prompt of your LLM instructions to “think step by step” before replying. This makes the LLM think out loud before reaching a conclusion and, even in regular non-reasoning LLMs, improves significantly their problem solving skills.

At a first glance, the output of a reasoning model may look precisely like the output of a CoT prompt, so some experts may think that their reasoning capabilities are the same. This is a mistake. Reasoning models are much more powerful than regular LLMs, even when these are equipped with a CoT prompt: this is because reasoning models pass through one additional step during their training where they learn to refine their “thinking step by step” skills through supervised learning on prompts with verifiable output, such as mathematical problems. Reasoning models are not zero-shot resoners like regular LLMs: they’re fine-tuned for it.

## Wrapping up

Reasoning models may not be the super-human intelligence some of us are waiting for, but they surely are a significant step forward toward LLMs with very strong reasoning abilities.

If you want to learn more about what reasoning models can do, how they reason, when to use them and more, make sure to attend my talk [LLMs that Think: Demystifying Reasoning Models](https://odsc.com/speakers/llms-that-think-demystifying-reasoning-models/) at this year’s virtual edition of [ODSC East](https://odsc.com/boston/). See you there!

<p class="fleuron"><a href="/posts/2024-05-06-teranoptia/">ifo</a></p>

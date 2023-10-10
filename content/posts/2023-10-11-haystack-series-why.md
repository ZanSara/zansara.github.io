---
title: "Haystack 2.0 - Why rewriting Haystack?!"
date: 2023-10-11
author: "ZanSara"
tags: ["Haystack 2.0", Haystack, LLM, NLP, Python, AI]
series: ["Haystack 2.0 Series"]
featuredImage: "/posts/2023-10-11-haystack-series-why.png"
draft: true
---

Before even starting to dive into what Haystack 2.0 is, how was it build, and how it works, let's spend a few words about the whats and the whys.

First of all, *what is* Haystack?

And next, why on Earth did we decide to rewrite it from the ground up?

### A Pioneer Framework

Haystack is a relatively young framework, its initial release dating back to [Nov 28, 2019](https://github.com/deepset-ai/haystack/releases/tag/0.1.0). Back then Natural Language Processing was a field that just started moving its first step outside from research labs, and Haystack is one of the first libraries that promised enterprise-grade, production-ready NLP features. We were proud to enable usecases such as [semantic search](https://medium.com/deepset-ai/what-semantic-search-can-do-for-you-ea5b1e8dfa7f), [FAQ matching](https://medium.com/deepset-ai/semantic-faq-search-with-haystack-6a03b1e13053), document similarity,  document summarization, machine translation, language-agnostic search, and so on. 

The field was niche but constantly moving, and research was lively. [The BERT paper](https://arxiv.org/abs/1810.04805) had been published a few months before Haystack's first release and it was unlocking a small revolution in itself. In the shade of much larger research labs such as Google's and Meta's deepset, then just at pre-seed stage, was also pouring effort into [research](https://arxiv.org/abs/2104.12741) and [model training](https://huggingface.co/deepset).

In those times, competition was close to non-existent. The field was still quite technical, and most people didn't know about its potential. We were mostly free to explore features and use cases at our own pace and to set the direction for our own product. This gave us the freedom to decide what to work on, what to double-down on, and what to deprioritize, postpone or ignore. Haystack was building its own space for itself in what was fundamentally a green field.


### ChatGPT

This rather idyllic situation came to an end all too abruptly at the end of November 2022, when [ChatGPT was released](https://openai.com/blog/chatgpt).

Since then, for us in the NLP field everything seemed to change overnight. Day by day. For *months*. 

The speed of progress went from lively to faster-than-light all at once. Every company with the budget to train an LLM seemed to be doing so and researchers kept releasing open-source models just as quickly, while open-source contributors pushed to reduce the hardware requirements for inference lower and lower. My best memory of those times is the drama of [LlaMa's first "release"](https://github.com/facebookresearch/llama/pull/73): I remember betting, on March 2nd, that within a week I would be running LlaMa models on my laptop and I wasn't even surprised when my prediction [turned out true](https://news.ycombinator.com/item?id=35100086) with the release of [llama.cpp](https://github.com/ggerganov/llama.cpp) on March 10th.

Of course, keeping up with this explosion was far beyond us. Competitors started to spawn like mushrooms, and our space was suddenly crowded with new startups, far more agile than us and better funded. All of a sudden we needed to compete, and we realized we weren't really used to it.

### PromptNode vs FARMReader

Luckily for us, Haystack was not in a bad shape. Thanks to the efforts of [Vladimir Blagojevic](https://twitter.com/vladblagoje), a few weeks after ChatGPT became a sensation we added some decent support for LLMs in the form of [PromptNode](https://github.com/deepset-ai/haystack/pull/3665), and our SaaS team could quickly start to demo some generative QA usecases to our customers. We even managed to add support for [Agents](https://github.com/deepset-ai/haystack/pull/3925), another hot topic in the wake of ChatGPT, despite some hard tradeoffs that we needed to take (more on them later).

However, the go-to library for LLMs was not Haystack in the mind of most developers. It was [LangChain](https://docs.langchain.com/docs/), and for a long time it seemed like we would never be able to challenge their status and popularity. Everyone was talking about it, everyone was building demos, products, startups on it, its development speed was unbelievable and, in the day-to-day discourse of the newly born LLM community, Haystack was nowhere to be found.

Why?

That's because no one even realized that Haystack, the semantic search framework from 2019, now supported LLMs as well. All our documentation, tutorials, blog posts, research efforts, models on HuggingFace, *everything* was pointing towards semantic search. No LLMs to be seen.

And semantic search was going down *fast*.

![Reader Models downloads graph](/posts/2023-10-11-haystack-series-why-reader-model-downloads.png)

*The image above shows today's monthly downloads for one of deepset's most successful models on HuggingFace, 
[deepset/roberta-base-squad2](https://huggingface.co/deepset/roberta-base-squad2). This model performs [extractive Question Answering](https://huggingface.co/tasks/question-answering), our primary use case before the release of ChatGPT. You can see how, even with more than one a half million downloads monthly, this model is experiencing a disastrous collapse in popularity, and in the current landscape it is very unlikely to ever recover.*


### A (Sort Of) Pivot

It is in this context that, around February 2023, we decided to bet on the rise of LLMs and committed to focus all our efforts towards becoming the #1 framework powering production-grade LLMs applications.

As we quickly realized, this was by far not an easy proposition for us. Extractive QA was not only ingrained deeply in our public image, but in our codebase as well: implementing and maintaining PromptNode was proving more and more painful by the day, and when we tried to fit the concept of Agents into Haystack, it felt uncomfortably like trying to force a square peg into a round hole.

Haystack pipelines were great at their job of making extractive QA simple for the users, and highly optimized for this usecase. But supporting LLMs was nothing like enabling extractive QA. Using Haystack for LLMs was quite a painful experience, and at the same time, modifying Pipeline to accomodate them seemed like the best way to mess with all the users that relied on Pipeline's for their existing, value-generating applications. Making mistakes with the current Pipeline could ruin us.

It is with this realization in mind that we took what I consider the best option for the future of Haystack: a rewrite. The knowledge and experience we gained while working on Haystack 1 could fuel the design of Haystack 2 and act as a reference frame for it. Unlike our competitors, we already knew a lot on how to make NLP work at scale and made many mistakes we would avoid in our next iteration. We knew that focusing on the best possible developer experience was what fueled the growth of Haystack 1 in the early days, and we were committed to do the same for the next version of it.

So the redesign of Haystack started, and it started from the concept of Pipeline.

### What's Next?

In the next post I am going to dwelve deeper into more details about Pipelines. Expect a much more technical piece, with code and software design discussion.

---

*Next: Soon!*

*Previous: [Haystack 2.0 - What is it?](/posts/2023-10-10-haystack-series-intro)*

*See the entire series here: [Haystack 2.0 series](/series/haystack-2.0-series/)*
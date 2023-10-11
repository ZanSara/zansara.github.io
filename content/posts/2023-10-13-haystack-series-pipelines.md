---
title: "Haystack 2.0 - Pipelines and Canals"
date: 2023-10-13
author: "ZanSara"
tags: ["Haystack 2.0", Haystack, LLM, NLP, Python, AI]
series: ["Haystack 2.0 Series"]
featuredImage: "/posts/2023-10-11-haystack-series-pipelines.png"
draft: true
---

...


.


Agents where a topic that was gaining steam: LLMs that not only reply to the users, but that are also able to reason about a topic, use tools, remember the past conversation. Agents were only beginning to take shape, but one thing was clear: supporting them not as "simple" as supporting text generation with LLMs has been. Agents required a whole new level of flexibility into connecting components together. Something that Haystack, so highly optimized toward the concept of Query and Indexing pipeline pairs, was not able to provide.

This itself was not a blocking issue. Soon after realizing that our Haystack Pipelines were not up to the task of supporting Agents, we decided to introduce them [as a standalone concept](https://github.com/deepset-ai/haystack/pull/3925) in the framework: a decision that helped us immensely to stay relevant in rollercoaster run that was ahead of us.

### A New Pipeline

This discussion lead to the realization that our pipelines were *rigid*. 

Haystack Pipelines were very easy to use for the usecases we met most often (extractive QA), but they were hard to bend to any other usecase. The discussion around how to best implement Agents surfaced a river of feedback about how Pipelines were very unruly outside of the most common usecases: PromptNode required extensive hacking of Pipeline's parameters, Tuana almost failed to implement a summarization demo a few weeks earlier, batch processing was very brittle and close to unusable, and implementing a pipeline with branches and joins was a task full of pitfalls and obscure bugs. Developer Experience in these scenarios was miserable: the idea that Retrieval Augmented Generation ([RAG](https://www.deepset.ai/blog/llms-retrieval-augmentation)) would become one of our most common usecases was dire, considering how difficult it was to make it work.

Surely we could do better than this!

### The Rewrite

The timing seemed quite right. It was time to either get onto the train of Generative AI or to stay behind. So we chose to take the risk, set aside some time and resources and start to understand what a new Pipeline  would look like, one that was flexible enough for the times ahead.

In the next post I'm going to go more into the details of what this new Pipeline ended up being. I am going to compare the typical traits of a Pipeline 1.x, its strenghts and its limitations, and then compare it with the features of Pipelines in Haystack 2.

---

*Next: Soon!*

*Previous: [Haystack 2.0 - Why rewriting Haystack?!](/posts/2023-10-10-haystack-series-why)*

*See the entire series here: [Haystack 2.0 series](/series/haystack-2.0-series/)*
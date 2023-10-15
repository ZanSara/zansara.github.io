---
title: "Canals"
date: 2023-10-20
author: "ZanSara"
tags: ["Haystack 2.0", Haystack, NLP, Python, Canals, Pipeline, DAG, graph, "API Design", "Semantic Search"]
series: ["Haystack 2.0 Series"]
featuredImage: "/posts/2023-10-20-haystack-series-canals/cover.png"
draft: true
---

.

.

.

.

- Example about flipping reader and retriever

- Explain why it works

- Explain why it can't be fixed easily

- Mention other cracks like lack of parallel branch execution


## New Use Cases

- GenAI requires even wilder graphs

- Example with web retrieval

- Agents would need loops if they're implemented as pipelines

- DAGs are not sufficient

- We start to desperately need validation and clear IO definitions

## Enter Canals

- Explain the key differences

- Explain the key difficulties and how we plan to address them.


## Bonus: do we *really* need the Pipeline tho?

- Mention how close a Canals pipeline is to a simple Python script

- Name the advantages (drawing, serialization, evaluation, high-level abstraction of component, flatter API surface)

- Clarify that the real value comes from the components and not from the way you orchestrate them.

.

.

.

.

.

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

*Previous: [Haystack's Pipeline](/posts/2023-10-13-haystack-series-pipeline)*

*See the entire series here: [Haystack 2.0 series](/series/haystack-2.0-series/)*
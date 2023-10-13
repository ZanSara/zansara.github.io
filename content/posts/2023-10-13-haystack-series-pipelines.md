---
title: "Haystack 2.0 - Pipelines and Canals"
date: 2023-10-13
author: "ZanSara"
tags: ["Haystack 2.0", Haystack, NLP, Python, Canals, Pipeline, DAG, graph, "API Design", "Semantic Search"]
series: ["Haystack 2.0 Series"]
featuredImage: "/posts/2023-10-13-haystack-series-pipelines.png"
draft: true
---

If you've ever looked at Haystack before you've surely met with the concept of Pipeline. Pipelines are one of the most prominent concepts of the framework and may have even inspired LangChain's chains, for what we know.

However, the Pipeline abstraction is by no means an obvious choice when it comes to NLP frameworks. Why did we adopt this concept, and what does it bring us? 

## A Bit Of History

In the very first releases of Haystack, interestingly, Pipelines were not a thing. Version 0.1.0 was released with a simpler object, the [Finder](https://github.com/deepset-ai/haystack/blob/d2c77f307788899eb562d3cb6e42c69b968b9f2a/haystack/__init__.py#L16), that little more than wrapping around a [Retriever](https://docs.haystack.deepset.ai/docs/retriever) and a [Reader](https://docs.haystack.deepset.ai/docs/reader), the two fundamental building blocks of a [semantic search](https://docs.haystack.deepset.ai/docs/glossary#semantic-search) application.

Soon the capabilities of language models started to expand and enable more usecases. One hot topic was [hybrid retrieval](https://haystack.deepset.ai/blog/hybrid-retrieval): a system composed of two different Retrievers, an optional [Ranker](https://docs.haystack.deepset.ai/docs/ranker), and an optional Reader. These kind of applications clearly didn't fit the Finder's design, so in [version 0.6.0](https://github.com/deepset-ai/haystack/releases/tag/v0.6.0) the [Pipeline](https://docs.haystack.deepset.ai/docs/pipelines) object was introduced: a new abstraction that allowed users to build applications made of graphs of components.

Pipeline's API were a huge step forward from Finder. They instantly enabled an amount of combinations that unlocked almost all usecases conceivable, and became a foundational concept of Haystack that was meant to stay for a very long time.

It's unsurprising then to realize that the API offered by Pipeline almost haven't changed since their initial release. This is the snippet included in the release notes of version 0.6.0 to showcase hybrid retrieval. Does it look familiar?
 
```python
p = Pipeline()
p.add_node(component=es_retriever, name="ESRetriever", inputs=["Query"])
p.add_node(component=dpr_retriever, name="DPRRetriever", inputs=["Query"])
p.add_node(component=JoinDocuments(join_mode="concatenate"), name="JoinResults", inputs=["ESRetriever", "DPRRetriever"])
p.add_node(component=reader, name="QAReader", inputs=["JoinResults"])
res = p.run(query="What did Einstein work on?", top_k_retriever=1)
```

## A Powerful Abstraction

One fascinating aspect of Haystack 1.x Pipeline is the simplicity of its user-facing API. In almost all examples you see only two or three methods:

- `add_node`: to add a component to the graph and connect it to the others.
- `run`: to run the whole system from start to finish.
- `draw`: to draw the graph of the pipeline to an image.

At this level, users don't need to know what kind of data the components need to function, or what they produce, or even what the components *do*: all they need to know is the place they must occupy in the graph for the system to work.

For example, as long as the users know that their hybrid retrieval pipeline should look something like this (note: this is the output of `Pipeline.draw()`), translating it into a Haystack pipeline using a few `add_node` calls is mostly straightforward.

![Hybrid Retrieval](/posts/2023-10-13-haystack-series-pipelines-hybrid-retrieval.png)

This fact is reflected by the documentation of the various components as well. For example, this is how the documentation page for Ranker opens:

![Ranker Documentation](/posts/2023-10-13-haystack-series-pipelines-ranker-docs.png)

Note how the very first information given about this component is *where to place it*. Right after, it does specify what are its inputs and outputs (more on this later), and then lists which specific classes can cover the role of a Ranker. 

The message is clear: all Ranker classes are functionally interchangeable and, as long as you place them correctly in the pipeline, they are going to fulfill the function of Ranker as you expect them to. Users don't need to understand what distinguishes `CohereRanker` from `RecentnessReranker` unless they want to: the documentation promises that you can swap them safely, and thanks to the Pipeline abstraction, this statement holds true for the large majority of cases. For most users, this is the dream.

There is only one issue with this model. How can the users know which graph they have to build?

## Ready-made Pipelines

Most NLP applications are made by a fairly limited number of high-level components: Retriever, Readers, Rankers, plus the occasional filter, translator, summarizer or query classifier. Systems requiring more than five components used to be really rare, at least when talking about "query" pipelines (more on this later).

But the most important point is that in most cases customizing the system did not imply customizing the graph. Pipeline graphs could be mapped to high-level usecases, such as semantic search, language-agnostic document search, hybrid retrieval, and so on. Users would identify their usecase, find an example or a tutorial defining the shape of the pipeline they need, and then swap the single components until they find the combination that works the best for their exact requirements.

This workflow was evident and encouraged: it was the philosophy behind Finder as well, and from version 0.6.0 Haystack immediately provided what are called "[Ready-made Pipelines](https://docs.haystack.deepset.ai/docs/ready_made_pipelines)": objects that initialized the graph on the user's behalf, and expected as input the components to place in each point of the graph: for example one Reader, two Retrievers, and a Ranker.

With this further abstracton on top of Pipeline, creating an NLP application became an action that doesn't even require the user to be aware of the existence of the graph. In fact:

```python
pipeline = ExtractiveQAPipeline(reader, retriever)
```

is enough to get your Extractive QA applications ready to answer your questions.


## "Flexibility powered by DAGs"

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

*Previous: [Haystack 2.0 - Why rewriting Haystack?!](/posts/2023-10-10-haystack-series-why)*

*See the entire series here: [Haystack 2.0 series](/series/haystack-2.0-series/)*
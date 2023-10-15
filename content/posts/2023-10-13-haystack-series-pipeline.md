---
title: "Haystack 2.0 - The Pipeline"
date: 2023-10-13
author: "ZanSara"
tags: ["Haystack 2.0", Haystack, NLP, Python, Canals, Pipeline, DAG, graph, "API Design", "Semantic Search"]
series: ["Haystack 2.0 Series"]
featuredImage: "/posts/2023-10-13-haystack-series-pipeline.png"
draft: true
---

If you've ever looked at Haystack before you've surely met with the concept of Pipeline. Pipelines are one of the most prominent concepts of the framework and may have even inspired LangChain's chains, for what we know.

However, the Pipeline abstraction is by no means an obvious choice when it comes to NLP frameworks. Why did we adopt this concept, and what does it bring us? 

In this post I am going to go into all the details of how Pipelines work in Haystack now, why they work this way, and what are its strenghts and weaknesses. This deep dive into the current state of the framework is also a premise to for my next post, where I am going to explain how Haystack 2.0 addresses this version's shortcomings.

And if you think you already know how Haystack Pipelines works, give this post a chance: I might manage to change your mind.

## A Bit Of History

In the very first releases of Haystack, interestingly, Pipelines were not a thing. Version 0.1.0 was released with a simpler object, the [Finder](https://github.com/deepset-ai/haystack/blob/d2c77f307788899eb562d3cb6e42c69b968b9f2a/haystack/__init__.py#L16), that little more than wrapping around a [Retriever](https://docs.haystack.deepset.ai/docs/retriever) and a [Reader](https://docs.haystack.deepset.ai/docs/reader), the two fundamental building blocks of a [semantic search](https://docs.haystack.deepset.ai/docs/glossary#semantic-search) application.

In the next few months, however, the capabilities of language models expanded to enable many more usecases. One hot topic was [hybrid retrieval](https://haystack.deepset.ai/blog/hybrid-retrieval): a system composed of two different Retrievers, an optional [Ranker](https://docs.haystack.deepset.ai/docs/ranker), and an optional Reader. These kind of applications clearly didn't fit the Finder's design, so in [version 0.6.0](https://github.com/deepset-ai/haystack/releases/tag/v0.6.0) the [Pipeline](https://docs.haystack.deepset.ai/docs/pipelines) object was introduced: a new abstraction that helped users build applications as a graph of components.

Pipeline's API were a huge step forward from Finder. They instantly enabled an amount of combinations that unlocked almost all usecases conceivable, and became a foundational concept of Haystack that was meant to stay for a very long time. In fact, the API offered by the very first version of Pipeline were already so powerful that to this date, they almost haven't changed. 

This is the snippet included in the release notes of version 0.6.0 to showcase hybrid retrieval. Does it look familiar?
 
```python
p = Pipeline()
p.add_node(component=es_retriever, name="ESRetriever", inputs=["Query"])
p.add_node(component=dpr_retriever, name="DPRRetriever", inputs=["Query"])
p.add_node(component=JoinDocuments(join_mode="concatenate"), name="JoinResults", inputs=["ESRetriever", "DPRRetriever"])
p.add_node(component=reader, name="QAReader", inputs=["JoinResults"])
res = p.run(query="What did Einstein work on?", top_k_retriever=1)
```

## A Powerful Abstraction

One fascinating aspect of this Pipeline model is the simplicity of its user-facing API. In almost all examples you see only two or three methods used:

- `add_node`: to add a component to the graph and connect it to the others.
- `run`: to run the whole system from start to finish.
- `draw`: to draw the graph of the pipeline to an image.

At this level, users don't need to know what kind of data the components need to function, or what they produce, or even what the components *do*: all they need to know is the place they must occupy in the graph for the system to work.

For example, as long as the users know that their hybrid retrieval pipeline should look more or less like this (note: this is the output of `Pipeline.draw()`), translating it into a Haystack pipeline using a few `add_node` calls is mostly straightforward.

![Hybrid Retrieval](/posts/2023-10-13-haystack-series-pipeline-hybrid-retrieval.png)

This fact is reflected by the documentation of the various components as well. For example, this is how the documentation page for Ranker opens:

![Ranker Documentation](/posts/2023-10-13-haystack-series-pipeline-ranker-docs.png)

Note how the very first information given about this component is *where to place it*. Right after, it does specify what are its inputs and outputs (more on this later), and then lists which specific classes can cover the role of a Ranker. 

The message is clear: all Ranker classes are functionally interchangeable and, as long as you place them correctly in the pipeline, they are going to fulfill the function of Ranker as you expect them to. Users don't need to understand what distinguishes `CohereRanker` from `RecentnessReranker` unless they want to: the documentation promises that you can swap them safely, and thanks to the Pipeline abstraction, this statement holds true for the majority of cases.

## Ready-made Pipelines

There is only one issue with this model. How can the users know which sort of graph they have to build?

Most NLP applications are made by a fairly limited number of high-level components: Retriever, Readers, Rankers, plus the occasional filter, translator, summarizer or query classifier. Systems requiring more than five components used to be really rare, at least when talking about "query" pipelines (more on this later).

Therefore, at this level of abstraction there are just a few graph topologies possible, and better yet, they could each be mapped to a high-level usecases, such as semantic search, language-agnostic document search, hybrid retrieval, and so on

But the most important point is that, in most cases, tailoring the application did not require any changes to the graph's shape. Users only need to identify their usecase, find an example or a tutorial defining the shape of the pipeline they need, and then swap the single components until they find the combination that works the best for their exact requirements.

This workflow was evident and encouraged: it was the philosophy behind Finder as well, and from version 0.6.0 Haystack immediately provided what are called "[Ready-made Pipelines](https://docs.haystack.deepset.ai/docs/ready_made_pipelines)": objects that initialized the graph on the user's behalf, and expected as input the components to place in each point of the graph: for example a Reader and a Retriever, in case of simple Extractive QA.

With this further abstracton on top of Pipeline, creating an NLP application became an action that doesn't even require the user to be aware of the existence of the graph. In fact:

```python
pipeline = ExtractiveQAPipeline(reader, retriever)
```

is enough to get your Extractive QA applications ready to answer your questions. And you can do so with just another line.

```python
answers = pipeline.run(query="What did Einstein work on?")
```

## Flexibility powered by DAGs

This abstraction is extremely powerful for the usecases that it was designed for. There are a few layers of ease of use versus customization the user can choose from depending on their expertise, which help them progress from a simple ready-made Pipeline to fully custom graphs. 

However, the focus was oriented so much on the initial stages of the user's journey that the needs of power-users were sometimes forgotten. Such issues didn't show immediately, but quickly added friction as soon as the users tried to customize their system beyond the examples contained in the tutorials and in the documentation.

For one simple example of these issues, let's talk about pipelines with branches. As an example, here are two apparently very similar pipelines.

![Query Classification vs Hybrid Retrieval](/posts/2023-10-13-haystack-series-pipeline-branching-query-pipelines.png)

The first pipeline represents the Hybrid Retrieval usecase we've met with before. Here, the Query node sends its outputs to both Retrievers and they both produce some documents. Therefore, in order for the Reader to make sense of this data, we need to have a Join node which merges the two lists into one, and then a Ranker which takes the lists, sorts them again by similarity to the query, and sends the re-arranged list to the Reader.

The second pipeline instead performs a simpler form of Hybrid Retrieval. Here the Query node sends its outputs to a Query Classifier, which then triggers only one of the two Retrievers. The Retriever that run then sends its output directly to Reader, which doesn't need to be aware of which Retriever the data comes from. 

The two pipelines are both built in the way you would expect, with a bunch of `add_node` calls, and running them is done with the same identical code, which is in fact the same code needed for every other pipeline we've seen so far.

```python
pipeline_1 = Pipeline()
pipeline_1.add_node(component=sparse_retriever, name="SparseRetriever", inputs=["Query"])
pipeline_1.add_node(component=dense_retriever, name="DenseRetriever", inputs=["Query"])
pipeline_1.add_node(component=join_documents, name="JoinDocuments", inputs=["SparseRetriever", "DenseRetriever"])
pipeline_1.add_node(component=rerank, name="Ranker", inputs=["JoinDocuments"])
pipeline_1.add_node(component=reader, name="Reader", inputs=["SparseRetriever", "DenseRetriever"])

answers = pipeline_1.run(query="What did Einstein work on?")
```
```python
pipeline_2 = Pipeline()
pipeline_2.add_node(component=query_classifier, name="QueryClassifier", inputs=["Query"])
pipeline_2.add_node(component=sparse_retriever, name="DPRRetriever", inputs=["QueryClassifier"])
pipeline_2.add_node(component=dense_retriever, name="ESRetriever", inputs=["QueryClassifier"])
pipeline_2.add_node(component=reader, name="Reader", inputs=["SparseRetriever", "DenseRetriever"])

answers = pipeline_2.run(query="What did Einstein work on?")
```

Both pipelines run, exactly as you would expect them to. Hoorray! Pipelines can branch and join!

Now, let's take the first pipeline and customize it further.

After we made sure our demo works well for English documents, we decide to expand language support to French. The dense retriever has no issues handling several languages, as long as we select a multilingual model; however, the sparse retriever needs the keywords to match, so we surely need to translate the queries to English if we want to find some relevant documents in our English-only knowledge base.

Here is how the Pipeline ends up looking like.

![Multilingual Hybrid Retrieval](/posts/2023-10-13-haystack-series-pipeline-multilingual-hybrid-retrieval.png)

```python
pipeline = Pipeline()
pipeline.add_node(component=language_classifier, name="LanguageClassifier", inputs=["Query"])
pipeline.add_node(component=translator, name="Translator", inputs=["LanguageClassifier.output_1"])
pipeline.add_node(component=sparse_retriever, name="SparseRetriever", inputs=["Translator", "LanguageClassifier.output_2"])
pipeline.add_node(component=dense_retriever, name="DenseRetriever", inputs=["LanguageClassifier.output_1", "LanguageClassifier.output_2"])
pipeline.add_node(component=join_documents, name="JoinDocuments", inputs=["SparseRetriever", "DenseRetriever"])
pipeline.add_node(component=rerank, name="Ranker", inputs=["JoinDocuments"])
pipeline.add_node(component=reader, name="Reader", inputs=["Ranker"])
```

In this pipeline, Language Classifier sends all French queries over `output_1`, and all English queries over `output_2`. In this way, they queries will pass throught the Translator node only if it was written in French.

But... wait. Let's look again at the graph, and at the code. DenseRetriever should be receiving *two* inputs: both `output_1` and `output_2`. That's what the code says, and what I need for the system to work. Is this a bug in `draw()`?

Thanks to the `debug=True` parameter of `Pipeline.run()`, we start inspecting what each node saw during the execution, and we realize quickly that our worst fears are true: this is a bug in the Pipeline implementation. The underlying library powering the pipeline's graphs takes the definition of Directed Acyclic Graphs very seriously, and does not allow two nodes to be connected by more than one edge, while in this case we are trying to draw two between the classifier and the dense retriever. There are, of course, other graph classes supporting this case, but Haystack happens to use the wrong one.

> Trivia

> This issue was discovered by our own Solutions Engineering team which, unsurprisingly, was building a Pipeline a bit more complex than the tutorials'. [Their pipeline](/posts/2023-10-13-haystack-series-pipeline-miriam-bug-report.png) simply tried to pass `output_1` to a node and both `output_2` and `output_3` to another. The same Pipeline managed to surface an incredible amount of other corner cases: we eventually opened three complex issues from the pipeline in question.

Interestingly, Pipeline doesn't even notice there is a problem and does not fail. It does run, exactly as the drawing suggests: when the query happens to be in French, only the sparse retriever would process it.

Clearly this is not good for us.

Well, let's open an issue on Github and look for a workaround. Given that we're Haystack power-users by now, we realize that we can use a Join node with a single input as a no-op node: if we put it along one of the edges, the bug can be solved.

So here is our current Pipeline:

![Multilingual Hybrid Retrieval with No-Op Joiner](/posts/2023-10-13-haystack-series-pipeline-multilingual-hybrid-retrieval-with-noop.png)

```python
pipeline = Pipeline()
pipeline.add_node(component=language_classifier, name="LanguageClassifier", inputs=["Query"])
pipeline.add_node(component=translator, name="Translator", inputs=["LanguageClassifier.output_1"])
pipeline.add_node(component=sparse_retriever, name="SparseRetriever", inputs=["Translator", "LanguageClassifier.output_2"])
pipeline.add_node(component=no_op_join, name="NoOpJoin", inputs=["LanguageClassifier.output_1"])
pipeline.add_node(component=dense_retriever, name="DenseRetriever", inputs=["NoOpJoin", "LanguageClassifier.output_2"])
pipeline.add_node(component=join_documents, name="JoinDocuments", inputs=["SparseRetriever", "DenseRetriever"])
pipeline.add_node(component=rerank, name="Ranker", inputs=["JoinDocuments"])
pipeline.add_node(component=reader, name="Reader", inputs=["Ranker"])
```

Great news: the pipeline now runs as we expect! Trying for English queries shows exactly the same performance as before. However, in the moment when we run a French query, the results seems to be still much worse.

What now? Is the dense retriever still not running?!

Some debugging later we figure that now the Retrievers are not at fault. We forgot another piece of the puzzle: Ranker needs the query to be in the same language as the documents to work properly. It needs the query to be in English, just like the sparse retriever does.

But... how does the Pipeline passes the query down to the Ranker?

Up until this point we didn't need to know anything about how exactly values are passed from one component to the next. We didn't need to care about their inputs and outputs at all: Pipeline was doing all this dirty work for us. All of a sudden we are in the weird situation where we need to control this process and explicitly tell the pipeline which query to pass to the Ranker, and we have no idea of how to do that.

Worse yet. There is *no way* to reliably do that. 

The documentation seems to blissfully ignore the topic, docstrings gives us no pointers, and looking at [the routing code of Pipeline](https://github.com/deepset-ai/haystack/blob/aaee03aee87e96acd8791b9eff999055a8203237/haystack/pipelines/base.py#L483) we quickly get dizzy and cut the chase. We scour the Pipeline API in all details until we're certain that there's nothing that can help.

Well, there must be at least some workaround. Maybe we can forget about this issue by rearranging the nodes?

One easy way out is that we could translate the query for both retrievers instead of doing so only for the sparse one. This solution also gets rid of the NoOpJoin node, so it doesn't sound too bad.

The pipeline looks like this now.

![Multilingual Hybrid Retrieval with two Translators](/posts/2023-10-13-haystack-series-pipeline-multilingual-hybrid-retrieval-two-translators.png)

We happen to have two nodes now that contain identical translator components. Given that they are stateless, surely I can place the same instance in both places, with different names, and avoid doubling its memory footprint just to workaround a couple of Pipeline bugs. After all, Translator nodes use relatively heavy models for machine translation.

This is what Pipeline replies to us as soon as we try.

```
PipelineConfigError: Cannot add node 'Translator2'. You have already added the same 
instance to the pipeline under the name 'Translator'.
```

Ok, so it seems like we can't re use components in two places: there is an explicit check against this, for some reason. Alright, let's rearrange *again* this pipeline with this new constraint in mind.

How about we first translate the query and then distribute it?

![Multilingual Hybrid Retrieval, translate-and-distribute](/posts/2023-10-13-haystack-series-pipeline-multilingual-hybrid-retrieval-translate-and-distribute.png)

```python
pipeline = Pipeline()
pipeline.add_node(component=language_classifier, name="LanguageClassifier", inputs=["Query"])
pipeline.add_node(component=translator, name="Translator", inputs=["LanguageClassifier.output_1"])
pipeline.add_node(component=sparse_retriever, name="SparseRetriever", inputs=["Translator", "LanguageClassifier.output_2"])
pipeline.add_node(component=dense_retriever, name="DenseRetriever", inputs=["Translator", "LanguageClassifier.output_2"])
pipeline.add_node(component=join_documents, name="JoinDocuments", inputs=["SparseRetriever", "DenseRetriever"])
pipeline.add_node(component=rerank, name="Ranker", inputs=["JoinDocuments"])
pipeline.add_node(component=reader, name="Reader", inputs=["Ranker"])
```

Nothing. The query is still in French, untranslated. Having wasted far too much time on this relatively simple pipeline, we throw the towel, go to Haystack's Discord server and cry for help.

As with most community questions regarding "advanced" Pipelines, I would normally be summoned to reply, and I would promise you a workaround asap.

The workaround, in fact, exists. But it's not pretty.

![Multilingual Hybrid Retrieval, working version](/posts/2023-10-13-haystack-series-pipeline-multilingual-hybrid-retrieval-workaround.png)

```python
pipeline = Pipeline()
pipeline.add_node(component=language_classifier, name="LanguageClassifier", inputs=["Query"])
pipeline.add_node(component=translator_workaround, name="TranslatorWorkaround", inputs=["LanguageClassifier.output_2"])
pipeline.add_node(component=sparse_retriever, name="SparseRetriever", inputs=["LanguageClassifier.output_1", "TranslatorWorkaround"])
pipeline.add_node(component=dense_retriever, name="DenseRetriever", inputs=["LanguageClassifier.output_1", "TranslatorWorkaround"])
pipeline.add_node(component=join_documents, name="JoinDocuments", inputs=["SparseRetriever", "DenseRetriever"])
pipeline.add_node(component=join_query_workaround, name="JoinQueryWorkaround", inputs=["TranslatorWorkaround", "JoinDocuments"])
pipeline.add_node(component=rerank, name="Ranker", inputs=["JoinQueryWorkaround"])
pipeline.add_node(component=reader, name="Reader", inputs=["Ranker"])
```

Note that you need two custom nodes: a wrapper for the translator and a brand new Join node.

```python
class TranslatorWorkaround(TransformersTranslator):

    outgoing_edges = 1

    def run(self, query):
        results, edge = super().run(query=query)
        return {**results, "documents": [] }, "output_1"

    def run_batch(self, queries):
        pass


class JoinQueryWorkaround(JoinNode):

    def run_accumulated(self, inputs, *args, **kwargs):
        return {"query": inputs[0].get("query", None), "documents": inputs[1].get("documents", None)}, "output_1"

    def run_batch_accumulated(self, inputs):
        pass

```

Wanna see this beauty in action? Have a look at this notebook.

Having learned only that it's better not to try to implement too complicated branching patterns with Haystack unless you work with them 8 hours a day, let's now turn to the indexing side of your application. We'll try to stick to the basics this time.

## Indexing Pipelines

Indexing pipelines' main goal is to transform files into Documents that a query pipeline can later retrieve information from. They mostly look like the following.

![Indexing Pipeline](/posts/2023-10-13-haystack-series-pipeline-indexing-pipeline.png)

And the code looks just like how you would expect it. 

```python
pipeline = Pipeline()
pipeline.add_node(component=file_type_classifier, name="FileTypeClassifier", inputs=["File"])
pipeline.add_node(component=text_converter, name="TextConverter", inputs=["FileTypeClassifier.output_1"])
pipeline.add_node(component=pdf_converter, name="PdfConverter", inputs=["FileTypeClassifier.output_2"])
pipeline.add_node(component=docx_converter, name="DocxConverter", inputs=["FileTypeClassifier.output_4"])
pipeline.add_node(component=join_documents, name="JoinDocuments", inputs=["TextConverter", "PdfConverter", "DocxConverter"])
pipeline.add_node(component=preprocessor, name="Preprocessor", inputs=["JoinDocuments"])
pipeline.add_node(component=document_store, name="DocumentStore", inputs=["Preprocessor"])

pipeline.run(file_paths=paths)
```
No big surprises: there's a File starting node instead of Query, which seems totally logical given that this pipeline expects a list of files, not a query. All very intuitive.

Indexing pipelines are run by giving them a list of paths that points to the files to convert. As we know that in this scenario more than one Converter may run, there is a Join node before the PreProcessor to make sense of the merge. We make sure that the directory contains only files that we can convert, in this case .txt, .pdf and .docx, and then we run the code above.

The code, however, fails.

```
ValueError: Multiple non-default file types are not allowed at once.
```



.

.

.

.

.

.

.








This is where the magic starts to kick in.

If you observe the two pipelines carefully you'll notice that they seem to behave differently. We need a Join node in the first case, but we don't need it in the second. It seems like the Pipeline knows already that in the first both Retrievers will run, while in the second only one will. But how does it know it?

In code there is no evident lead. We did not communicate to the first Pipeline that both Retriever have to run, neither we specified that in the second only one will. It seems like Pipeline just *knows*.


.

.

.




## Connecting New Components

This abstraction is extremely powerful for the usecases that it was designed for. There are a few layers of ease of use versus customization the user can choose from depending on their expertise, which help them progress from a simple ready-made Pipeline to fully custom graphs. 

However, the focus was oriented so much on the initial stages of the user's journey that the needs of power-users were often forgotten. Such issues didn't show immediately for users that stick to simple ready-made pipelines and well-known use cases, but quickly added friction as soon as they tried to customize their system further.

For example, let's imagine we put together this non-sensical Pipeline.

```python
p = Pipeline()
p.add_node(component=reader, name="Reader", inputs=["Query"])
p.add_node(component=retriever, name="Retriever", inputs=["Reader"])
```

A user that knows what the two components do sees immediately that this Pipeline is meaningless. However, Haystack won't raise any exception when this is done, and the code runs successfully. You can even `draw()` it.

![Swapper Retriever/Reader Pipeline](/posts/2023-10-13-haystack-series-pipeline-swapped-retriever-reader.png)

Alright, so what happens when we run it? It must fail, right?

```python
res = p.run(query="What did Einstein work on?")
```



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

*Previous: [Haystack 2.0 - Why rewriting Haystack?!](/posts/2023-10-10-haystack-series-why)*

*See the entire series here: [Haystack 2.0 series](/series/haystack-2.0-series/)*
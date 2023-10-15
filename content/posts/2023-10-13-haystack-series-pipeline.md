---
title: "Haystack's Pipeline"
date: 2023-10-13
author: "ZanSara"
tags: ["Haystack 2.0", Haystack, NLP, Python, Pipeline, DAG, graph, "API Design", "Semantic Search", "Hybrid Retrieval"]
series: ["Haystack 2.0 Series"]
featuredImage: "/posts/2023-10-13-haystack-series-pipeline.png"
draft: true
---

If you've ever looked at Haystack before you've surely met with the concept of Pipeline. Pipelines are one of the most prominent concepts of the framework and may have even inspired LangChain's chains, for what we know.

However, the Pipeline abstraction is by no means an obvious choice when it comes to NLP frameworks. Why did we adopt this concept, and what does it bring us? 

In this post I am going to go into all the details of how Pipelines work in Haystack now, why they work this way, and what are its strenghts and weaknesses. This deep dive into the current state of the framework is also a premise to for my next post, where I am going to explain how Haystack 2.0 addresses this version's shortcomings.

If you think you already know how Haystack Pipelines work, give this post a chance: I might manage to change your mind.

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

Note how the very first information given about this component is *where to place it*. Right after, it does specify what are its inputs and outputs, even though it's not immediately clear why we need this information, and then lists which specific classes can cover the role of a Ranker. 

The message is clear: all Ranker classes are functionally interchangeable and, as long as you place them correctly in the pipeline, they are going to fulfill the function of Ranker as you expect them to. Users don't need to understand what distinguishes `CohereRanker` from `RecentnessReranker` unless they want to: the documentation promises that you can swap them safely, and thanks to the Pipeline abstraction, this statement holds true for the majority of cases.

## Ready-made Pipelines

But how can the users know which sort of graph they have to build?

Most NLP applications are made by a fairly limited number of high-level components: Retriever, Readers, Rankers, plus the occasional filter, translator, summarizer or query classifier. Systems requiring more than these components used to be really rare, at least when talking about "query" pipelines (more on this later).

Therefore, at this level of abstraction there are just a few graph topologies possible, and better yet, they could each be mapped to a high-level usecases such as semantic search, language-agnostic document search, hybrid retrieval, and so on

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

## "Flexibility powered by DAGs"

This abstraction is extremely powerful for the usecases that it was designed for. There are a few layers of ease of use versus customization the user can choose from depending on their expertise, which help them progress from a simple ready-made Pipeline to fully custom graphs. 

However, the focus was oriented so much on the initial stages of the user's journey that the needs of power-users were sometimes forgotten. Such issues didn't show immediately, but quickly added friction as soon as the users tried to customize their system beyond the examples contained in the tutorials and in the documentation.

For an example of these issues, let's talk about pipelines with branches. Here are two small, apparently very similar pipelines.

![Query Classification vs Hybrid Retrieval](/posts/2023-10-13-haystack-series-pipeline-branching-query-pipelines.png)

The first pipeline represents the Hybrid Retrieval usecase we've met with before. Here, the Query node sends its outputs to both retrievers and they both produce some output. Therefore, in order for the reader to make sense of this data, we need to have a Join node which merges the two lists into one, and then a ranker which takes the lists, sorts them again by similarity to the query, and sends the re-arranged list to the reader.

The second pipeline instead performs a simpler form of Hybrid Retrieval. Here the Query node sends its outputs to a Query Classifier, which then triggers only one of the two retrievers, the one that is expected to perform better on it. The triggered retriever that run then sends its output directly to reader, which doesn't need to be aware of which retriever the data comes from. So in this case we don't need the Join node.

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

Here is how the Pipeline ends up looking like. Language Classifier sends all French queries over `output_1`, and all English queries over `output_2`. In this way, they queries will pass throught the Translator node only if it was written in French.

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

But... wait. Let's look again at the graph, and at the code. DenseRetriever should be receiving *two* inputs from Language Classifier: both `output_1` and `output_2`, because it can handle both languages. Whats going on? Is this a bug in `draw()`?

Thanks to the `debug=True` parameter of `Pipeline.run()`, we start inspecting what each node saw during the execution, and we realize quickly that our worst fears are true: this is a bug in the Pipeline implementation. The underlying library powering the pipeline's graphs takes the definition of Directed Acyclic Graphs very seriously, and does not allow two nodes to be connected by more than one edge. There are, of course, other graph classes supporting this case, but Haystack happens to use the wrong one.

Interestingly, Pipeline doesn't even notice there is a problem and does not fail. It does run, exactly as the drawing suggests: when the query happens to be in French, only the sparse retriever would process it.

> Trivia

> This issue was discovered by our own Solutions Engineering team which, unsurprisingly, was building a Pipeline a bit more complex than the tutorials'. [Their pipeline](/posts/2023-10-13-haystack-series-pipeline-miriam-bug-report.png) simply tried to pass `output_1` to a node and both `output_2` and `output_3` to another. For some reason, we never saw any contributor report this issue on GitHub, even if the bug has been there since the inception of Pipeline.

Clearly this is not good for us.

Well, let's look for a workaround. Given that we're Haystack power-users by now, we realize that we can use a Join node with a single input as a "no-op" node: if we put it along one of the edges, that edge won't be connecting Language Classifier and Dense Retriever directly, so the bug should be solved.

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

Great news: the pipeline now runs as we expect! However, in the moment when we run a French query, the results are a bit better, but still are still quite bad.

What now? Is the dense retriever still not running? Is the Translation node doing a poor job?

Some debugging later we realize that the Translator is amazingly good and the Retrievers are both running. But we forgot another piece of the puzzle: Ranker needs the query to be in the same language as the documents to work properly. It needs the query to be in English, just like the sparse retriever does. Right now is receiving the original French query, and that's the reason for the lack of performance. We soon realize that this is very important also for the Reader.

So... how does the Pipeline passes the query down to the Ranker?

Up until this point we didn't need to know anything about how exactly values are passed from one component to the next. We didn't need to care about their inputs and outputs at all: Pipeline was doing all this dirty work for us. All of a sudden we are in the weird situation where we need to control this process, to explicitly tell the pipeline which query to pass to the Ranker, and we have no idea of how to do that.

Worse yet. There is *no way* to reliably do that. 

The documentation seems to blissfully ignore the topic, docstrings gives us no pointers, and looking at [the routing code of Pipeline](https://github.com/deepset-ai/haystack/blob/aaee03aee87e96acd8791b9eff999055a8203237/haystack/pipelines/base.py#L483) we quickly get dizzy and cut the chase. We dig through the Pipeline API several times until we're certain that there's nothing that can help.

Well, there must be at least some workaround. Maybe we can forget about this issue by rearranging the nodes.

One easy way out is that we could translate the query for both retrievers instead of doing so only for the sparse one. This solution also gets rid of the NoOpJoin node we introduced earlier, so it doesn't sound too bad.

The pipeline looks like this now.

![Multilingual Hybrid Retrieval with two Translators](/posts/2023-10-13-haystack-series-pipeline-multilingual-hybrid-retrieval-two-translators.png)

```python
pipeline = Pipeline()
pipeline.add_node(component=language_classifier, name="LanguageClassifier", inputs=["Query"])
pipeline.add_node(component=translator, name="Translator", inputs=["LanguageClassifier.output_1"])
pipeline.add_node(component=sparse_retriever, name="SparseRetriever", inputs=["Translator", "LanguageClassifier.output_2"])
pipeline.add_node(component=translator_2, name="Translator2", inputs=["LanguageClassifier.output_1"])
pipeline.add_node(component=dense_retriever, name="DenseRetriever", inputs=["Translator2", "LanguageClassifier.output_2"])
pipeline.add_node(component=join_documents, name="JoinDocuments", inputs=["SparseRetriever", "DenseRetriever"])
pipeline.add_node(component=rerank, name="Ranker", inputs=["JoinDocuments"])
pipeline.add_node(component=reader, name="Reader", inputs=["Ranker"])
```

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

Looks neat, but nothing has changed. The query received by Ranker is still in French, untranslated. Shuffling the order of the `add_node` calls and the names of the components in the `inputs` parameters seems to have no effect on the graph. We even try to connect directly Translator with Ranker in a desperate attempt to forward the correct value, but Pipeline at this point starts throwing obscure, apparently meaningless error messages like:

```
BaseRanker.run() missing 1 required positional argument: 'documents'
```

Isn't Ranker receiving the documents from JoinDocuments? Where did they go?

Having wasted far too much time on this relatively simple pipeline, we throw the towel, go to Haystack's Discord server and ask for help.

Soon enough one of the maintainers would show up, promising a workaround asap. You're skeptical at this point, but the workaround, in fact, exists. 

It's just not very pretty.

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

Wanna play with this pipeline yourself? [Colab](https://drive.google.com/file/d/18Gqfd0O828T71Gc-IHeU4v7OXwaPk7Fc/view?usp=sharing), [gist](https://gist.github.com/ZanSara/33020a980f2f535e2529df4ca4e8f08a).

Along with this beautiful code, we also receive an explanation about how the JoinQueryWorkaround will work only for this specific pipeline and is pretty hard to generalize, which is the reason why it's not present in Haystack right now. I'll now spare you the details: you will have an idea why by the end of this journey.

Having learned only that it's better not to try to implement unusual branching patterns with Haystack unless you're ready for a fight, let's now turn to the indexing side of your application. We'll stick to the basics this time.

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
No surprising stuff here. The starting node is File instead of Query, which seems totally logical given that this pipeline expects a list of files, not a query. All very intuitive.

Indexing pipelines are run by giving them a list of paths that points to the files to convert. As we know that in this scenario more than one Converter may run, there is a Join node before the PreProcessor to make sense of the merge. We make sure that the directory contains only files that we can convert, in this case .txt, .pdf and .docx, and then we run the code above.

The code, however, fails.

```
ValueError: Multiple non-default file types are not allowed at once.
```

The more we look at the error, the less it makes sense. What are non-default file types? Why are they not allowed at once, and and what can I do to fix that?

We head for the documentation, were we find an interesting lead.

![`FileTypeClassifier documentation`](/posts/2023-10-13-haystack-series-pipeline-filetypeclassifier-docs.png)

So it seems like the File Classifier can only process the files if they're all of the same type.

After all we've been through with the Hybrid Retrieval pipelines, this sounds wrong. We know that Pipeline can run two branches at the same time, we've been doing it all the time just a moment ago. Why FileTypeClassifier can't send data to two different converters just like LanguageClassifier was sending data to two different retrievers?

Turns out, this is *not* the same thing. 

Let's compare the three pipelines side by side and try to spot the difference.

![All branching pipelines, side by side](/posts/2023-10-13-haystack-series-pipeline-all-branching-pipelines.png)

In the first case, Query sends the same identical value to both Retrievers. So from the component's perspective, there's a single output being produced: the Pipeline takes care of copying it for all nodes that are connected to it.

In the second case, QueryClassifier can send the query to either Retriever, but never to both of them. So the component can produce two different outputs, but at every point in time it will always produce just one of them.

In the third case, FileTypeClassifier may need to return two different outputs in the same time, for example one with a list of TXT files, and one with a list of PDF. And it turns out this can't be done. This is, unfortunately, a well-known limitation of the Pipeline/BaseComponent API design. 
The output of a component is defined as a tuple, `(output values, output_edge)`, and nodes can't produce a list of these tuples to send different values to different nodes. 

That's the end of the story. This time, there is just no workaround: you need to pass the files one by one, or forget about using a Pipeline for this task.

## Validation

On top of these challenges there are other interesting tradeoffs that needed to be made in order for the API to look so simple at a first impact. One of this is connections validation.

Let's imagine we quickly skimmed through a tutorial and got one bit of information wrong: we mistakenly believe that in an Extractive QA Pipeline, you need to place a Reader in front of a Retriever. So we sit down and write this.

```python
p = Pipeline()
p.add_node(component=reader, name="Reader", inputs=["Query"])
p.add_node(component=retriever, name="Retriever", inputs=["Reader"])
```

Up to this point, running the script raises no error. Haystack is happy to connect these two in this order. You can even `draw()` this Pipeline just fine.

![Swapper Retriever/Reader Pipeline](/posts/2023-10-13-haystack-series-pipeline-swapped-retriever-reader.png)

Alright, so what happens when we run it?

```python
res = p.run(query="What did Einstein work on?")
```
```
BaseReader.run() missing 1 required positional argument: 'documents'
```

This is the same error we've seen in the translating hybrid retrieval pipeline from before, but fear not! Here we can simply obey the error message by doing:

```python
res = p.run(query="What did Einstein work on?", documents=document_store.get_all_documents())
```

And to our surprise, this pipeline doesn't crash. It just hangs there, showing an insanely slow progress bar assuring us that some inference is in progress. A few hours later, we kill the process and consider switching to another framework, because this one is clearly dog slow.

What happened?

The cause of this issue is the same that makes connecting Haystack components in a Pipeline so effortless, and it's related to the way components and Pipeline communicate. If you check `Pipeline.run()`'s signature, you'll see that it looks like:


```python
def run(
    self,
    query: Optional[str] = None,
    file_paths: Optional[List[str]] = None,
    labels: Optional[MultiLabel] = None,
    documents: Optional[List[Document]] = None,
    meta: Optional[Union[dict, List[dict]]] = None,
    params: Optional[dict] = None,
    debug: Optional[bool] = None,
):
```

which mirrors almost exactly `BaseComponent`'s, the base class nodes have to inherit from.

```python
@abstractmethod
def run(
    self,
    query: Optional[str] = None,
    file_paths: Optional[List[str]] = None,
    labels: Optional[MultiLabel] = None,
    documents: Optional[List[Document]] = None,
    meta: Optional[dict] = None,
) -> Tuple[Dict, str]:
```

This match means two things:

- Every component can be connected to every other, because the inputs of all of them look exactly the same.

- It's impossible to tell if it makes sense to connect two components, because their interfaces match regardless.

Take this with a grain of salt: the actual implementation is far more nuanced that what I just showed you, but the problem is fundamentally this: that components are trying to be as compatible as possible to all others and they have no way to signal, to the Pipeline or to the users, that they're meant to be connected only to some nodes and not to others.

Components also often take inputs that they don't use. A Ranker only needs documents, so all the other inputs required by the run method signature go unused. What do components do with the values? It depends: 

- Some have them in the signature, and forward them unchanged.
- Some have them in the signature, and don't forward them.
- Some don't have them in the signature, breaking the inheritance pattern, and Pipeline reacts by just assuming that they should be added unchanged to the output dictionary.

If you check closely the two workaround nodes for the Hybrid Retrieval pipeline we tried to build before, you'll notice the fix entirely focuses on altering the routing of the unused parameters `query` and `documents` to make the pipeline behave in the way the user expects. However, this behavior does not generalize: a different pipeline would require a different behavior, which is the reason why the components behave differently to begin with.


## Wrapping up

Along this journey into the guts of Haystack Pipelines we've seen at the same time some really beautiful API and the ugly consequences of their implementation. As always, there's no free lunch: trying to over-simplify the interface is going to bite as soon as the usecases become non trivial.

However, we believe that this concept has a huge potential, and that this version of Pipeline can be improved a lot before the impact on the API becomes too heavy. In Haystack 2.0, armed with the experience we gained working with this implementation of Pipeline, we re-implemented it in a fundamentally different way, while striving to keep its API close to the ones of its predecessor.

In the next post we're going to see how.

---

*Next: Soon!*

*Previous: [Why rewriting Haystack?!](/posts/2023-10-11-haystack-series-why)*

*See the entire series here: [Haystack 2.0 series](/series/haystack-2.0-series/)*
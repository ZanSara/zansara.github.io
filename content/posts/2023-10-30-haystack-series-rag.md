---
title: "RAG Pipelines of all shapes and forms"
date: 2023-10-30
author: "ZanSara"
tags: ["Haystack 2.0", Haystack, NLP, Python, LLM, GPT, "Retrieval Augmentation", RAG, "Semantic Search"]
series: ["Haystack 2.0 Series"]
featuredImage: "/posts/2023-10-30-haystack-series-rag/cover.png"
draft: true
# canonicalUrl: https://haystack.deepset.ai/blog/rag-pipelines-of-all-shapes-and-forms
---
<small>*[The Republic of Rose Island, Wikipedia](https://it.wikipedia.org/wiki/File:Isoladellerose.jpg)*</small>


Since the start of this series one use case that I constantly brought up is Retrieval Augmented Generation, or RAG for short.

RAG is quickly becoming a key technique to make LLMs more reliable and effective at answering any sort of question, regardless how specific, so it's crucial for Haystack to enable it.

Let's see how to build such applications with Haystack 2.0, starting from a very basic call to an LLM to a fully fledged, production-ready RAG pipeline that scales. We are going to end up with a RAG application that can answers all your questions about countries of the world.

# What is RAG?

The idea of Retrieval Augmented Generation was first defined in a [paper](https://arxiv.org/abs/2005.11401) by Meta in 2020. It was designed to solve a few of the inherent limitations of seq2seq models (language models that, given a sentence, can finish writing it for you), such as:

- Their internal knowledge, for as vast as it may be, will always be limited and at least slightly out of date.
- They work best on generic topics, rather than niche and specific areas, unless they're fine-tuned on purpose, which is a very expensive and slow process.
- Even when they have subject-matter expertise, they tend to "hallucinate": they confidently produce false statements backed by apparently solid reasoning.
- They cannot reliably cite their sources or tell where their knowledge comes from, which makes fact-checking their replies non trivial.

RAG solves these issues of "grounding" the LLM to reality by providing some relevant, up-to-date and trusted information to the model together with the question. In this way the LLM doesn't need to draw information from its internal knowledge, but it can base its replies on the snippets provided by the user.

![RAG Paper diagram](/posts/2023-10-30-haystack-series-rag/rag-paper-image.png)

As you can see in the image above (taken directly from the original paper), a system such as RAG is made of two parts: one that finds text snippets that are relevant to the question asked by the user, and a generative model, usually an LLM, that rephrases the snippets into a coherent answer for the question.

Let's build one of these with Haystack 2.0! 

{{< notice info >}} *All these code snippets were tested against `haystack-ai==0.105.0`. Haystack 2.0 is still unstable, so later versions of this package might introduce breaking change without any notice until Haystack 2.0 is officially released.* {{< /notice >}}

# Generators: Haystack's LLM components

As every NLP framework that deserves its name, Haystack supports LLMs in different ways. The easiest way to query an LLM in Haystack 2.0 is through a Generator component: depending on which LLM and the way you intend to query it (chat, text completion, etc...) you should pick the appropriate class.

We're going to use ChatGPT for these examples, so the component we need is [`GPTGenerator`](https://github.com/deepset-ai/haystack/blob/main/haystack/preview/components/generators/openai/gpt.py). Here is all the code needed to use it to query OpenAI's ChatGPT:

```python
from haystack.preview.components.generators.openai.gpt import GPTGenerator

generator = GPTGenerator(api_key=api_key)
generator.run(prompt="What's the official language of France?")
# returns {"replies": ['The official language of France is French.']}
```
You can select your favourite OpenAI model by specifying a `model_name` at initialization, for example `gpt-4`. It also supports specifying an `api_base_url`, for private deployments, a `streaming_callback` if you want to see the output generated live in the terminal, and optional `kwargs` to let you pass whatever other parameter the model understands, such as the number of answers (`n`), the temperature (`temperature`), etc.

Note that in this case we're passing the API key to the component's constructor. This is unnecessary: `GPTGenerator` is able to read the value from the `OPENAI_API_KEY` environment veriable, and also from the `api_key` module variable of [`openai`'s SDK](https://github.com/openai/openai-python#usage).

Right now Haystack supports HuggingFace models through the [`HuggingFaceLocalGenerator`](https://github.com/deepset-ai/haystack/blob/f76fc04ed05df7b941c658ba85adbf1f87723153/haystack/preview/components/generators/hugging_face/hugging_face_local.py#L65) component, and many more LLMs are coming soon.


# PromptBuilder: structured prompts from templates

Let's imagine that our LLM-powered chatbot comes also with a set of pre-defined questions that the user can just select instead of typing in full. For example, instead of asking them to type `What's the official language of France?`, we let them select `Tell me the official languages` from a list, and they simply need to type "France" (or "Wakanda", for a change - our chatbot needs some challenges too).

In this scenario we have two pieces of the prompt: a variable (the country name, like "France") and a prompt template, which in this case is `"What's the official language of {{ country }}?"`

Haystack offers a component that is able to render variables into prompt templates: it's called [`PromptBuilder`](https://github.com/deepset-ai/haystack/blob/main/haystack/preview/components/builders/prompt_builder.py). As the generators we've seen before, also `PromptBuilder` is nearly trivial to initialize and use.

```python
from haystack.preview.components.builders.prompt_builder import PromptBuilder

prompt_builder = PromptBuilder(template="What's the official language of {{ country }}?")
prompt_builder.run(country="France")
# returns {'prompt': "What's the official language of France?"}
```

Note how we defined a variable, `country`, by wrapping its name in double curly brackets. PromptBuilder lets you define any input variable by just wrapping it that way: if the prompt template was `"What's the official language of {{ nation }}?"`, the `run()` method of `PromptBuilder` would have expected a `nation` input.


This syntax comes from [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/intro/), a popular templating library for Python. If you used Flask, Django, or Ansible, you will feel at home with `PromptBuilder`. If instead you never heard of any of these libraries before, you can check out the [syntax](https://jinja.palletsprojects.com/en/3.0.x/templates/) on Jinja's documentation. Jinja is extremely powerful and offers way more features than you'll ever need in prompt templates, ranging from simple if statements and for loops to object access through dot notation, full nesting of templates, variables manipulation, macros, and more.

# A Simple Generative Pipeline

With these two components we can already assemble a minimal Pipeline, to see how they work together. Connecting them is trivial: `PromptBuilder` generates a `prompt` output, and `GPTGenerator` expects an input with the exact same name and type.

```python
from haystack.preview import Pipeline
from haystack.preview.components.generators.openai.gpt import GPTGenerator
from haystack.preview.components.builders.prompt_builder import PromptBuilder

pipe = Pipeline()
pipe.add_component("prompt_builder", PromptBuilder(template="What's the official language of {{ country }}?"))
pipe.add_component("llm", GPTGenerator(api_key=api_key))
pipe.connect("prompt_builder", "llm")

pipe.run({"prompt_builder": {"country": "France"}})
# returns {"llm": {"replies": ['The official language of France is French.'] }}
```

Here is the pipeline graph:

![Simple LLM pipeline](/posts/2023-10-30-haystack-series-rag/simple-llm-pipeline.png)

# Make the LLM cheat

Building the Generative part of a RAG application was very simple! However, so far we only provided the question to the LLM, but no information to base its answers from. Nowadays LLMs possess a lot of general knowledge, so questions about famous countries such as France or Germany are easy for them to reply correctly. However, some users may be interested in knowing more about obscure or defunct microstates which don't exist anymore: in this case, ChatGPT is unlikely to answer correctly.

For example, let's ask our Pipeline something *really* obscure.

```python
pipe.run({"prompt_builder": {"country": "the Republic of Rose Island"}})
# returns {
#     "llm": {
#         "replies": [
#             'The official language of the Republic of Rose Island was Italian.'
#         ]
#     }
# }
```

The answer is an educated guess, but is not accurate: although it was located just outside of Italy's territorial waters, the official language of this short-lived [micronation](https://en.wikipedia.org/wiki/Republic_of_Rose_Island) was Esperanto.

How can we get ChatGPT to reply to such a question properly? One way is to make it "cheat" by providing the answer as part of the question. In fact, `PromptBuilder` is designed to serve exactly this usecase.

Here is our new, more advanced prompt:

```text
Given the following information, answer the question.
Context: {{ context }}
Question: {{ question }}
```

Let's build a new pipeline using this prompt!

```python
context_template = """
Given the following information, answer the question.
Context: {{ context }}
Question: {{ question }}
"""
language_template = "What's the official language of {{ country }}?"

pipe = Pipeline()
pipe.add_component("context_prompt", PromptBuilder(template=context_template))
pipe.add_component("language_prompt", PromptBuilder(template=language_template))
pipe.add_component("llm", GPTGenerator(api_key=api_key))
pipe.connect("language_prompt", "context_prompt.question")
pipe.connect("context_prompt", "llm")

pipe.run({
    "context_prompt": {"context": "Rose Island had its own government, currency, post office, and commercial establishments, and the official language was Esperanto."}
    "language_prompt": {"country": "the Republic of Rose Island"}
})
# returns {
#     "llm": {
#         "replies": [
#             'The official language of the Republic of Rose Island is Esperanto.'
#         ]
#     }
# }
```
Let's look at the graph of our Pipeline:

![Double PromptBuilder pipeline](/posts/2023-10-30-haystack-series-rag/double-promptbuilder-pipeline.png)

The beauty of `PromptBuilder` lays in its flexibility: they allow users to chain instances together to assemble complex prompts from simpler schemas: for example, here we use the output of the first `PromptBuilder` as the value of `question` in the second prompt.

However, in this specific scenario we can build a simpler system by merging the two prompts into a single one.

```text
Given the following information, answer the question.
Context: {{ context }}
Question: What's the official language of {{ country }}?
```

If we use this prompt, the resulting system becomes again really straightforward.

```python
template = """
Given the following information, answer the question.
Context: {{ context }}
Question: What's the official language of {{ country }}?
"""
pipe = Pipeline()
pipe.add_component("prompt_builder", PromptBuilder(template=template))
pipe.add_component("llm", GPTGenerator(api_key=api_key))
pipe.connect("prompt_builder", "llm")

pipe.run({
    "prompt_builder": {
        "context": "Rose Island had its own government, currency, post office, and commercial establishments, and the official language was Esperanto.",
        "country": "the Republic of Rose Island"
    }
})
# returns {
#     "llm": {
#         "replies": [
#             'The official language of the Republic of Rose Island is Esperanto.'
#         ]
#     }
# }
```

![PromptBuilder with two inputs pipeline](/posts/2023-10-30-haystack-series-rag/double-variable-promptbuilder-pipeline.png)


# Retrieving the context

For now we've been playing with prompts, but the fundamental question remains unanswered: where do we get the correct text snippet for the question the user is asking? We can't expect such information as part of the input: we need our system to be able to fetch this information independently, based uniquely on the query. Thankfully, retrieving relevant information from large [corpora](https://en.wikipedia.org/wiki/Text_corpus) (a technical term for large collections of data, usually text) is a task that Haystack excels at since its inception.

The components that perform this task is called a [Retriever](https://docs.haystack.deepset.ai/docs/retriever) (watch out: at the time of writing, the documentation still refers to Haystack 1.x components). Retrieval can be performed on different data sources: to begin, let's assume we're searching for data into a local database, which is the use case that most Retrievers are geared towards.

So, to begin with, let's create a small local database where we are going to store a bunch of information about some European countries. Haystack offers a neat toy object for these small scale demos: `InMemoryDocumentStore`. This document store is little more than a Python dictionary under the hood, but provides the same exact API as much more powerful data stores and vector stores, such as [Elasticsearch](https://github.com/deepset-ai/haystack-core-integrations/pull/41) or [ChromaDB](https://haystack.deepset.ai/integrations/chroma-documentstore). Keep in mind that the object is called "Document Store", and not simply "datastore", because what it stores is Haystack's Document objects: a small dataclass that helps other components make sense of the data that they receive.

So, let's initialize an `InMemoryDocumentStore` and write some `Documents` into it.

```python
from haystack.preview.dataclasses import Document
from haystack.preview.document_stores import InMemoryDocumentStore

documents = [
    Document(text="German is the the official language of Germany."), 
    Document(text="The capital of France is Paris, and its official language is French."),
    Document(text="Italy recognizes a few official languages, but the most widespread one is Italian."),
    Document(text="Esperanto has been adopted as official language for some microstates as well, such as the Republic of Rose Island, a short-lived microstate built on a sea platform in the Adriatic Sea.")
]
docstore = InMemoryDocumentStore()
docstore.write_documents(documents=documents)

docstore.filter_documents()
# returns [
#     Document(text="German is the the official language of Germany."), 
#     Document(text="The capital of France is Paris, and its official language is French."),
#     Document(text="Esperanto has been adopted as official language for some microstates as well, such as the Republic of Rose Island, a short-lived microstate built on a sea platform in the Adriatic Sea."),
#     Document(text="Italy recognizes a few official languages, but the most widespread one is Italian."),
# ]
```

Once the Document Store is set up, we can initialize a Retriever. In Haystack 2.0 each Document Store comes with its own set of highly optimized Retrievers: `InMemoryDocumentStore` offers two, one based on BM25 ranking, and one based on embedding similarity.

Let's start from the BM25-based retriever, which is slightly easier to set up. Let's first try to use it on its own, to see how it behaves.

```python
from haystack.preview.components.retrievers.memory_bm25_retriever import MemoryBM25Retriever

retriever = InMemoryBM25Retriever(document_store=docstore)
retriever.run(query="Rose Island", top_k=1)
# returns [
#     Document(text="Esperanto has been adopted as official language for some microstates as well, such as the Republic of Rose Island, a short-lived microstate built on a sea platform in the Adriatic Sea.")
# ]

retriever.run(query="Rose Island", top_k=3)
# returns [
#     Document(text="Esperanto has been adopted as official language for some microstates as well, such as the Republic of Rose Island, a short-lived microstate built on a sea platform in the Adriatic Sea.")
#     Document(text="Italy recognizes a few official languages, but the most widespread one is Italian."),
#     Document(text="The capital of France is Paris, and its official language is French."),
# ]
```

We see that `InMemoryBM25Retriever` accepts a few parameters. `query` is the question we want to find relevant documents for. In the case of BM25, the algorithm focuses entirely on keyword metching, so it cannot make sense of synonims and descriptions, but only exact words. It makes it very fast, but it doesn't fail gracefully when the keywords are not present in any document.

`top_k` instead controls the number of documents returned. We can see that in the first example, the correct document is returned, while in the second, once the Retriever ran out of relevant documents (i.e., documents that contain any keyword from the question), it just starts returning random ones until it reaches the required `top_k`. Although the behavior is not optimal, BM25 guarantees that if there was a documents that is relevant and with matching keyword, it will be in the first position, so for now we can use it.

Let's now make use of this new component in our Pipeline. 

# Our first RAG Pipeline

The Retriever does not return a single string, but a list of Documents: it's time to use Jinja's powerful syntax to do some unpacking on our behalf:

```text
Given the following information, answer the question.

Context: 
{% for document in documents %}
    {{ document.text }}
{% endfor %}

Question: What's the official language of {{ country }}?
```

Notice how, despite the slightly alien syntax for a Python programmer, what the template does is fairly evident: it iterates over the documents and, for each of them, renders their `text` field.

With all these pieces set up, we can finally put them all together:

```python
template = """
Given the following information, answer the question.

Context: 
{% for document in documents %}
    {{ document.text }}
{% endfor %}

Question: What's the official language of {{ country }}?
"""
pipe = Pipeline()

pipe.add_component("retriever", InMemoryBM25Retriever(document_store=docstore))
pipe.add_component("prompt_builder", PromptBuilder(template=template))
pipe.add_component("llm", GPTGenerator(api_key=api_key))
pipe.connect("retriever", "prompt_builder.documents")
pipe.connect("prompt_builder", "llm")

pipe.run({
    "prompt_builder": {
        "country": "the Republic of Rose Island"
    }
})
# returns {
#     "llm": {
#         "replies": [
#             'The official language of the Republic of Rose Island is Esperanto.'
#         ]
#     }
# }
```

![BM25 RAG Pipeline](/posts/2023-10-30-haystack-series-rag/bm25-rag-pipeline.png)

Congratulations! We've just built our first, true-to-its-name RAG Pipeline. Swap out `InMemoryDocumentStore` and `InMemoryBM25Retriever` with their Elasticsearch counterparts, which offer nearly identical API, and you have a system ready to scale up to real production workloads.

# Searching the web

A pipeline like this is very convenient if you need to perform RAG onto private data only. However, in many cases you may want to get data from the Internet as well, for example from news outlets, from documentation pages, and so on. To accomplish this goal, rather than a Retriever we need a Search Engine.

Haystack 2.0 already provides a search engine component called `SerperDevWebSearch`. It uses [SerperDev's API](https://serper.dev/) to query popular search engines and return two types of data: a list of text snippets, coming from the serach engine's preview boxes, and a list of links, which point to the top search results.








---

*Next: Soon!*

*Previous: [Canals: a new concept of Pipeline](/posts/2023-10-26-haystack-series-canals)*

*See the entire series here: [Haystack 2.0 series](/series/haystack-2.0-series/)*
---
title: "[DRAFT] Embedding Retrieval"
date: 2023-10-29
author: "ZanSara"
tags: ["Haystack 2.0", Haystack, NLP, Python, LLM, "Retrieval Augmentation", RAG, "indexing", "Document Store", Embeddings]
series: ["Haystack 2.0 Series"]
featuredImage: "/posts/2023-11-xx-haystack-series-minimal-indexing/cover.png"
draft: true
# canonicalUrl: https://haystack.deepset.ai/blog/....
---
<small>*[The Republic of Rose Island, Wikipedia](https://it.wikipedia.org/wiki/Isola_delle_Rose)*</small>

In the previous post of the Haystack 2.0 series we've seen how to build RAG pipelines using a generator, a prompt builder and a retriever with its document store. However, the content of our document store wasn't exactly extensive, and populating one with clean, properly formatted data may seem like a daunting task.

In this post I will show you how to use Haystack 2.0 to populate a document store that you can then use for retrieval.

{{< notice info >}}

💡 *Do you want to see the code in action? Check out the [Colab notebook](https://drive.google.com/file/d/1cM1M61VBIWcIkulCpM9uTdObid2Vj47G/view?usp=sharing) or the [gist](#).*

{{< /notice >}}

{{< notice warning >}}

<i>⚠️ **Warning:**</i> *This code was tested on `haystack-ai==0.117.0`. Haystack 2.0 is still unstable, so later versions might introduce breaking changes without notice until Haystack 2.0 is officially released. The concepts and components however stay the same.*

{{< /notice >}}


# The task

In Haystack's terminology, the process of extracting information from a group of files and properly store it into a document store is called "indexing". The process includes, at the very minimum, reading the content of a file and generate a Document object from it, and then store this Document into a document store. So you will need:

- A file converter
- A document writer

This is the very bare minimum set you need in a pipeline that does indexing. 

However, common indexing pipelines include more than two components. They should be able to process more than one file type, for example .txt, .pdf, .docx, .html, if not audio and video files, or images, so we need one component for each of these types. Having many file types to convert, we need a routing component that sends each file to the proper converter based in their type. Consider also that files tend to contain way more text than a normal LLM can chew, so we will need to split those huge Documents into smaller chunks. Also, the converters may not always do a perfect job, so we may need to clean the data from artifacts such as page numbers, headers and footers, and so on. On top of all of this, if you plan to use a retriever which is based on embedding similarity, you will also need to embed all documents before writing them into the store.

So you'll end up with a list that looks more like this:

- A file type router
- Several file converters
- A document cleaner
- A document splitter
- A document embedder
- A document writer

Sounds like a lot of work! 

In this post we will focus on the preprocessing part of the pipeline, so on cleaning, splitting, embedding and writing of documents. Later I am going to make another post focusing on all the converters that Haystack offers and how to build more "multimodal" indexing Pipelines.

# Converting files

One of the most important tasks of this pipeline is to convert files into Documents. Haystack provides several converters for this task: at the time of writing, it supports:

- Raw text files (`TextFileToDocument`)
- HTML files, so web pages in general (`HTMLToDocument`)
- PDF files, by extracting text natively (`PyPDFToDocument`)
- Image files, PDFs with images and Office files with images, by OCR (`AzureOCRDocumentConverter`)
- Audio files, doing transcription with Whisper either locally (`LocalWhisperTranscriber`) or remotely using OpenAI's hosted models (`RemoteWhisperTranscriber`)
- A ton of [other formats](https://tika.apache.org/2.9.1/formats.html), such as Microsoft's Office formats, thanks to [Apache Tika](https://tika.apache.org/) (`TikaDocumentConverter`)

In this post we are going to use only webpages, so our converter of choice is `HTMLToDocument`.

`HTMLToDocument` is a converter that understands HTML and to extract only meaningful text from it, filtering all the markup away. Keep in mind that this is a file converter, not a URL fetcher: it can only process local files, such as a website crawl. Haystack provides some components to fetch webpages, but we are going to see them in a later post.

Here is how you use this converter on a local file:

```python
from haystack.preview.components.file_converters.html import HTMLToDocument

path = "Republic_of_Rose_Island.html"

converter = HTMLToDocument()
converter.run(sources=[path])

# returns {"documents": [Document(text="The Republic of Rose Isla...")]}
```

`HTMLToDocument` is a very simple component that offers close to no parameters to customize its behavior. One interesting feature is the input types it accepts: it can take paths to local files in the form of strings or `Path` objects, but it also accepts `ByteStream` objects.

`ByteStream` is a handy Haystack abstraction that makes handling binary streams easier. So components that are retrieving large files from the Internet, or otherwise producing them on the fly, can "pipe" them directly into this component without saving the data to disk first.

# Cleaning the text

We've seen how to take whole web pages and convert them into large Document objects. The converters normally do a good job, but it's rarely parfect: so Haystack offers a component called `DocumentCleaner` that can help remove some noise from the text of the resulting documents.

Just as any other component, `DocumentCleaner` is rather straightforward to use.

```python
from haystack.preview.components.preprocessors.document_cleaner import DocumentCleaner

cleaner = DocumentCleaner()
cleaner.run(documents=documents)
# returns {"documents": [Document(text=...), Document(text=...), ...]}
```

The effectiveness of `DocumentCleaner` depends a lot on the type of converter you use. Some flags, such as `remove_empty_lines` and `remove_extra_whitespace`, are small fixes which can come handy, but normally have little impact on the quality of the results when used in a RAG pipeline. They can, however, make a vast difference for Extractive QA.

Other parameters, like `remove_substrings` or `remove_regex` work very well but need manual inspection and iteration from a human to get right. For example, for Wikipedia pages we could use them to remove all instances of the word `"Wikipedia"`, which are undoubtedly many and irrelevant.

Finally, `remove_repeated_substrings` is a convenient method that removed headers and footers from long text, for example books and articles, but in fact it works only for PDFs and to a limited degree for text files, because it relies on the presence of form feed characters (`\f`), which are rarely present in web pages.

# Splitting the text

Now that the text is cleaned up, we can move onto a more interesting process: text splitting.

So far, each Document stored the content of an entire file. If a file was a whole book with hundreds of pages, a single Document would contain hundreds of thousands of words, which is clearly too much for an LLM to make sense of (for now). Such a large Document is also very hard for Retrievers to understand, because it contains so much text that it ends up looking relevant for every possible question. To populate our document store with data that can be used effectively by a RAG pipeline, we need to chunk this data into much smaller Documents. 

That's where `TextDocumentSplitter` comes to play.

{{< notice info >}}

💡 *With LLMs in a race to offer the [largest context window](https://magic.dev/blog/ltm-1) and research showing that such chase is [counterproductive](https://arxiv.org/abs/2307.03172), there is no general consensus about how splitting Documents for RAG impacts the LLM's performance.*

*What you need to keep in mind is that splitting implies a tradeoff. Huge documents are always going to be a bit relevant for every question, but they will bring a lot of context which may, or may not, confuse the model. On the other hand, very small Documents are much more likely to be retrieved only for questions they're highly relevant for, but they might provide too little context for the LLM to really understand their meaning.*

*Tweaking the size of your Documents for the specific LLM you're using and the domain of your application is one way to optimize your RAG pipeline, so be ready to experiment with different Document sizes before committing to one.*

{{< /notice >}}

How is it used?

```python
from haystack.preview.components.preprocessors.text_document_splitter import TextDocumentSplitter

text_splitter = TextDocumentSplitter(split_by="sentence", split_length=5)
text_splitter.run(documents=documents)

# returns {"documents": [Document(text=...), Document(text=...), ...]}
```

`TextDocumentSplitter` lets you configure the approximate size of the chunks you want to generate with three parameters: `split_by`, `split_length` and `split_overlap`.

`split_by` defines the unit to use when splitting some text. For now the options are `word`, `sentence` and `passage` (paragraph), but we will soon add other options such as tokens.

`split_length` is the number of the units defined above each document should include. For example, if the unit is `sentence`, `split_length=10` means that all you Documents will contain 10 sentences worth of text (except usually for the last document, which will contain less). If the unit was `word`, it would instead contain 10 words.

`split_overlap` is the amount of unit that should be included from the previous Document. For example, if the unit is `sentence` and the length is `10`, setting `split_overlap=2` means that the last two sentences of the first document will be present also at the start of the second, which will include only 8 new sentences for a total of 10. Such repetition carries over to the end of the text to split.

# Compute text embeddings

Now that we have a set of clean, short Documents, we're almost ready to store them. At this stage there's an optional step that we can take, which is, to compute the embeddings for each Document.

In my previous post about RAG pipelines I've used (purposefully) a BM25 Retriever, which does not use embeddings. However, BM25 is by far not the most effective or failsafe retrieval method: embedding based retrieval, in fact, regularly outperforms it in nearly every scenario.

There are some downsides of using embeddings for retrieval:
- Computing embedding similarity is normally more expensive than computing a BM25 score,
- Both the query and all the Documents need to be converted into embeddings before the calculations can take place,
- Every model architecture has its own embedding type, which also require a dedicated tokenizer.

So, even if it is more powerful, using embeddings for retrieval does require some extra work.

If you decide to use this retrieval style, you would need to compute embeddings for all your Documents before storing them. Such a calculation should be done right before writing the Documents into the store, and makes use of a component called Embedder.

Right now Haystack offers two types of Embedders for Documents: one for OpenAI models, and one for SentenceTransformers models. We are going to use the OpenAI one for now, which is called `OpenAIDocumentEmbedder`.

Let's see hos it is used:

```python
from haystack.preview.components.embedders.openai_document_embedder import OpenAIDocumentEmbedder

embedder = OpenAIDocumentEmbedder(api_key=api_key)
embedder.run(documents=split_documents)["documents"]

# returns {"documents": [Document(text=...), Document(text=...), ...]}
```
After running the embedder, the list of Documents may look unchanged. However, after passing through this component, all Documents will have their `embedding` field populated with a large vector, that can then be used by the document store for retrieval.

`OpenAIDocumentEmbedder` offers some parameters to let you customize the generation of your embeddings. To begin, you can choose the `model_name`: the default is `text-embedding-ada-002`. You can then pass the OpenAI `organization` keyword if that's necessary to authenticate.

Two parameters, `prefix` and `suffix`, do pretty much what the name implies: they put fixed prefixes or suffixes to the document's content right before embedding it. It may be useful in some conditions to make the embedding more meaningful to the LLM, but it strongly depends on your usecase.

`metadata_fields_to_embed` provides something even more powerful: it appends the content of the document's metadata to the text. Often the metadata of a document contains information that the text is missing, but that is crucial to understand its content. For example, the metadata can containt the date the Document was created, giving the LLM a more precise sense of time. Or if the Document is a snippet of text from a legal document, it may be talking about "the Company", the "First Party", and so on, but the definition of such terms is not the paragraph: if the metadata contains keys such as `{"title": "Certificate of Incorporation - XYZ Inc."}`, it allows the LLM to frame the content of the Document much more precisely. In short: the richer the metadata, the more useful it is to embed it together with the Document's content.

Finally, `embedding_separator` is a small fine-tuning parameter that sets which character to use to separate the metadata fields to embed when they are appended to the Document's content. You normally don't need to use it.

# Writing to the store

Once all of this is done, we can finally move onto the last step of our journey: writing the Documents into our document store. Luckily, this process is really simple. We first create the document store:

```python
from haystack.preview.document_stores import InMemoryDocumentStore

document_store = InMemoryDocumentStore()
```

and then use `DocumentWriter` to actually write the documents in.


```python
from haystack.preview.components.writers import DocumentWriter

writer = DocumentWriter(document_store=document_store)
writer.run(documents=documents_with_embeddings)
```

If you've seen my [previous post](/posts/2023-10-27-haystack-series-rag) about RAG Pipelines you may wonder: why use `DocumentWriter` when we could just call the `.write_documents()` method of our document store?

In fact, the two methods are fully equivalent: `DocumentWriter` does nothing more than calling the `.write_documents()` method of the document store. The difference is that `DocumentWriter` is the way to go if you are using a Pipeline, which is exactly what we're going to do next.

# Putting it all together

We finally have all the components we need to go from a heterogeneous list of files to a document store populated with clean, short, searchable Document objects. Let's build a Pipeline to sum up this entire process:

```python
from haystack.preview import Pipeline

document_store = InMemoryDocumentStore()

pipeline = Pipeline()
pipeline.add_component("converter", HTMLToDocument())
pipeline.add_component("cleaner", DocumentCleaner())
pipeline.add_component("splitter", TextDocumentSplitter(split_by="sentence", split_length=5))
pipeline.add_component("embedder", OpenAIDocumentEmbedder(api_key=api_key))
pipeline.add_component("writer", DocumentWriter(document_store=document_store))
pipeline.connect("converter", "cleaner")
pipeline.connect("cleaner", "splitter")
pipeline.connect("splitter", "embedder")
pipeline.connect("embedder", "writer")

pipeline.draw("simple-indexing-pipeline.png")

pipeline.run({"converter": {"sources": file_names}})
```

![Indexing Pipeline](/posts/2023-11-xx-haystack-series-minimal-indexing/simple-indexing-pipeline.png)

That's it! We now have a fully functional indexing pipeline that can take a web page and convert them into Documents that our RAG pipeline can use. As long as the RAG pipeline reads from the store we are writing the Documents too, we can add as many Documents as we need to keep the chatbot's answers up to date without having to touch the RAG pipeline at all.

However, it doesn't end here. This pipeline is very simple: Haystack offers many more facilities to extend what's possible with indexing pipelines much further, like doing web searches, downloading files from the web, processing many other file types, and so on. We will see how soon, so make sure to check out the next posts.

---

*Next: Soon!*

*Previous: [RAG Pipelines from scratch](/posts/2023-10-27-haystack-series-rag)*

*See the entire series here: [Haystack 2.0 series](/series/haystack-2.0-series/)*
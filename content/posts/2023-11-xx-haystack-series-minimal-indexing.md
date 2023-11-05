---
title: "Indexing data for RAG applications"
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

In this post I will show you a few ways to use Haystack 2.0 to populate a document store that you can then use for retrieval.

{{< notice info >}}

💡 *Do you want to see the code in action? Check out the [Colab notebook](https://colab.research.google.com/drive/1gmdQem6f0RBYBb0HeBDPZwbb7_JU3-Us?usp=sharing) or the [gist](#).*

{{< /notice >}}

{{< notice warning >}}

<i>⚠️ **Warning:**</i> *This code was tested on `haystack-ai==0.105.0`. Haystack 2.0 is still unstable, so later versions might introduce breaking changes without notice until Haystack 2.0 is officially released. The concepts and components however stay the same.*

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

Sounds like a lot of work! Let's explore this pipeline one component at a time.

# Converting files

One of the most important tasks of this pipeline is to convert files into Documents. Haystack provides several converters for this task: at the time of writing, it supports:

- Raw text files (`TextFileToDocument`)
- HTML files, so web pages in general (`HTMLToDocument`)
- PDF files, by extracting text natively (`PyPDFToDocument`)
- Image files, PDFs with images and Office files with images, by OCR (`AzureOCRDocumentConverter`)
- Audio files, doing transcription with Whisper either locally (`LocalWhisperTranscriber`) or remotely using OpenAI's hosted models (`RemoteWhisperTranscriber`)
- A ton of [other formats](https://tika.apache.org/2.9.1/formats.html), such as Microsoft's Office formats, thanks to [Apache Tika](https://tika.apache.org/) (`TikaDocumentConverter`)

For the sake of making the example easy to run on Colab, I'll skip Tika, Azure and the local Whisper component. We are left with four converters for text files, web pages, PDFs and audio files. Let's check them out!

## Text files

`TextFileToDocument` is a rather basic converter that reads the content of a text file and dumps it into a Document object. It's perfect for raw text files, code files, and for now it's also very handy for Markdown and other human-readable markup formats, like Wikipedia dumps. We are [already working](https://github.com/deepset-ai/haystack/pull/6159) to introduce dedicated converters to extract more information from markup formats, but `TextFileToDocument` will always be a quick-and-dirty option as well.

Here is how you can use it to convert some files.

```python
from haystack.preview.components.file_converters.txt import TextFileToDocument

path = "Republic_of_Rose_Island.txt"

converter = TextFileToDocument()
converter.run(paths=[path])

# returns {"documents": [Document(text="The '''Republic of Rose Isla...")]}
```

Note that for each input path you will get a Document out. As we passed the path to a single file, `TextFileToDocument` produced a single, large Document as a result.

The behavior of `TextFileToDocument` can be customized to support some different usecases. For example, you can select the text encoding to expect (such as `utf-8`, `latin-1`, and so on) through the `encoding` parameter, but you can also make it filter out text in unexpected languages using the `valid_languages` parameter, which uses `langdetect` under the hood. 

Another advanced feature is the removal of numerical lines: `remove_numeric_tables` can be set to `True` to make the converter try to spot numerical tables and automatically remove them from the text, while `numeric_row_threshold` sets the maximum percentage of numerical characters that can be present in a line before it's considered to be a numerical table and filtered out. This cleanup step is disabled by default.

## Web pages

`HTMLToDocument` is a converter that understands HTML and to extract only meaningful text from it, filtering all the markup away. Keep in mind that this is a file converter, not a URL fetcher: it can only process local files, such as a website crawl. Haystack provides some components to fetch webpages, but we are going to see them in a later post.

Here is how you use this converter on a local file.

```python
from haystack.preview.components.file_converters.html import HTMLToDocument

path = "Republic_of_Rose_Island.html"

converter = HTMLToDocument()
converter.run(sources=[path])

# returns {"documents": [Document(text="The Republic of Rose Isla...")]}
```

`HTMLToDocument` is even simpler than the text converter, and for now offers close to no parameters to customize its behavior. One interesting feature though its the input types it accepts: it can take paths to local files in the form of strings or `Path` objects, but it also accepts `ByteStream` objects.

`ByteStream` is a handy Haystack abstraction that makes handling binary streams easier. So components that are retrieving large files from the Internet, or otherwise producing them on the fly, can "pipe" them directly into this component without saving the data to diks first.

## PDFs

`PyPDFToDocument`, as the name implies, uses the `pypdf` Python library to extract text from PDF files. Note that PyPDF can extract everything that is stored as text in the PDF, but it cannot recognise text stored in pictures. For that you need an OCR-capable converter, such as `AzureOCRDocumentConverter`, which needs an Azure API key.

Let's convert some files with `PyPDFToDocument`:

```python
from haystack.preview.components.file_converters.pypdf import PyPDFToDocument

path = "Republic_of_Rose_Island.pdf"

converter = PyPDFToDocument()
pdf_documents = converter.run(sources=[path])

# returns {"documents": [Document(text="The Republic of Rose Isla...")]}
```

`PyPDFToDocument` is also very simple and offers no parameters to customize its behavior for now. Just as `HTMLToDocument`, it also accepts as input strings, paths, and `ByteStream` objects, which will come handy when we will see how to retrieve documents from the Internet.

## Audio files

Last but not least, Haystack provides transcriber components based on [Whisper](https://openai.com/research/whisper) that can be used to convert audio files into text Documents. Whisper is open source, but is also available as an API from OpenAI: as a consequence, there are two transcribers available:

- `LocalWhisperTranscriber`: it downloads the selected Whisper model from HuggingFace and performs the transcription locally.
- `RemoteWhisperTranscriber`: it uses OpenAI API to run inference remotely, which may be faster, but required an API key.

For the sake of this example we will use the remote transcriber, but the local one is nearly identical. Here is how you use them:

```python
from haystack.preview.components.audio.whisper_remote import RemoteWhisperTranscriber

path = "/content/Republic_of_Rose_Island.mp3"

converter = RemoteWhisperTranscriber(api_key=api_key)
converter.run(audio_files=[path])

# returns {"documents": [Document(text="The Republic of Rose Isla...")]}
```

This converter lets you pass any parameter that the Whisper model understand as kwargs, so if the API changes, the component will keep working. Other than that, it offers no other specific parameters.


# Routing files

Now that we're familiar with the simple API offered by the file converters, let's track back one step: in a list of files, how to send the appropriate file to the correct converter?

This step is especially important for Pipelines, so Haystack offers a small component that is fit for the purpose: `FileTypeRouter`. This component routes the files by mime type, and expects a list of all the possible mimetypes the pipeline can handle at init time. 

Given that our pipeline can handle text files, HTML files, PDFs and audios, the supported mime types in our case are `["text/plain", "text/html", "audio/mpeg", "application/pdf"]`. If you don't know which mime types match your file types, check out [this list](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types) with the most common types, and in turn links to the [official spec](https://www.iana.org/assignments/media-types/media-types.xhtml). To be really accurate we could add other text and audio types to the list and route all of them to `TextFileToDocument` and `RemoteWhisperTranscriber`, but for this example this is going to be sufficient.

Here is how it's used:

```python
from haystack.preview.components.routers.file_type_router import FileTypeRouter

router = FileTypeRouter(
    mime_types=["text/plain", "text/html", "audio/mpeg", "application/pdf"]
)
router.run(
    sources=[
        "Republic_of_Rose_Island.txt", 
        "Republic_of_Rose_Island.html", 
        "Republic_of_Rose_Island.pdf", 
        "Republic_of_Rose_Island.mp3"
    ]
)
# returns {
#    'text/plain': [PosixPath('Republic_of_Rose_Island.txt')],
#    'text/html': [PosixPath('Republic_of_Rose_Island.html')],
#    'application/pdf': [PosixPath('Republic_of_Rose_Island.pdf')],
#    'audio/mpeg': [PosixPath('Republic_of_Rose_Island.mp3')],
# }
```
Note how, just as the HTML and PDF converters, also `FileTypeRouter` expects `sources` as input, meaning that it knows how to deal with `ByteStream` objects. 

However, what happens if we add a file of a mime type that is not included in the list above, or a path to a file that doesn't exist at all?

```python
router.run(
    sources=[ 
        "Republic_of_Rose_Island.png",
        "Republic_of_Rose_Island.mp3",
        "I_do_not_even_exist_and_I_have_no_extension"
    ]
)
# returns {
#    'audio/mpeg': [PosixPath('Republic_of_Rose_Island.mp3')],
#    'unclassified': [
#        PosixPath('Republic_of_Rose_Island.png'),
#        PosixPath('I_do_not_even_exist_and_I_have_no_extension')
#    ],
# }
```

This is one powerful feature of `FileTypeRouter`: it can not only route files each to their own converter, but it can also filter out files that we have no use for.


# Cleaning the text

So we now have a way to classify the files by type and we can convert them all into a bunch of large Document objects. The converters normally do a good job, but it's rarely parfect: so Haystack offers a component called `DocumentCleaner` that can help remove some noise from the text of the resulting documents.

Just as any other component, `DocumentCleaner` is rather straightforward to use.

```python
from haystack.preview.components.preprocessors.text_document_cleaner import DocumentCleaner

cleaner = DocumentCleaner()
cleaner.run(documents=documents)
# returns {"documents": [Document(text=...), Document(text=...), ...]}
```

The effectiveness of `DocumentCleaner` depends a lot on the type of converter you use. Some flags, such as `remove_empty_lines` and `remove_extra_whitespace`, are small fixes which can come handy, but normally have little impact on the quality of the results when used in a RAG pipeline. They can, however, make a vast difference for Extractive QA.

Other parameters, like `remove_substrings` or `remove_regex` work very well but need manual inspection and iteration from a human to get right. For example, for Wikipedia pages we could use them to remove all instances of the word `"Wikipedia"`, which are undoubtedly many and irrelevant.

Finally, `remove_repeated_substrings` is a convenient method that removed headers and footers from long text, for example books and articles, but in fact it works only for PDFs and to a limited degree for text files, because it relies on the presence of form feed characters (`\f`).

# Splitting the text

Now that the text is cleaned up, we can mov onto a more interesting process: text splitting.

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
pipeline.add_component("router", FileTypeRouter(mime_types=["text/plain", "text/html", "application/pdf", "audio/mpeg"]))
pipeline.add_component("text_converter", TextFileToDocument())
pipeline.add_component("html_converter", HTMLToDocument())
pipeline.add_component("pdf_converter", PyPDFToDocument())
pipeline.add_component("mp3_converter", RemoteWhisperTranscriber(api_key=api_key))
pipeline.add_component("join", DocumentsJoiner())
pipeline.add_component("cleaner", DocumentCleaner())
pipeline.add_component("splitter", TextDocumentSplitter(split_by="sentence", split_length=5))
pipeline.add_component("embedder", OpenAIDocumentEmbedder(api_key=api_key))
pipeline.add_component("writer", DocumentWriter(document_store=document_store))
pipeline.connect("router.text/plain", "text_converter")
pipeline.connect("router.text/html", "html_converter")
pipeline.connect("router.application/pdf", "pdf_converter")
pipeline.connect("router.audio/mpeg", "mp3_converter")

pipeline.connect("text_converter", "join.text")
pipeline.connect("html_converter", "join.html")
pipeline.connect("pdf_converter", "join.pdf")
pipeline.connect("mp3_converter", "join.mp3")

pipeline.connect("join", "cleaner")
pipeline.connect("cleaner", "splitter")
pipeline.connect("splitter", "embedder")
pipeline.connect("embedder", "writer")

pipeline.run({
    "router": {
        "sources": [
            "Republic_of_Rose_Island.txt",
            "Republic_of_Rose_Island.pdf",
            "Republic_of_Rose_Island.html",
            "Republic_of_Rose_Island.mp3",
        ]
    }
})
```

![Indexing Pipeline](/posts/2023-11-xx-haystack-series-minimal-indexing/indexing-pipeline.png)

.

.

.

---

*Next: Soon!*

*Previous: [RAG Pipelines from scratch](/posts/2023-10-27-haystack-series-rag)*

*See the entire series here: [Haystack 2.0 series](/series/haystack-2.0-series/)*
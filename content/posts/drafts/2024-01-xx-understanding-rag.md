---
title: "Understanding RAG"
date: 2024-01-30
author: "ZanSara"
tags: [NLP, Python, LLM, GPT, "Retrieval Augmentation", RAG, "Semantic Search"]
featuredImage: "/posts/2024-01-30-understanding-rag/cover.png"
draft: true
---


References:

https://stackoverflow.blog/2023/10/18/retrieval-augmented-generation-keeping-llms-relevant-and-current/

Retrieval-Augmented Generation for Large Language Models: A Survey https://arxiv.org/abs/2312.10997

Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (original Meta articl) https://arxiv.org/abs/2005.11401

https://developer.nvidia.com/blog/rag-101-demystifying-retrieval-augmented-generation-pipelines/

https://huggingface.co/docs/transformers/model_doc/rag

https://www.turing.com/resources/understanding-retrieval-augmented-generation-rag




Retrieval Augmented Generation (RAG) is quickly becoming an essential technique to make LLMs more reliable and effective at answering any question, regardless of how specific. To stay relevant in today's NLP landscape, Haystack must enable it.

Let's see how to build such applications with Haystack 2.0, from a direct call to an LLM to a fully-fledged, production-ready RAG pipeline that scales. At the end of this post, we will have an application that can answer questions about world countries based on data stored in a private database. At that point, the knowledge of the LLM will be only limited by the content of our data store, and all of this can be accomplished without fine-tuning language models.




## What is RAG?

The idea of Retrieval Augmented Generation was first defined in a [paper](https://arxiv.org/abs/2005.11401) by Meta in 2020. It was designed to solve a few of the inherent limitations of seq2seq models (language models that, given a sentence, can finish writing it for you), such as:

- Their internal knowledge, as vast as it may be, will always be limited and at least slightly out of date.
- They work best on generic topics rather than niche and specific areas unless they're fine-tuned on purpose, which is a costly and slow process.
- All models, even those with subject-matter expertise, tend to "hallucinate": they confidently produce false statements backed by apparently solid reasoning.
- They cannot reliably cite their sources or tell where their knowledge comes from, which makes fact-checking their replies nontrivial.

RAG solves these issues of "grounding" the LLM to reality by providing some relevant, up-to-date, and trusted information to the model together with the question. In this way, the LLM doesn't need to draw information from its internal knowledge, but it can base its replies on the snippets provided by the user.

![RAG Paper diagram](/posts/2023-10-27-haystack-series-rag/rag-paper-image.png "A visual representation of RAG from the original paper")

As you can see in the image above (taken directly from the original paper), a system such as RAG is made of two parts: one that finds text snippets that are relevant to the question asked by the user and a generative model, usually an LLM, that rephrases the snippets into a coherent answer for the question.

Let's build one of these with Haystack 2.0!

{{< notice info >}}

💡 *Do you want to see this code in action? Check out the Colab notebook [here](https://colab.research.google.com/drive/1FkDNS3hTO4oPXHFbXQcldls0kf-KTq-r?usp=sharing) or the gist [here](https://gist.github.com/ZanSara/0af1c2ac6c71d0a723c179cc6ec1ac41)*.

{{< /notice >}}

{{< notice warning >}}

⚠️ **Warning:** *This code was tested on `haystack-ai==0.149.0`. Haystack 2.0 is still unstable, so later versions might introduce breaking changes without notice until Haystack 2.0 is officially released. The concepts and components however stay the same.*

{{< /notice >}}

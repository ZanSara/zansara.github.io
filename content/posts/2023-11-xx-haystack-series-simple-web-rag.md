---
title: "[DRAFT] The World of Web RAG"
date: 2023-11-30
author: "ZanSara"
tags: ["Haystack 2.0", Haystack, NLP, Python, LLM, GPT, "Retrieval Augmentation", RAG, "Semantic Search", Web]
series: ["Haystack 2.0 Series"]
featuredImage: "/posts/2023-11-xx-haystack-series-simple-web-rag/cover.jpeg"
draft: true
---

In the previous post of the Haystack 2.0 series we've seen how to build RAG pipelines using a generator, a prompt builder and a retriever with its document store. An application like that is great if you have a large data store and you need to perform RAG onto private data only. However, in many cases you may want to get data from the Internet as well, for example from news outlets, from documentation pages, and so on. 

In this post we are going to see how to build a Web RAG pipeline, starting from a simple local one and replacing the retriever with components that can find relevant information on the web.

# Searching the Web

To accomplish this goal, rather than a Retriever we need a Search Engine.

Haystack 2.0 already provides a search engine component called `SerperDevWebSearch`. It uses [SerperDev's API](https://serper.dev/) to query popular search engines and return two types of data: a list of text snippets, coming from the serach engine's preview boxes, and a list of links, which point to the top search results.














---

*Next: Soon!*

*Previous: [Indexing data for RAG applications](/posts/2023-11-05-haystack-series-minimal-indexing)*

*See the entire series here: [Haystack 2.0 series](/series/haystack-2.0-series/)*

<small>*Cover image from [Wikipedia](https://commons.wikimedia.org/wiki/File:Isola_delle_Rose_1968.jpg)*</small>

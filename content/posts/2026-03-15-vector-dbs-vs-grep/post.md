---
title: "Is grep really better than a vector DB?"
description: "Some agentic applications don't use vector DBs for search. Is it a good idea?"
date: 2026-03-15
author: "ZanSara"
series: ["Practical Questions"]
featured-image: "/posts/2026-03-15-vector-dbs-vs-grep/cover-inv.png"
---

---

_This is episode 7 of a series of shorter blog posts answering questions I received during the course of my work. They discuss common misconceptions and doubts about various generative AI technologies. You can find the whole series here: [Practical Questions](/series/practical-questions)._

---
For the past two years, the default architecture for giving LLMs access to a knowledge base has been **RAG with vector databases**. 

This architecture turned out to be very powerful, but it's far from cheap to setup and maintain: you need the system to chunk all the documents, embed all the chunks, store them in a vector DB, retrieve them, and feed them to the model. Every new document needs to go through this pipeline before it's usable, and changes to a document already processed means going through the vector DB and deleting all the affected chunks.

So it may come as a big surprise for many of us to learn that, as some people claims, an agent equipped with `grep` can find the data it's looking for just as well.

For example, [one of the many comparisons](https://youtu.be/99Kxkemj1g8?t=4308) that have been done on this topic found roughly these figures when answering questions about a Django codebase:

1. **Vector search** over embedded chunks achieved ~60% accuracy.
2. **Agentic search** using tools like `grep`, `find`, and `cat`, where the model iteratively explores the repository, achieved ~68%.

The same test on a TypeScript/Go codebase had the two approaches both reaching around ~70%.  

The difference was **cost and context**: vector search consumed significantly more tokens. While it arguably provided more context to the agent, it's not clear whether the context retrieved this way was more useful, and it's easy to find contradicting results on the Internet.

So, what's truly going on? 

If I had to summarize it in one sentence, it would be: retrieval quality depends heavily on the domain and the structure of the information.

## Let's check our assumptions

Classic retrieval steps in the RAG architecture assumes the query **must be correct on the first try**. Because of this, most of the effort and breakthroughs in this field focused on getting decent results for all possible queries. 

Vector search shines at this. By getting the chunks of context that semantically come as close as possible to the query (or to an answer to it), embedding-based retrieval was crucial for the one-shot retrieval typical of RAG apps.

However, agents remove that constraint. An agent can try an initial search with a surely subpar query, then inspect the results, refine the query, and search again.

This iterative process dramatically reduces the weaknesses of keyword search and, in fact, leverages all its strengths: exact keyword retrieval is not an ideal task for a vector DB, because semantically similar keywords will also be included.

This does not mean vector search is useless in the age of agents.

## Domain Differences

Retrieval strategies behave very differently depending on the domain. Let's see a few examples to understand where one approach or the other shines.

### Code Search

Code search is a perfect candidate for **agentic keyword search**, because identifiers are keywords that need exact matches in the results. 

Vector search, while possible, has always been difficult to perform effectively on code. On top of that, there are tons of tools and techniques made for human coders to navigate a codebase with keywords, and agents can take advantage of those. For example, agents can use `grep`, AST search, symbol indexing, repository graphs, and more.

There's also a problem with **context fragmentation**. Vector search returns chunks, which in the case of code search are usually a fixed number of lines or symbols. Most of the time this context is useless for the agent, because it rarely includes a full logical unit, and when it does (such as when chunking on function boundaries), it becomes much harder to retrieve, because the chunks are larger.

This means that not only is vector search less precise, but it also wastes a lot of context.

### How-to Guides / Knowledge Bases / General Prose

This is the classic use case where **vector search shines** and keyword search is far less effective.

When your corpus of text is made of conceptual explanations, natural language queries, inconsistent terminology, and so on, semantic similarity is the most likely to bring up relevant results.

Even in this case, however, pure vector search usually gets beaten by hybrid approaches, such as running vector and keyword searches in parallel and then reranking the results.

You can find more about hybrid retrieval in [this other post of mine](/posts/2025-11-04-hybrid-retrieval/).

### Legal / Medical / Scientific Documents

These sit somewhere in between. In these documents, the terminology is specialized, wording matters, and citations and sections are important. Vector search can surface relevant passages, but precision matters more than in the previous scenario. There's more structure than in free-form prose, and you can't lose it during the retrieval phase.

For these kinds of documents, hybrid approaches are necessary to avoid too many false positive matches.

## What should I pick?

Choosing an approach usually depends on the use cases you foresee for your agent, but in practice it's often difficult to know beforehand what kind of documents your agent will need to sift through. Even coding agents need to search the web and read technical documentation, for example.

In these situations, it's best to avoid flattening the decision into a "keyword vs embeddings" choice. Your agent can make use of both of them and more. For example, if your agent must be able to search anything, you may give it:

- A vector DB for static, shapeless prose, for example internal knowledge bases, static "ground truth" documents, foundational data, etc. Even searching through messages on Slack and Teams may be a good fit for a vector DB.
- Tools like `grep`, `cat`, `find`, etc. Let the agent leverage its coding skills for quick keyword searches across all the data. Don't forget to make the data that's available in the vector DB also accessible through these tools.
- A simple BM25 index that can be searched for keyword matches when the results from the command-line tools are overwhelming for the agent.
- A web search tool that the agent can use to complement its local search results, if applicable.

... and so on. 

## Conclusion

Vector databases are not automatically the correct architecture. Neither is `grep`.

Before choosing, it is worth asking:

- Is the information to search through **structural** or **semantic**?
- Do queries benefit from **iteration**? Will my agent be able to retry the search as many times as it wants?
- Would a simple keyword search index solve most cases, or do I need to search by meaning?

Sometimes the correct system architecture is a sophisticated hybrid embedding retriever. And sometimes it is still just `grep -R "the keyword"`.

The only way to know for sure is, as usual, a RAG evaluation pipeline. Don't forget to measure your outcomes!


---
title: "ODSC East: RAG, the bad parts (and the good!)"
date: 2024-04-25
author: "ZanSara"
tags: [LLM, NLP, Python, AI, RAG, "ODSC East", ODSC, Retrieval, Generation, Evaluation, Haystack]
featuredImage: "/talks/2024-04-25-odsc-east-rag.png"
---

[Announcement](https://odsc.com/speakers/rag-the-bad-parts-and-the-good-building-a-deeper-understanding-of-this-hot-llm-paradigms-weaknesses-strengths-and-limitations/), [slides](https://drive.google.com/file/d/19EDFCqOiAo9Cvx5fxx6Wq1Z-EoMKwxbs/view?usp=sharing)

---

At [ODSC East 2024](https://odsc.com/boston/) I talked about RAG: how it works, how it fails, and how to evaluate its performance objectively. I gave an overview of some useful open-source tools for RAG evalution and how to use them with [Haystack](https://haystack.deepset.ai/?utm_campaign=odsc-east), and then offer some ideas on how to expand your RAG architecture further than a simple two-step process.

Some resources mentioned in the talk:

- Haystack: open-source LLM framework for RAG and beyond: [https://haystack.deepset.ai/](https://haystack.deepset.ai/?utm_campaign=odsc-east)
- Build and evaluate RAG with Haystack: [https://haystack.deepset.ai/tutorials/35_model_based_evaluation_of_rag_pipelines](https://haystack.deepset.ai/tutorials/35_model_based_evaluation_of_rag_pipelines/?utm_campaign=odsc-east)
- Evaluating LLMs with UpTrain: https://docs.uptrain.ai/getting-started/introduction
- Evaluating RAG end-to-end with RAGAS: https://docs.ragas.io/en/latest/
- Semantic Answer Similarity (SAS) metric: https://docs.ragas.io/en/latest/concepts/metrics/semantic_similarity.html
- Answer Correctness metric: https://docs.ragas.io/en/latest/concepts/metrics/answer_correctness.html
- Perplexity.ai: https://www.perplexity.ai/

Plus, shout-out to a very interesting LLM evaluation library I discovered at ODSC: [continuous-eval](https://docs.relari.ai/v0.3). Worth checking out especially if SAS or answer correctness are too vague and high level for your domain.
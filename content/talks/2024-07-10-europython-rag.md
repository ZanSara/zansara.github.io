---
title: "EuroPython: Is RAG all you need? A look at the limits of retrieval augmented generation"
date: 2024-07-10
author: "ZanSara"
featuredImage: "/talks/2024-07-10-europython-rag.png"
---

[Announcement](https://ep2024.europython.eu/session/is-rag-all-you-need-a-look-at-the-limits-of-retrieval-augmented-generation), 
[slides](https://drive.google.com/file/d/13OXMLaBQr1I_za7sqVHJWxRj5xFAg7KV/view?usp=sharing).
Did you miss the talk? Check out the [recording](https://drive.google.com/file/d/1OkYQ7WMt63QkdJTU3GIpSxBZmnLfZti6/view?usp=sharing) (cut from the [original stream](https://www.youtube.com/watch?v=tcXmnCJIvFc)),
or the [write-up](/posts/2024-04-29-odsc-east-rag) of a previous edition of the same talk.

---

{{< raw >}}
<div class='iframe-wrapper'>
<iframe src="https://drive.google.com/file/d/1OkYQ7WMt63QkdJTU3GIpSxBZmnLfZti6/preview" width=100% height=100% allow="autoplay"></iframe>
</div>
{{< /raw >}}

At [EuroPython 2024](https://ep2024.europython.eu/) I talked about RAG: how it works, how it fails, and how to evaluate its performance objectively. I gave an overview of some useful open-source tools for RAG evalution such as [continuous-eval](https://docs.relari.ai/v0.3?utm_campaign=europython-2024) and how to use them with [Haystack](https://haystack.deepset.ai/?utm_campaign=europython-2024), and then offered some ideas on how to expand your RAG architecture further than a simple two-step process.

Some resources mentioned in the talk:

- [Haystack](https://haystack.deepset.ai/?utm_campaign=europython-2024): open-source LLM framework for RAG and beyond.
- [continuous-eval](https://docs.relari.ai/v0.3?utm_campaign=europython-2024) by [Relari AI](https://www.relari.ai/?utm_campaign=europython-2024).
- Build and evaluate RAG with Haystack: [https://haystack.deepset.ai/tutorials/35_model_based_evaluation_of_rag_pipelines](https://haystack.deepset.ai/tutorials/35_model_based_evaluation_of_rag_pipelines/?utm_campaign=europython-2024)
- Use continuous-eval with Haystack: <https://github.com/relari-ai/examples/blob/main/examples/haystack/simple_rag/app.py>
- Perplexity.ai: https://www.perplexity.ai/

---
title: "AMTA 2024 Virtual Tutorial Day: Controlling LLM Translations of Invariant Elements with RAG"
date: 2024-09-18
author: "ZanSara"
featuredImage: "/talks/2024-09-18-amta-2024-controlling-invariants-rag.png"
---

[Announcement](https://amtaweb.org/virtual-tutorial-day-program/), 
[notebook](https://colab.research.google.com/drive/1VMgK3DcVny_zTtAG_V3QSSdfSFBWAgmb?usp=sharing) and 
[glossary](https://docs.google.com/spreadsheets/d/1A1zk-u-RTSqBfE8LksZxihnp7KxWO7YK/edit?usp=sharing&ouid=102297935451395786183&rtpof=true&sd=true).
All resources can also be found in 
[my archive](https://drive.google.com/drive/folders/1Tdq92P_E_77sErGjz7jSPfJ-or9UZXvn?usp=drive_link).

---

{{< raw >}}
<div class='iframe-wrapper'>
<iframe src="https://drive.google.com/file/d/1BvcNbsAGWp25EDpiQ5ljYos3_eneo3wu/preview" width=100% height=100% allow="autoplay"></iframe>
</div>
{{< /raw >}}

---

At the [AMTA 2024 Virtual Tutorial Day](https://amtaweb.org/virtual-tutorial-day-program/) I talked about controlling invariant translation elements with RAG. During the talk several speakers intervened on the topic, each bringing a different perspective of it. 

[Georg Kirchner](https://www.linkedin.com/in/georgkirchner/) introduced the concept of invariant translation elements, such as brand names, UI elements, and corporate slogans. [Christian Lang](https://www.linkedin.com/in/christian-lang-8942b0145/) gave a comprehensive overview of the challenges of handling invariant translation elements with existing tools and how LLMs can help at various stages of the translation, covering several approaches, including RAG. Building on his overview, I showed how to implement a simple RAG system to handle these invariants properly using [Haystack](https://haystack.deepset.ai/?utm_campaign=amta-2024): we run a [Colab notebook](https://colab.research.google.com/drive/1VMgK3DcVny_zTtAG_V3QSSdfSFBWAgmb?usp=sharing) live and checked how the translation changes by introducing context about the invariants to the LLM making the translation. Last, [Bruno Bitter](https://www.linkedin.com/in/brunobitter/) gave an overview of how you can use [Blackbird](https://www.blackbird.io/) to integrate a system like this with existing CAT tools and manage the whole lifecycle of content translation.

---
title: "Office Hours: RAG Pipelines"
date: 2023-10-12
author: "ZanSara"
featuredImage: "/talks/2023-10-12-office-hours-rag-pipelines.png"
---

[Recording](https://drive.google.com/file/d/1UXGi4raiCQmrxOfOexL-Qh0CVbtiSm89/view?usp=drive_link), [notebook](https://gist.github.com/ZanSara/5975901eea972c126f8e1c2341686dfb). All the material can also be found [here](https://drive.google.com/drive/folders/17CIfoy6c4INs0O_X6YCa3CYXkjRvWm7X?usp=drive_link).

---

{{< raw >}}
<div class='iframe-wrapper'>
<iframe src="https://drive.google.com/file/d/1UXGi4raiCQmrxOfOexL-Qh0CVbtiSm89/preview" width="100%" height="100%" allow="autoplay"></iframe>
</div>
{{< /raw >}}

In this [Office Hours](https://discord.com/invite/VBpFzsgRVF) I walk through the LLM support offered by Haystack 2.0 to this date: Generator, PromptBuilder, and how to connect them to different types of Retrievers to build Retrieval Augmented Generation (RAG) applications. 

In under 40 minutes we start from a simple query to ChatGPT up to a full pipeline that retrieves documents from the Internet, splits them into chunks and feeds them to an LLM to ground its replies.

The talk indirectly shows also how Pipelines can help users compose these systems quickly, to visualize them, and helps them connect together different parts by producing verbose error messages.
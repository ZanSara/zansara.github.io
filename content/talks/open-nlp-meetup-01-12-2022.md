---
title: "A Practical Introduction to Image Retrieval"
date: 2021-12-01
author: "ZanSara"
tags: [haystack, llm, retrieval, nlp, image, colab, python, multimodality, ai, image-to-text]
featuredImage: "/talks/open-nlp-meetup-01-12-2022.png"
---

Youtube: [Open NLP meetup #7: Ethics in NLP & A Practical Introduction to Image Retrieval](https://www.youtube.com/watch?v=7Idjl3OR0FY) ([Backup]())

Slides: [A Practical Introduction to Image Retrieval](https://gist.github.com/ZanSara/dc4b22e7ffe2a56647e0afba7537c46b)

Colab: [MultiModalRetriever - Live coding](https://gist.github.com/ZanSara/9e8557830cc866fcf43a2c5623688c74)

All the material can also be found [here](https://drive.google.com/drive/folders/1_8vO8O5wcvqYyjDkt2NGbwF5X6aSWgV1?usp=drive_link).

---

## A Practical Introduction to Image Retrieval

*by Sara Zanzottera from deepset*

Search should not be limited to text only. Recently, Transformers-based NLP models started crossing the boundaries of text data and exploring the possibilities of other modalities, like tabular data, images, audio files, and more. Text-to-text generation models like GPT now have their counterparts in text-to-image models, like Stable Diffusion. But what about search? In this talk we're going to experiment with CLIP, a text-to-image search model, to look for animals matching specific characteristics in a dataset of pictures. Does CLIP know which one is "The fastest animal in the world"?

---

For the 7th OpenNLP meetup I presented the topic of Image Retrieval, a feature that I've recently added to Haystack in the form of a MultiModal Retriever.

The talk consists of 5 parts:

- An introduction of the topic of Image Retrieval
- A mention of the current SOTA model (CLIP)
- An overview of Haystack
- A step-by-step description of how image retrieval applications can be implemented with Haystack
- A live coding session where I start from a blank Colab notebook and build a fully working image retrieval system from the ground up, to the point where I can run queries live.

Towards the end I mention briefly an even more advanced version of this image retrieval system, which I had no time to implement live. However, I later built a notebook implementing such system and you can find it here: [Cheetah.ipynb](https://gist.github.com/ZanSara/31ed3fc8252bb74b1952f2d0fe253ed0)

The slides were generated from the linked Jupyter notebook with `jupyter nbconvert Dec_1st_OpenNLP_Meetup.ipynb --to slides --post serve`.

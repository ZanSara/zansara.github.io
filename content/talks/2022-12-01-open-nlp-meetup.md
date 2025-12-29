---
title: "OpenNLP Meetup: A Practical Introduction to Image Retrieval"
date: 2022-12-01
author: "ZanSara"
featuredImage: "/talks/2022-12-01-open-nlp-meetup.png"
---

[Youtube link](https://www.youtube.com/watch?v=7Idjl3OR0FY),
[slides](https://gist.github.com/ZanSara/dc4b22e7ffe2a56647e0afba7537c46b), [Colab](https://gist.github.com/ZanSara/9e8557830cc866fcf43a2c5623688c74) (live coding).
All the material can also be found [here](https://drive.google.com/drive/folders/1_3b8PsvykHeM0jSHsMUWQ-4h_VADutcX?usp=drive_link).

---

<iframe src="https://drive.google.com/file/d/19mxD-xUJ-14G-2XAqXEVpZfqR2MsSZTn" width="640" height="480" allow="autoplay"></iframe>

## A Practical Introduction to Image Retrieval

*by Sara Zanzottera from deepset*

Search should not be limited to text only. Recently, Transformers-based NLP models started crossing the boundaries of text data and exploring the possibilities of other modalities, like tabular data, images, audio files, and more. Text-to-text generation models like GPT now have their counterparts in text-to-image models, like Stable Diffusion. But what about search? In this talk we're going to experiment with CLIP, a text-to-image search model, to look for animals matching specific characteristics in a dataset of pictures. Does CLIP know which one is "The fastest animal in the world"?

---

For the 7th [OpenNLP meetup](https://www.meetup.com/open-nlp-meetup/) I presented the topic of Image Retrieval, a feature that I've recently added to Haystack in the form of a [MultiModal Retriever](https://docs.haystack.deepset.ai/docs/retriever#multimodal-retrieval) (see the [Tutorial](https://haystack.deepset.ai/tutorials/19_text_to_image_search_pipeline_with_multimodal_retriever)).

The talk consists of 5 parts:

- An introduction of the topic of Image Retrieval
- A mention of the current SOTA model (CLIP)
- An overview of Haystack
- A step-by-step description of how image retrieval applications can be implemented with Haystack
- A live coding session where I start from a blank Colab notebook and build a fully working image retrieval system from the ground up, to the point where I can run queries live.

Towards the end I mention briefly an even more advanced version of this image retrieval system, which I had no time to implement live. However, I later built a notebook implementing such system and you can find it here: [Cheetah.ipynb](https://gist.github.com/ZanSara/31ed3fc8252bb74b1952f2d0fe253ed0)

The slides were generated from the linked Jupyter notebook with `jupyter nbconvert Dec_1st_OpenNLP_Meetup.ipynb --to slides --post serve`.


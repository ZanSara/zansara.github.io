---
title: "An (unofficial) Python SDK for Verbix"
description: If you need a Python SDK for a verb conjugator, try this one while it's still alive.
date: 2023-09-10
author: "ZanSara"
featuredImage: "/posts/2023-09-10-python-verbix-sdk/cover.png"
---

PyPI package: https://pypi.org/project/verbix-sdk/

GitHub Repo: https://github.com/ZanSara/verbix-sdk

Minimal Docs: https://github.com/ZanSara/verbix-sdk/blob/main/README.md

---

As part of a larger side project which is still in the works ([Ebisu Flashcards](https://github.com/ebisu-flashcards)), these days I found myself looking for some decent API for verbs conjugations in different languages. My requirements were "simple":

- Supports many languages, including Italian, Portuguese and Hungarian
- Conjugates irregulars properly
- Offers an API access to the conjugation tables
- Refuses to conjugate anything except for known verbs
- (Optional) Highlights the irregularities in some way

Surprisingly these seem to be a shortage of good alternatives in this field. All websites that host polished conjugation data don't seem to offer API access (looking at you, [Reverso](https://conjugator.reverso.net) -- you'll get your own post one day), and most of the simples ones use heuristics to conjugate, which makes them very prone to errors. So for now I ended up choosing [Verbix](https://verbix.com) to start from.

Unfortunately the website doesn't inspire much confidence. I attempted to email the creator just to see them [close their email account](https://verbix.com/contact.html) a while later, an [update in their API](https://api.verbix.com/) seems to have stalled half-way, and the [blog seems dead](https://verb-blog.verbix.com/). I often have the feeling this site might go under any minute, as soon as their domain registration expires.

But there are pros to it, as long as it lasts. Verbix offers verbs conjugation and nouns declination tables for some [very niche languages, dialects and conlangs](https://verbix.com/languages/), to a degree that many other popular websites does not even come close. To support such variety they use heuristic to create the conjugation tables, which is not the best: for Hungarian, for example, I could easily get it to conjugate for me [verbs that don't exist](https://verbix.com/webverbix/go.php?T1=meegy&Submit=Go&D1=121&H1=221) or that have spelling mistakes. On the other hand their API do have a field that says whether the verb is known or not, which is a great way to filter out false positives.

So I decided to go the extra mile and I wrote a small Python SDK for their API: [verbix-sdk](https://pypi.org/project/verbix-sdk/). Enjoy it while it lasts...

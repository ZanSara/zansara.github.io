---
title: "A simple vibecoding exercise"
date: 2025-05-21
author: "ZanSara"
featuredImage: "/posts/2025-05-21-vibecoding/cover.png"
---

{{< audio 
    audioFile="/posts/2025-05-21-vibecoding/A simple vibecoding exercise.mp3" 
    speechifyLink="https://app.speechify.com/share/7ba6f11d-9b76-4334-b85c-f6fe6c02e4ac"
>}}

Sometimes, after an entire day of coding, the last thing you want to do is to code some more. It would be so great if I could just sit down and enjoy some Youtube videos...

Being abroad, most of the videos I watch are in a foreign language, and it helps immensely to have subtitles when I'm not in the mood for hard focus. However, Youtube subtitles are often terrible or missing entirely.

Can the magic of modern Generative AI fix this problem?

We've all heard of [vibecoding](https://x.com/karpathy/status/1886192184808149383): sitting in front of your IDE, telling an AI what you want the code to do and letting it loose to create _something_ that achieves that goal. In this case, the goal is rather simple: given a video file, generate subtitles for it using [Deepgram](https://deepgram.com/)'s SDK (since it has a [generous free tier](https://deepgram.com/pricing)). It seems such a simple task that even an LLM should be able to reach it with minimal or no assistance. Right?

# The first shot: OpenAI

For this simple experiment I decided not to use a dedicated IDE or VSCode plugin, but to stick to text based tools. After all, I expected this task to be sorted with a single Python script made by OpenAI's famed [`o4-mini-high`](https://openai.com/index/introducing-o3-and-o4-mini/), advertized as "Great at coding and visual reasoning".

![](/posts/2025-05-21-vibecoding/openai-model-selector.png)

The prompt was very simple:

> Write me a Python script that, given a video file, returns me an [.srt](https://en.wikipedia.org/wiki/SubRip) subtitle file using Deepgram's API.

As expected, the model thought about it, did some web searches, and then cooked up a script that used `deepgram-sdk` and `deepgram-captions`. Looked good, but as soon as I tried to run it, issues came up. Deepgram's SDK complained about wrong formats, wrong SDK version, HTTP errors... Copy-pasting the errors back to `o4-mini-high` was vain: the model seems to understand that the Deepgram API had a major upgrade since the model was trained, but fails to use the new version. After four or five attempts (including one full restart of the chat), I realized this was going nowhere and I looked for another option.

# The backup option: Claude Code

I've heard many times that the best LLMs for vibecoding belong to the [Claude](https://www.anthropic.com/claude) family. On top of that, there's a cool TUI utility called [Claude Code](https://www.anthropic.com/claude-code) that allows you to vibecode from the terminal, no IDE required. It uses [Claude 3.7 Sonnet](https://www.anthropic.com/claude/sonnet) under the hood, so the expectations are high.

Time to give it a try.

Installing the utility is matter of a single command (`npm install -g @anthropic-ai/claude-code`) and a few emails to authenticate the utility into my Anthropic account. Once done we're ready to go.

![](/posts/2025-05-21-vibecoding/claude-code-intro.gif)

The prompt is the same:

> Write me a Python script that, given a video file, returns me an .srt subtitle file using Deepgram's API.

Sure enough, Claude's first attempt also fails for the same reason as o4 did: their knowledge is outdated, and they both use the Deepgram's API in a way that's not compabible with its new v3 API. However, after a few attempts, Claude actually produces a script that _mostly_ works.

# Results

[Here](https://gist.github.com/ZanSara/4bab5db89376d595128e0688804d694c) is the output (I pasted the `README` and the `requirements.txt` at the top of the file for simplicity). I only needed to replace [`nova-2`](https://developers.deepgram.com/docs/models-languages-overview#nova-2) with [`nova-3`](https://developers.deepgram.com/docs/models-languages-overview#nova-3) to get the best possible transcription for Portuguese (other languages may get better transcription with `nova-2`).

To summarize:
- **Is it perfect? No.** I can easily spot a lot of improvements to the code just by looking at it. It's quite verbose, for example.
- **Was it cheap? No.** This script costed me a few dollars worth of tokens and about half a hour of trial and errors, about the hourly rate of a US software engineer.
- **Is it enough for my purposes? Absolutely.** Now I am finally able to enjoy my videos with good quality subtitles without too much hassle.
- **Could somebody that can't program do this?** I'm not so sure. Given how simple this task was, I was a bit disappointed by how long it took and I am rather skeptical about the ability of today's LLMs to handle more complex requests without oversight - at least with the tools I used.

However, looking at the big picture, the trend is clear. Three years ago, LLMs could just about write coherent sentences. Today, they can write decent helper scripts. Soon the may be able to implement your side projects from start to finish. 

Will it feel like a blessing or a curse? We'll soon find out.



_Edit 22/05/2025: Claude 4 has been released the day after I published this post, so here is a video of myself reimplementing this same script with the new model ✨_


{{< raw >}}
<div class='iframe-wrapper'>
<iframe src="https://drive.google.com/file/d/1cTo-VD8sFYYau900zIwFSCgkxLDt9iWO/preview" width=100% height=100% allow="autoplay"></iframe>
</div>
{{< /raw >}}


<p class="fleuron"><a href="https://www.zansara.dev/posts/2024-05-06-teranoptia/">{z</a></p>

---
title: "PyData Global: Building LLM Voice Bots with Open Source Tools"
date: 2024-12-03
author: "ZanSara"
featuredImage: "/talks/2024-12-03-pydata-global-voice-bots.png"
externalLink: 
---

[Announcement](https://global2024.pydata.org/cfp/talk/T3YDBP/), [slides](https://drive.google.com/file/d/1rXb4-m-BWwhAqDCDBXpzw6nJ9OELOpSl/view?usp=sharing), [demo video](https://drive.google.com/file/d/1bja0O8LG7790UIU7HpAYXat-BYXeUbK-/view?usp=sharing) and full video ([Youtube](https://www.youtube.com/watch?v=Td5dFdG0wE4), [backup](https://drive.google.com/file/d/1HTEEs-Zr8mZoJA8a7AuiJf61soGvQNPI/view?usp=sharing)).
All resources can also be found in 
[my archive](https://drive.google.com/drive/folders/1ZPkne2QxOnSXfchv08CWkAZG3duXxd4Z?usp=sharing).

---
{{< googledriveVideo url="https://drive.google.com/file/d/1HTEEs-Zr8mZoJA8a7AuiJf61soGvQNPI" >}}
---


## Demo

During the talk I showed a recording of a demo built with [Intentional](https://github.com/intentional-ai/intentional), a new library to prompt voice bots in a way that takes inspiration from classic intent-based chatbots. Here are the instructions needed to run this same demo on your own machine and play with it.

{{< notice info >}}

_Intentional is still in its very first stages of development and highly unstable!_

_I am looking for contributors to help this project come to life, so if you would like to help there are many ways to do so: leave a star on [the repo](https://github.com/intentional-ai/intentional), [test the library](https://intentional-ai.github.io/intentional/docs/home/) on your machine, [open an issue](https://github.com/intentional-ai/intentional/issues/new), reach out to me to leave feedback (you can find my contact [on the homepage](/)), [spread the word](https://github.com/intentional-ai/intentional) about Intentional, or even [contribute to the project](https://intentional-ai.github.io/intentional/CONTRIBUTING/) with a PR._

{{< raw >}}
<!-- Place this tag in your head or just before your close body tag. -->
<script async defer src="https://buttons.github.io/buttons.js"></script>
<a class="github-button" href="https://github.com/intentional-ai" data-color-scheme="no-preference: light; light: light; dark: dark;" data-size="large" data-show-count="true" aria-label="Follow @intentional-ai on GitHub">Follow @intentional-ai</a>
<a class="github-button" href="https://github.com/intentional-ai/intentional/subscription" data-color-scheme="no-preference: light; light: light; dark: dark;" data-size="large" data-show-count="true" aria-label="Watch intentional-ai/intentional on GitHub">Watch</a>
<a class="github-button" href="https://github.com/intentional-ai/intentional" data-color-scheme="no-preference: light; light: light; dark: dark;" data-size="large" data-show-count="true" aria-label="Star intentional-ai/intentional on GitHub">Star</a>
{{< /raw >}}

{{< /notice >}}

First, install Intentional and the plugin for [Textual](https://textual.textualize.io/)'s UI:

```bash
pip install intentional intentional-textual-ui
```

{{< notice info >}}

_This demo was only tested on Linux (Ubuntu). You will need `portaudio` in order for Intentional to handle audio from your microphone, so if you face errors during the installation, try:_ `sudo apt install portaudio19-dev`

{{< /notice >}}

Next, you'll need the configuration file where the conversation tree is defined. Intentional bots are, at their core, entirely defined by this configuration file (with the partial exception of tools, as you can see [in the documentation](https://intentional-ai.github.io/intentional/docs/home/)). Download the demo configuration file [from this link](https://drive.google.com/file/d/1dkvxpCH6uny8ew3wrsgh7SPZdqvKuTyd/view?usp=sharing) and save it as `demo.yml`.

Now, make your OpenAI API key available to the CLI:

```bash
export OPENAI_API_KEY=<your api key>
```

Now you're ready to run the bot. Intentional comes with a simple CLI that can directly run bots from a config file and draw their conversation graph. To run the bot and talk to it as shown in the video, run:

```bash
intentional demo.yml
```

You should see a UI such as this coming up (with the chat history empty):

![](/talks/2024-12-03-pydata-global-voice-bots-demo-ui.png)

Just start speaking and the bot will quickly reply to you. 

{{< notice info >}}

_Occasionally the transcriptions don't work well. The bot is generating such transcriptions exclusively for your convenience, so even if they're mangled, in most cases you can be confident that the model actually heard you well._

{{< /notice >}}

To see the conversation graph, run this command:

```bash
intentional demo.yml --draw
```

The PNG file will be created next to `demo.yml` and will be called `demo.png`.






---
title: "Reasoning effort defaults across the GPT-5.x family"
description: "If you never pinned the reasoning effort across model upgrades, you may have accidentally changed your reasoning effort dramatically."
date: 2026-05-26
author: "ZanSara"
featured-image: "cover-inv.png"
---

GPT-5.x models are [reasoning models](https://magazine.sebastianraschka.com/p/understanding-reasoning-llms), and as such, you can set the reasoning effort that they should make when addressing your prompts.

Reasoning is a big part of what makes LLMs smarter or faster, and the reasoning effort is a huge lever to improve benchmark results and latency figures. However, unless you've been monitoring your LLM applications closely, you may not have found a reason to play too much with the reasoning effort, trusting that the default would be good enough for now.

Unfortunately, for some of us this is not a safe assumption to make.

## The default keeps changing

The problem is that OpenAI is **not keeping the default stable**. Reasoning itself have been turned on and off a few times across gpt-5.x releases:

- GPT-5: `medium` ([source](https://developers.openai.com/api/reference/java/resources/%24shared#(resource)%20%24shared%20%3E%20(model)%20reasoning_effort%20%3E%20(schema)))
- GPT-5.1: `none` ([source](https://developers.openai.com/api/docs/models/gpt-5.1))
- GPT-5.2: `none`([source](https://developers.openai.com/api/docs/models/gpt-5.2))
- GPT-5.4: `none` ([source](https://developers.openai.com/api/docs/models/gpt-5.4))
- GPT-5.5: `medium` ([source](https://developers.openai.com/api/docs/models/gpt-5.5))

This means that, unless you manually set the reasoning effort, you lost reasoning when upgrading from GPT-5 to GPT-5.1, sacrificing some output quality for faster responses. On the opposite, when upgrading from GPT-5.4 to GPT-5.5, the opposite happened: you traded off latency for some additional intelligence. 

If you're building simple chatbots, this distinction may not matter at all; but if you're building voice applications and other apps that require low-latency responses, this upgrade might have thrown a wrench in your numbers unexpectedly. GPT-5.5 is not necessarily this slow: you can make it run as fast as its predecessor, and keep the improved intelligence, by setting back the reasoning to where you want it to be.

## Picking the right reasoning effort

Choosing the right reasoning effort depends entirely on your preference for intelligence vs speed. This is what the official [OpenAI guidelines](https://developers.openai.com/api/docs/guides/reasoning) report on the matter:

| Reasoning effort | Intended use                                                                                                                                          | Typical tradeoff                                                         |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `none`           | Latency-critical tasks that do not benefit from reasoning or multi-step tool calls. Examples: voice, fast retrieval, classification.                  | Fastest, lowest reasoning overhead, weaker for planning/tool-heavy work. |
| `minimal`        | Fast responses on GPT-5 models that support it.                                                                                                       | Very low reasoning overhead; availability is model-dependent.            |
| `low`            | Efficient reasoning for tool use, planning, search, multi-step decisions, drafting, data analysis, execution-oriented coding, support/chat workflows. | Modest latency/token increase. Often a safer floor than `none`.          |
| `medium`         | General default for quality/reliability, planning, judgement, agentic coding, research, spreadsheets/slides, longer delegated tasks.                  | Balanced quality, latency, and cost. `gpt-5.5` defaults to this.         |
| `high`           | Hard reasoning, complex debugging, deep planning, high-value agentic tasks.                                                                           | Better quality on difficult tasks, higher latency/cost.                  |
| `xhigh`          | Deep research, long rollouts, challenging coding/security/code-review workflows where evals prove value.                                              | Highest latency/cost; should be justified by evals.                      |

In many cases the reasoning effort should be raised, at the expense of latency, on very tough tasks that require thinking. Agentic coding is a typical example. For all other scenarios you can save money and reduce latency by keeping the reasoning effort low, and setting up an eval framework to check whether your benchmarks are still healthy.
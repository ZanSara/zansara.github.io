---
title: "What's an agent harness?"
description: "The intelligence of modern AI agents is due to the LLMs, but their practical capabilities only exist thanks to their harness."
date: 2026-06-12
author: "ZanSara"
series: ["Practical Questions"]
featured-image: "cover-inv.png"
---

---

_This is episode 9 of a series of shorter blog posts answering questions I received during the course of my work. They discuss common misconceptions and doubts about various generative AI technologies. You can find the whole series here: [Practical Questions](/series/practical-questions)._

---

The term "agent harness", or even simply "harness", seemingly appeared out of nowhere at some point at the start of this year, and everybody immediately started using it as if it had always had an obvious and commonly understood definition. If this caught you off guard, you're not alone: the term has existed since before LLMs, but it was a rather niche AI research term that only went mainstream in early 2026.

## Definition

In short, an agent harness is **all the software scaffolding that sits around an LLM**. The harness is the software that manages how the LLM uses tools, remembers context, stays within its guardrails, etc. To use a simple metaphor, the LLM is the brain of the AI agent: it understands, reasons, makes decisions, etc. The harness is its body: it takes actions, receives feedback from the environment, etc. Without its harness, the LLM can talk about a solution and explain it, but cannot put it into practice. That part is the harness's task.

In fact, the LLM and its harness have such orthogonal roles that they are not tied to each other: nearly any LLM can be used with any harness, depending on the end goal. Harnesses are LLM-agnostic and can work with any LLM, which makes it easier to upgrade the LLM without rebuilding the harness, and vice versa.

![](agent-harness-inv.png)

In more practical terms, the primary component of an agent harness is **tools**. LLMs on their own are not able to run tools: they *request* a tool execution from their harness, the harness executes the tool, whether directly or through an MCP, collects the outputs, then invokes the LLM again with the outputs of the tool. This machinery is one of the most basic forms of harness.

Another example is **long-term memory**. There are plenty of [implementations of memory](/posts/2026-02-04-how-does-llm-memory-work/), but none of them is a native capability of the LLM: they are all part of the harness, and must be implemented in the scaffolding around the model for the model to acquire this capability. For example, one simple form of memory is the "scratchpad" approach, where the LLM can take notes about what it should remember long-term. This scratchpad is external to the LLM, just like a notebook is external to your head: the LLM writes into its scratchpad using a tool, and the harness makes sure to register the edits, store its content, inject it into the chat history at every new chat, etc.

Some forms of **guardrails** are also implemented in the harness. One common and simple implementation of a guardrail is to make each prompt go through two LLMs instead of one: the first to actually answer the question, and the second to review the answer, to make sure it addresses the prompt without breaking any guardrails in the process. Again, this workflow is not native to any LLM: it must be implemented around the LLM call.

In addition, the harness is the perfect place to introduce **observability**: monitoring, logging, error handling, and other scaffolding that's essential for production-grade systems.

## Why a term for this?

These sorts of scaffolds are not new. They've been around for a very long time: in fact, the term seems to come from 2020, long before LLMs, when researchers started to study the relationship that an AI system could develop with external software. However, the term definitely gained a ton of popularity and escaped the research domain some time at the end of 2025.

Late 2025 was also the time when agentic coding started to really take off. Coincidence?

It is now generally understood that coding agents require two parts to be effective: an excellent LLM that is able to invoke tools effectively, and an excellent harness that gives the LLM exactly what it needs to do its work, nothing more and nothing less. A state-of-the-art LLM in a poor harness will perform well below its potential, while a rather poor LLM placed in a great harness will punch above its weight. 

While agent harnesses are an essential part of every type of AI agent, they're usually called like this in the context of coding agents. For example, Claude Code is an agent harness, and Claude is its LLM. Cursor is a harness which can use several different LLMs under the hood. But OpenClaw is also a harness, which can also be powered by different LLMs.

## In conclusion

There are two situations where it's important to understand the concept of harness:

1. You use coding agents. Understanding the distinction between the LLM's own capabilities and the role of the surrounding harness is very useful to debug situations where the agent performs unexpectedly poorly. For example, the LLM has no idea whether it's running on Windows, Linux, or a Mac: the harness has to tell the LLM this, so the LLM can issue the correct CLI commands.

2. You are building AI agents. In this case, it's essential to know what kind of features and failure modes are due to the harness and what kind are due to the model. It's also crucial to be able to evaluate the LLM and the harness components in isolation and as a complete system, keeping in mind how the two parts influence each other's abilities.

Either way, as the word becomes more and more popular, it's now an essential term to keep in mind when reasoning about AI agents.
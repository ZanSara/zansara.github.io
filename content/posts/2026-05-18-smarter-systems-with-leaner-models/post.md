---
title: "Smarter Systems with Leaner Models"
description: "Token prices keep falling with every new model release. So how come AI bills are only raising? Is it structural, or there's a way to help it?"
author: "ZanSara"
date: 2026-05-18
featured-image: "/posts/2026-05-18-smarter-systems-with-leaner-models/cover-inv.png"
---

---

_This post is a writeup of my talk at [The Economist's Impact 2nd AI Compute Summit](ttps://events.economist.com/ai-compute/programme/#day1+cat-10+smarter-systems-leaner-models-reducing-compute-costs-without-sacrificing-quality). You can find the slides [here](/talks/2026-05-19-ai-compute-summit)._

---

LLMs keep getting smarter, month by month. But they also get bigger, more hardware and resource intensive, more difficult to run efficiently, and even if token costs keep getting slashed, the AI bills of most companies just goes up.

Is it still possible to build state of the art AI application while keeping cost under control?

Let's have a closer look at what's happening here, and dive deeper into a few approaches to limit your spending without affecting the performance of your AI applications.

## The fundamental problem

AI economics have moved past the simple question of whether a model is "big enough." The more useful question is whether each workflow is buying the right amount of intelligence, context, latency, and reliability for the job. In other words: the relevant unit is no longer raw model size. It is **cost per quality outcome**.

That distinction is becoming essential, because the two headline trends in AI economics now point in opposite directions. On one side, there's a famous figure: the Stanford AI Index reports that the inference cost for a system performing at GPT-3.5 level dropped more than **280-fold** between November 2022 and October 2024.[^stanford-2025]. And while GPT-3.5 may seem a thing of the past, Gartner also forecasts that by 2030 the price of a 1T-sized model (what most flagship LLMs are estimated at) will fall by more than 90%[^gartner-2030]. On the other, Gartner forecast worldwide GenAI spending of roughly $644 billion in 2025, up 76.4% from 2024[^gartner-genai-spend-2025], and Stanford also reports corporate AI investment of $252.3 billion in 2024, with private investment up 44.5%. [^stanford-2025-economy] The lesson here is that unit costs can fall while total usage expands even faster.

That's only natural, once we zoom out a little: increased intelligence unlocks use cases that were not possible with earlier models, therefore increasing usage. GPT-3.5 could not be used for agentic coding; GPT-5.5 can do most of the coding that software engineers used to do just last year.

This doesn't mean that we should let costs and resource utilization go out of control. A little architecture discipline and governance can keep broader deployment from outrunning token-price deflation.

## AI overspending is a system design issue

Right now, overwhelmed by hype and FOMO, a lot of developer teams simply default to a set of common, safe assumptions, that are sure to work with all LLMs. That was understandable while teams were still learning what generative AI could do, but it is increasingly hard to justify at scale. The lack of understanding of the capabilities and requirements of modern LLMs is one of the key drivers of overspending on AI workflows.

Spotting them is not always easy, but some are much easier to address than others. My recommendation is to look for them in this order:

1. **Context Engineering**: are you sending too many tokens to your LLM, when half or less would do?
2. **Right-Sizing**: are you using the smallest LLM that can carry out your specific workflow as well as a flagship model? 
3. **Inference Engineering**: are you getting the most out of your hardware, or at least as much as a commercial provider would?
4. **Silicon Strategy**: are you really at a point where GPUs are not enough for your usecase?

Let's unpack them.

## 1. Context Engineering

Anthropic defines context engineering as the work of curating and maintaining the optimal set of tokens available to the model across system instructions, tools, external data, message history, and other context state.[^anthropic-context-2025]

This is because no input is free when it comes to an LLM. 

This is often underestimated by AI builders. Every additional instruction and example, every additional corner case, every new document, image or tool added to the LLM context raises the cost of **each** of the prompts and responses of your AI. When the LLM context is stuffed by thousands of PDFs, even a three question answer will cause the LLM to reread everything, costing you several dollars, if not tens of dollar, for each back-and-forth.

Unnecessary input is not only damaging your wallet. It and also adds latency, cost, and diluites the model's attention. In short, this means: try to identify the **shortest context that preserves answer quality**.

This is where retrieval-augmented generation, prompt caching, and compression come in. 

**RAG** is often essential to lead the LLM to the answer without dumping millions of tokens at it. Microsoft describes token constraints as a core RAG challenge: RAG pipelines should return concise, highly relevant chunks rather than exhaustive document dumps.[^ms-rag-2026] 

**Caching** can also help noticeably. Anthropic's prompt-caching documentation positions caching as a way to reduce processing time and cost for repetitive prefixes, with cache-read tokens priced at 0.1x base input tokens in the cited Claude pricing table.[^claude-prompt-caching-docs]

Applications where there are lenghty back-and-forth with users, such as agentic coding, also benefit from **chat history compression**, where older consersation turns, RAG snippets, tool outputs etc are summarized instead of stored verbatim, to occupy less space in the context window.

To leverage these context engineering techniques, every major AI workflow should have a context budget. Track input tokens, output tokens, cached tokens, retrieval hit rate, cache hit rate, against output quality. If a customer-service workflow needs a policy excerpt and the last three turns, do not send the whole knowledge base and the entire conversation every time.

## 2. Right-sizing

Right-sizing does not mean simply choosing the smallest model. It means choosing the cheapest model that meets the workflow's service-level agreement for quality, latency, risk, and trust. 

Flagship models such as GPT-5.5, Claude Opus 4.7, etc are not always the right answer for your usecase. They are increasingly benchmarked against problems that are not within the realm of what most businesses use them for, such as PhD level math, complex algorithmic challenges, advanced physics and scientific discovery, not for simple question answering against a company's knowledge base, or chatting in real time with a person on the phone, or planning a business trip. There are other, leaner models, much better suited for such tasks.

In fact, choosing a smaller model is not only a cost saving technique. Smaller models occasionally display better stats at crucial skills, such as lower hallucination rates, than flagships.[^vectara-hallucination-blog][^vectara-hallucination-github] This is because flagships, being trained for the highest intelligence, tend to guess, infer, deduce from the data they have available, while the smaller models are just trained to admit ignorance. This makes them *better* suited for many industry applications while costing 5 to 10 times less than their smarter counterparts.[^openai-pricing-2026][^google-pricing-2026][^anthropic-pricing-2026]

![Right-sizing economics: list-price token cost compared with Vectara hallucination rates.](/posts/2026-05-18-smarter-systems-with-leaner-models/right-sizing.png)

_A comparison of the cost for a million token versus the hallucination rates of three popular flagship LLMs and their smaller counterparts._

That does not prove a small model is better for every workflow. It proves the opposite of the old default: you cannot infer the right model from size alone.

The research trend supports this. For example, Microsoft Research reports that fine-tuned small language models can act as enterprise search relevance labelers with human-judgment agreement on par with or better than a teacher LLM, while improving throughput by 17x and cost-effectiveness by 19x in their experiment.[^ms-slm-labelers-2026]

To right-size your applications, you should benchmark one or two smaller candidates against your own business KPIs. Do not trust generic leaderboards: measure against your own, real usage patterns. Check containment, false positives, deflection quality, escalation rate, p95 latency, cost per successful task, customer satisfaction, and any other metric that might matter for your use case.

### An example: flagships as managers of smaller workers

Routing and cascading can turn a rigid model selection choice into a more flexible, dynamic architecture that self-selects the best model for each task. 

A router (which may be an LLM as well) sends easy or known intents to cheap specialists, escalates uncertain work to stronger models, and reserves frontier models or humans for high-stakes cases. Research on routing and cascading shows that model-selection strategies can improve the cost-performance trade-off by choosing a single model per query or sequentially escalating until a satisfactory answer is found.[^routing-cascading-2024]

The question is therefore not "AI or humans?" It is: **What escalation tree gives the best unit economics without damaging trust?** A good routing system should include explicit thresholds for uncertainty, regulatory sensitivity, customer emotion, financial impact, and human override. The router itself should be measured as a product: containment is not success if escalations arrive too late.

## 3. Inference engineering

Once context and routing are under control, the next savings come from inference engineering. This is an active research area that needs to be followed closely if competition is a threat, and requires a non-negligible level of dedication to be done right. While most techniques are now available to everyone with limited effort, whomever manages to implement the latest, most complex optimizations will end up having an edge in terms of either cost or latency.

When talking about inference engineering is always worth framing it as a build-or-buy decision. Is it better to invest in an inference stack, with dedicated hardware, dedicated team, dedicated budget etc, or to buy compute from a commercial provider such as OpenRouter, Nebius, Fireworks, etc? The choice is not always trivial and may be influenced by other factors, such as data protection constraints, governance rules, etc. 

For some of us, keeping inference in-house is not negotiable, and therefore the realm of inference engineering is highly relevant. In these cases, start from the most basic optimizations such as prompt caching and batching, then move up the complexity scale with cache and model quantization, up to cutting edge techniques such as speculative decoding and more, keeping a constant eye on the state of the art as it progresses.

![Inference engineering quadrant: quick wins first, strategic bets second.](/posts/2026-05-18-smarter-systems-with-leaner-models/inference.png)

_A simplified maps of some of the inference optimizations techniques that can help your organization get the most out of the hardware, classified by their complexity versus their impact._

In short provider choice, serving stack, and model choice are intertwined. The same open model can feel very different across inference providers and stacks because the serving path differs. That is why mature AI companies benchmark latency, cost, and quality together on different stacks before settling on an inference strategy.

## 4. Silicon Strategy

More GPUs will only bring you so far, and the industry is actively looking for alternatives. Specialized inference hardware is a still immature, but hot research area: new chips could change the economics of AI if they manage to move from prototype to production, especially for predictable workloads, but evidence quality varies widely. Some numbers are vendor-reported, some come from early demonstrations, and many compare different models, sequence lengths, or serving configurations.

![Silicon throughput landscape using mixed vendor and benchmark sources.](/posts/2026-05-18-smarter-systems-with-leaner-models/silicon.png)

_A simplified comparison of a crucial claim for custom LLM chips: tokens per second on selected LLMs (usually Llama models)._

Taalas positions its approach as turning models into custom silicon and claims that its "Hardcore Models" are 1000x more efficient than software counterparts.[^taalas-home] Its HC1 product page says the demonstrator runs Llama 3.1 8B and delivers 17k tokens per second per user, while also making clear that the comparison chart combines Taalas measurements with NVIDIA baseline and Artificial Analysis sources.[^taalas-products] Forbes/Cambrian-AI coverage amplified the HC1 performance narrative, but this remains a case where procurement teams should treat claims as directional until they are independently reproduced on their own workloads.[^forbes-taalas-2026]

Cerebras provides a more concrete example of high-throughput inference at large scale: it reported Llama 3.1 405B running at 969 output tokens per second on Cerebras Inference, with 240 ms time to first token, in a result it says was measured by Artificial Analysis.[^cerebras-405b-2025] Etched's Sohu is another example of the specialization trade-off: The Register reported Etched's claim of 500,000 tokens per second for an eight-chip Sohu server running Llama 70B, while also noting that the chip had not taped out at the time of that report.[^etched-register]

This is why specialized silicon is still a rather hypothetical concern for most organizations. First, capture context, routing, and serving savings. Then use silicon options as negotiation leverage and roadmap planning. 

## Prototype fast, ship lean

The winning pattern is two-speed. Use frontier models for discovery, then industrialize with smaller, routed, cached, and optimized systems.

In the **exploratory** stage, use frontier or generalist models to learn what the product should do. This de-risks interaction design, customer value, and task fit quickly. In the **refinement** stage, freeze the task taxonomy, right-size models, enforce context budgets, and deploy routing and caching. In the **scale** stage, re-asses your inference options now that all other variables are under control and overall cost is more predictable. Evaluate specialized hardware only when the economics justify it.

## Where to start?

Most organization can start from these three simple actions

1. **Measure token usage.** Instrument token telemetry; identify top cost drivers before changing models.
2. **Benchmark small models.** Don’t rely on generic benchmarks, measure them against your business KPIs.
3. **Optimize serving layer.** Make sure you’re getting the most out of your hardware or inference provider.

Stop buying intelligence by habit. Stop treating the model as the system. Preserve user trust while lowering the cost of each successful outcome.

The next phase of AI competition will not be won by the company that uses the largest model most often. It will be won by the company that knows where intelligence is truly needed and designs the system around that fact.

## References

[^stanford-2025]: Stanford HAI, "The 2025 AI Index Report" (2025). https://hai.stanford.edu/ai-index/2025-ai-index-report
[^stanford-2025-economy]: Stanford HAI, "Economy | The 2025 AI Index Report" (2025), including corporate investment, private investment growth, and organizational AI use figures. https://hai.stanford.edu/ai-index/2025-ai-index-report/economy
[^gartner-genai-spend-2025]: Gartner, "Gartner Forecasts Worldwide GenAI Spending to Reach $644 Billion in 2025" (Mar. 31, 2025). https://www.gartner.com/en/newsroom/press-releases/2025-03-31-gartner-forecasts-worldwide-genai-spending-to-reach-644-billion-in-2025
[^gartner-2030]: Gartner, "Gartner Predicts That by 2030, Performing Inference on an LLM With 1 Trillion Parameters Will Cost GenAI Providers Over 90% Less Than in 2025" (Mar. 25, 2026). https://www.gartner.com/en/newsroom/press-releases/2026-03-25-gartner-predicts-that-by-2030-performing-inference-on-an-llm-with-1-trillion-parameters-will-cost-genai-providers-over-90-percent-less-than-in-2025
[^anthropic-context-2025]: Anthropic Engineering, "Effective context engineering for AI agents" (Sep. 29, 2025). https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
[^claude-prompt-caching-docs]: Anthropic Docs, "Prompt caching." https://docs.claude.com/en/docs/build-with-claude/prompt-caching
[^ms-rag-2026]: Microsoft Learn, "Retrieval-augmented generation (RAG) in Azure AI Search." https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
[^openai-pricing-2026]: OpenAI, "API Pricing." https://openai.com/api/pricing/
[^google-pricing-2026]: Google AI for Developers, "Gemini API Pricing." https://ai.google.dev/gemini-api/docs/pricing
[^anthropic-pricing-2026]: Anthropic, "Plans & Pricing." https://www.anthropic.com/pricing
[^ms-slm-labelers-2026]: Microsoft Research, "Fine-tuning Small Language Models as Efficient Enterprise Search Relevance Labelers" (arXiv abs/2601.03211, 2026). https://www.microsoft.com/en-us/research/publication/fine-tuning-small-language-models-as-efficient-enterprise-search-relevance-labelers/
[^routing-cascading-2024]: arXiv, "A Unified Approach to Routing and Cascading for LLMs" (2024/2025). https://arxiv.org/abs/2410.10347
[^taalas-home]: Taalas, company site and product positioning. https://taalas.com/
[^taalas-products]: Taalas, "Products" / HC1 technology demonstrator. https://taalas.com/products/
[^forbes-taalas-2026]: Forbes / Cambrian-AI, Karl Freund, "Taalas Launches Hardcore Chip With 'Insane' AI Inference Performance" (Feb. 19, 2026). https://www.forbes.com/sites/karlfreund/2026/02/19/taalas-launches-hardcore-chip-with-insane-ai-inference-performance/
[^cerebras-405b-2025]: Cerebras, "Llama 3.1 405B now runs at 969 tokens/s on Cerebras Inference." https://www.cerebras.ai/blog/llama-405b-inference
[^vectara-hallucination-blog]: Vectara, "Introducing the Next Generation of Vectara's Hallucination Leaderboard." https://www.vectara.com/blog/introducing-the-next-generation-of-vectaras-hallucination-leaderboard
[^vectara-hallucination-github]: Vectara, "Hallucination Leaderboard" GitHub repository. https://github.com/vectara/hallucination-leaderboard/
[^etched-register]: The Register, "Etched scores $120M for an ASIC built for transformer models" (Jun. 26, 2024). https://www.theregister.com/software/2024/06/26/etched-scores-120m-for-an-asic-built-for-transformer-models/679326

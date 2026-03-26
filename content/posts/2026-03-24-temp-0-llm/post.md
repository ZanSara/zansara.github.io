---
title: "Setting the temperature to zero will make an LLM deterministic?"
description: "We all know LLMs don't always respond the same thing to slight changes of prompt. But why does their answer differ also when the prompt is identical? And what can we do to prevent it?"
date: 2026-03-24
author: "ZanSara"
series: ["Practical Questions"]
featured-image: "/posts/2026-03-24-temp-0-llm/cover-inv.png"
---

---

_This is episode 8 of a series of shorter blog posts answering questions I received during the course of my work. They discuss common misconceptions and doubts about various generative AI technologies. You can find the whole series here: [Practical Questions](/series/practical-questions)._

---

One common explanation of the "temperature" parameter of LLMs is that it represents the "randomness" of the answer. 

That's broadly correct. Temperature is a parameter of the LLM final decoding steps, and the only one in the whole Transformer architecture that truly incorporates some randomness by design. At this stage, once the model has calculated the logits of the next token candidates, it has to map those values to an actual token from a list. Normally, LLMs perform best when they’re allowed to pick not necessarily the single best token, but instead choose at random among the N best tokens: the size of N is, more or less, what the temperature parameter represents.

Therefore, when we set the temperature to 0, the LLM must always choose the best next token, without making random choices. So, if the input is fixed and we have removed the only source of randomness in the architecture, the outputs should always be identical... right?

And yet, in practice, they often are not. Run the same prompt twice, with the same model, the same parameters, and temperature 0, and sooner or later the output will be a bit different. Not by much, usually. It may start with just one word; then the sentence takes a slightly different spin, until eventually the rest of the completion drifts away.

What's going on?

## Imperfect computations

If we pretend an LLM is just a mathematical function, `temperature=0` should indeed make decoding deterministic. At each step, the model emits logits, we take the argmax token, append it to the context, and repeat. The problem is that real inference is performed with **floating-point arithmetic** on massively parallel hardware, usually on a server that is trying to be as fast as possible rather than mathematically pristine.

Floating-point arithmetic is only an approximation of real-number arithmetic. In particular, it is **not associative**: in ordinary math, `(a + b) + c = a + (b + c)` always holds, but with floating-point numbers those two expressions can produce slightly different results because each intermediate step is rounded. The same applies to matrix multiplications, reductions, and accumulations throughout a neural network. Change the order of operations, and you can change the last few bits of the result.

Usually, those differences are tiny and often irrelevant, but in this case they have an impact. If two candidate next tokens have very similar logits, a minute numerical difference can swap their order, and once one token changes, the next decoding step runs on a different prefix, so the divergence compounds. The sampling rule is deterministic, while the computation that produced the logits is not guaranteed to be identical across runs.

You can think of it this way: **sampling determinism** is not the same thing as **system determinism**.

## It gets worse

However, this is only part of the problem. You may already be objecting that running the same matrix multiplication on a GPU with the same data repeatedly will always provide bitwise-identical results. The computations are done in floating-point arithmetic, and there are surely other jobs running on the GPU while your computer is on. So why are these calculations deterministic, while LLM sampling with `temperature=0` is not?

In a recent post on Thinking Machines's blog, [*Defeating Nondeterminism in LLM Inference*](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/), Horace He's digs even deeper into the issue. It's not merely that floating-point arithmetic is imperfect. Modern inference systems also need to batch requests together, and the result for one request can depend on the batch context in which it was executed. For a given exact batch, the forward pass may be deterministic. But from the user's point of view, the system is still nondeterministic, because the batch itself is not stable from run to run. Your prompt may be identical, but the inputs that get batched together with yours are not.

This is also why a prompt can look stable in local testing and then become flaky in production: the model did not suddenly become more creative, it's the system conditions that changed. `temperature=0` makes only the token selection rule deterministic. It does not guarantee that the entire inference system will produce exactly the same logits every time.

## Can it be fixed?

The way LLMs inference works today, especially at scale, doesn't leave us with many options to enforce the conditions that can guarantee deterministic outputs. There are only trade-offs, and they differ quite a lot between hosted APIs and self-hosted inference.

### Fixed seeds

To reduce randomness and make LLM outputs reproducible, some people recommend using a fixed seed, and indeed some providers expose one. OpenAI, for example, [documents](https://developers.openai.com/cookbook/examples/reproducible_outputs_with_the_seed_parameter) a `seed` parameter and says it makes a best effort to sample deterministically, while explicitly warning that determinism is not guaranteed and that backend changes can still affect outputs. Their `system_fingerprint` field exists precisely so you can notice when the underlying serving configuration has changed.

The problem with fixed seeds is that they help reproduce results when the temperature is above zero, not when it's already zeroed out. That's because a fixed seed controls the randomness of the sampling step: by setting the temperature to zero, we are already removing that source of randomness, so the net result is identical with or without a fixed seed, while every other source of nondeterminism coming from the GPU and the rest of the stack is unaffected.

So fixed seeds are worth using when you are trying to get the same results for a call with non-zero temperature, such as for tests, demos, and regression checks. But you must keep in mind that they affect only the sampler, and they won't help you when temperature is zero.

### No parallel jobs

If you self-host, one option to drastically reduce randomness is to reduce or eliminate concurrency.

This works for the simple reason that it stabilizes batching and scheduling. vLLM's [reproducibility guidance](https://docs.vllm.ai/en/latest/usage/reproducibility) says that by default it does not guarantee reproducibility on its own. In offline mode, you should disable multiprocessing to make scheduling deterministic, while in online mode, you need batch invariance support if you want outputs that are insensitive to batching. vLLM also documents batch invariance as a distinct feature and notes that it currently depends on specific hardware support.

This means that you can pick a few different configurations, depending on your needs:

* shared online serving with dynamic batching: fastest, cheapest, least reproducible
* isolated worker / no concurrent jobs: slower, more expensive, more reproducible
* specialized batch-invariant serving paths: better reproducibility, but with hardware and feature constraints

The overall pattern is that the more you optimize for throughput, the more reproducibility suffers.

### Cache responses

Caching doesn't exactly address the reproducibility issue per se, but in many applications it's the right level of abstraction if you want the same input to produce the same output. It's often not only the most viable option, but also the cheapest, simplest, and fastest, unless you're running a benchmark or an evaluation.

In practice, if you just need the *same visible result* for the same request, the most reliable method is not to regenerate it at all. Normalize the prompt, model ID, and relevant parameters into a cache key, store the first successful response, and serve that on subsequent identical requests. This does not make the model deterministic, of course, but it does make your *application* deterministic at the interface boundary, which is usually what application builders need.

Caching also has a very nice advantage over seeds and scheduler tricks: it does not depend on hidden implementation details inside the inference stack.

Of course, caching has limits. It only helps when requests repeat, and it can become awkward if tool calls, timestamps, external retrieval, or hidden context make two apparently identical requests not truly identical. Still, it is usually far more convenient than any other solution to this problem, and the only practical one for most production systems.

## Conclusion

When faced with LLM nondeterminism, there's often the reaction to treat it like a bug and to try to eliminate that. However, you should also keep in mind that LLMs were designed with a randomness factor built-in for a reason: because they perform much better when they are allowed a slight degree of nondeterminism.

I get it: nobody likes having such a huge, random black box at the core of an application's business logic. But removing randomness from the outputs is not the right way to manage an LLM's behavior. If you need completely deterministic output, it is better to use the LLM to design a decision tree (or a more sophisticated model, if needed) and then use that in your application.

Handling LLM outputs is rather matter of validation. Use schemas and validators so small textual drift does not break downstream code. Use evals instead of spot-checking. Cache where consistency matters, or where you need to save a few bucks. In other words, handle the randomness at the system boundary rather than trying to remove it from the model itself.

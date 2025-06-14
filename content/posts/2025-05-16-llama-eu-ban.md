---
title: "Using Llama Models in the EU"
date: 2025-05-16
author: "ZanSara"
featuredImage: "/posts/2025-05-16-llama-eu-ban/cover.png"
---

{{< audio 
    audioFile="/posts/2025-05-16-llama-eu-ban/Using Llama Models in the EU - Sara Zan.mp3" 
    speechifyLink="https://app.speechify.com/share/a3c834c1-2832-4b5e-8f3b-27ae94f33dfe"
>}}

[The Llama 4 family](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) has been released over a month ago and I finally found some time to explore it. Or so I wished to do, until I realized one crucial issue with these models:

**They are banned in the EU.**

Apparently Meta can’t be bothered to comply with EU regulations on AI, and therefore opted for a wide ban that should prevent such laws to apply to them. Of course, while this limitation is technically valid for each and every person and company domiciled in the EU, the problem arises primarily for companies that want to use Llama 4 to offer services and for researchers planning to work with these models, be it for evaluation, fine-tuning, distillation or other derivative work. Always keep in mind that I’m not a lawyer, so nothing of what I’m writing here constitutes as legal advice.

# The terms

The interesting part of this ban can be found by reading the [terms](https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md) of the Acceptable Usage Policy (AUP):

> With respect to any **multimodal models** included in Llama 4, the rights granted under Section 1(a) of the Llama 4 Community License Agreement are not being granted to you if you are an individual domiciled in, or a company with a principal place of business in, the European Union. 

As you can see, the restriction applies strictly to multimodal LLMs. Llama4 models are all multimodal, and that’s why the entire family of models is not accessible from the EU. However, if anyone releases a derivative model that is not multimodal, in theory the ban would not apply. I’m yet to see any such derivative model: if you know of any, let me know!

Interestingly, the terms also state that:

> This restriction does not apply to end users of a product or service that incorporates any such multimodal models.

So if you’re a company outside of the EU and provide services based on Llama4 to EU customers, you’re probably off the hook. Such interpretation seems to be confirmed by [Meta’s FAQ](https://www.llama.com/faq/) about Llama models, which state:

> **Can a non-EU based company develop a product or service using the Llama multimodal models and distribute such product or service within the EU?**

> Yes, if you are a company with a principal place of business outside of the EU, you may distribute products or services that contain the Llama multimodal models in accordance with your standard global distribution business practices [...]

[Meta’s FAQ](https://www.llama.com/faq/) are actually quite throughout, so if you have any doubt about your specific case you should head there and read more.

# What about other Llamas?

This wide EU ban is not new: it was introduced with [Llama 3.2 Vision](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/), the first multimodal model released by Meta. The clause does not exist for any model older than Llama 3.2.

To summarize, here is a list of which models can be used in the EU:

- Llama 4: all banned because they're all multimodal ([terms](https://github.com/meta-llama/llama-models/blob/main/models/llama4/USE_POLICY.md))
- Llama 3.3: allowed because it's not multimodal ([terms](https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/USE_POLICY.md))
- Llama 3.2: text only models are allowed, vision models are not allowed ([terms](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/USE_POLICY.md))
- Llama 3.1 and earlier: allowed because there's no such clause ([terms](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/USE_POLICY.md))

So for now this is the state of Llama licenses. My take is that with the implementation and rollout of the EU AI Act in 2025 and 2026, Meta will eventually adapt to make sure that the models are compliant with the way the Act is enforced in practice and relax, if not lift, the ban on newer models.

Also, Llama4 has not been shining in the [benchmarks](https://lmarena.ai/?leaderboard) (scroll down, I promise you it’s there)... we Europeans may not be missing much.

<p class="fleuron"><a href="https://www.zansara.dev/posts/2024-05-06-teranoptia/">AZ*</a></p>
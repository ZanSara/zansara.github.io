---
title: "The Agent Spectrum"
date: 2024-05-29
author: "ZanSara"
tags: [AI, LLM, RAG, Agents, "Autonomous Agents"]
featuredImage: "/posts/2024-05-30-the-agent-spectrum/cover.png"
draft: true
---

The concept of Agent is one of the most confusing out there in the post-ChatGPT landscape. The word has been used to identify systems that seem to have nothing in common with one another, from complex autonomous research systems down to a simple sequence of two predefined LLM calls. Even the distinction between Agents and techniques such as RAG and prompt engineering seems blurry at best.

Let's try to shed some light on the topic by understanding just how much the term "AI Agent" covers and set some landmarks to better navigate the space.

## Defining "Agent"

The problem starts with the definition of "agent". For example, [Wikipedia](https://en.wikipedia.org/wiki/Software_agent) reports that a software agent is

>  a computer program that acts for a user or another program in a relationship of agency.

This definition is extremely high-level, to the point that it could be applied to systems ranging from ChatGPT to a thermostat. However, if we restrain our definition to "LLM-powered agents", then it starts to mean something: an Agent is an LLM-powered application that can take actions to accomplish its goals. Here we see the difference between an agent and a simple chatbot, because a chatbot can only talk to a user without the freedom to take any action on their behalf.

In order to understand them, we can define Agents as software systems that does something on behalf of someone or something else with a goal in mind. An Agent is a system you can delegate tasks to. 

The main property of an Agent is _agency_: Agents have a goal to accomplish and also the means to perform actions to accomplish it. An LLM powered application can be called an Agent when it needs to take decisions and perform actions in order to achieve the goals set by the user, and to do so on their behalf, with no or limited supervision.

## Autonomous Agents vs Conversational Agents

On top of this definition there's an additional nuance to take into account: some LLM apps may look like agents only from the perspective of some of the parties involved, but not all. Incidentally, this distinction is normally brought up by the terms "conversational" and "autonomous" agents.

"Autonomous agents" describe apps that behave as Agents from the perspective of their user. An example of an autonomous agent is a virtual secretary: an app that can read through your emails and, for example, pay the bills for you. This is a system that the user sets up with a few credentials and then works autonomously, without the user's supervision.

"Conversational agents" instead describe software that behaves like an Agent from the perspective of their owner only. An example of a conversational agent is a virtual salesman: an app that reads through a list of potential clients and calls them one by one, trying to close a sale. From the perspective of the clients receiving the call the bot is not an agent: it can perform no actions on their behalf, in fact it may not be able to perform actions at all. But from the perspective of the salesman the bots are agents, because they're calling people for them, saving a lot of their time.

## From chatbots to agents

Even with all the distinctions above, telling whether your systems can be called "agentic" or not is not always straightforward. It's best to think about agents and chatbots as a spectrum, where a specific system may be more or less agentic and more or less autonomous without the need to draw hard lines.

![](/posts/2024-05-30-the-agent-spectrum/chatbot-to-agent-spectrum.png)

In order to understand this difference in practice, let's try to place some well known apps and patterns on this scale and analyze them.

## Bare LLMs

At the very left side of the diagram we find bare LLMs and all applications that perform nothing more than direct calls to LLMs, such as ChatGPT's free app and other similarly simple assistants and chatbots. There are no other components than the model itself and their mode of operation is very straightforward:

![](/posts/2024-05-30-the-agent-spectrum/direct-llm-call.png)

This systems rank so low because they're not designed with the intent of accomplishing a goal, and neither can take any actions on the user's behalf. They focus on talking with a user in a reactive way and can do nothing else than talk back. An LLM on its own has no agency at all. 

At this level it also makes very little sense to distinguish between autonomous or conversational agent behavior, because the entire app shows no degrees of autonomy from the perspective of any of the users involved.

## Basic RAG

Together with direct LLM calls and simple chatbots, basic RAG is also an example of an application that does not need any agency or goals to pursue in order to function. Simple RAG apps works in two stages: first the user question is sent to a retriever system, which fetches some additional data relevant to the question. Then, the question and the additional data is sent to the LLM to formulate an answer. 

![](/posts/2024-05-30-the-agent-spectrum/basic-rag.png)

This means that simple RAG is not agentic: the LLM takes no decision and performs no actions on behalf of the user. The LLM has no role in the retrieval step and simply reacts to the RAG prompt. Again, the LLM is given no agency, takes no decisions in order to accomplish its goals, and has no tools it can decide to use, or actions it can decide to take. It's a fully pipelined, reactive system. However, we may rank basic RAG more on the autonomous side because it does not need any user oversight in order to perform retrieval.

## Basic Conversational Agents

Confusingly, you may come across applications that call themselves "conversation agents". The term has been used for lots of different and unrelated use cases, but the idea that it tries to convey is that the app uses LLMs to accomplish a goal through conversation with a user. At every iteration with the user conversational agents will check if their goal was accomplished and, if not, will continue the conversation. As soon as the goal is achieved, they perform a pre-defined action and then close the chat.

![](/posts/2024-05-30-the-agent-spectrum/basic-conversational-agent.png)

For example, a conversational agent could be used to perform a screening interview, where the goal is fundamentally to go through a checklist with the user. Another more interesting use case for conversational agents is sales calls, where the aim of the bot is to get the user agree to a sale. 

Conversational agents are very different from simple chatbots. Chatbots are simply reactive and expect the users to lead the conversation, while conversational agents are highly motivated talkers that will steer the conversation and, if well built, won't let the user go on a tangent.

Conversational agents come in all shapes and forms, but the most basic of them rank quite low in the "agentic" scale because, although they have a clear goal to accomplish, they strongly lack the ability to perform any action on behalf of the users, which is a core of what defines an Agent. They can be seen as Agents only from the perspective of the person controlling them (for example, the salesmen that don't need to call the clients themselves), but not from the perspective of the person interacting with them (the client that receives the call).



.

.

.

.

.



On the contrary, OpenAI's GPT-4 is already an application that can be considered agentic. When prompted correctly, GPT-4 can perform some actions on behalf of the user: for example, users can ask GPT-4 questions that trigger a web search, or ask them to generate an image. These behaviors already raises the app to the status of Agent: the LLM received a question, realized it contains a task to accomplish, decided how to best accomplish such task and performed the necessary actions. This applications normally perform one single action to accomplish the task, and the possible actions they can do are very limited, but they can be seen as very simple AI Agents.

## Are RAG apps AI Agents?

RAG apps can take many shapes and forms, so it's important to understand how RAG is implemented before drawing the line.

Simple RAG apps works in two stages: first the user question is sent to a retriever system, which fetches some additional data relevant to the question. Then, the question and the additional data is sent to the LLM to formulate an answer. This means that simple RAG is not agentic: the LLM takes no decision and performs no actions on behalf of the user. The LLM has no role in the retrieval step and simply reacts to the RAG prompt.

However, RAG can be improved onto different axis, and in some cases introducing some agentic behavior can help noticeably. For example, some RAG systems start not with a retriever, but with an LLM call which task is to decide whether calling the retriever is necessary or not. For example, if the user asks "Where is Sealand located?" the LLM should do a retrieval, to make sure to not generate a hallucinated answer. Instead, if the question is "What is 45+23?", then retrieval is unnecessary and it should be skipped.

While arguable, a system like this can already be considered an AI Agent, because the LLM needs to decide whether or not to use a tool (the retriever) in order to accomplish the task of generating the best answer.

More sophisticated RAG implementations go even further in the direction of AI Agents by implementing "multi-hop" or "chain-of-though" RAG. These systems work as follows:

1. The user asks a rather complex question, such as "When was the eldest sistem of the last King of France born?"
2. The question is given to the LLM, which first of all breaks down the question into subtasks. In this case, the subtasks could be:
    a. Find out who was the last King of France
    b. Find out who was his eldest sister, if any
    c. Find out when she was born
3. These tasks are then addressed one after the other using a RAG pipeline and accumulating the answers at each step.
4. Once the last task has been addressed, the LLM recaps the results of this research and replies to the user.

Such applications are sometimes addressed already as Autonomous Agents, because they plan and perform their own research autonomously. However, many people prefers to identify a system like this as "agentic RAG" to clarify that the core of the system is still a RAG pipeline and that the amount of actions they can take is limited only to the decision of how many time to run their RAG pipeline and with which question.

## Conversational Agents

Another blurry concept is that of "conversational agents". It's important here to distinguish this concept from a simple chatbot or assistant application



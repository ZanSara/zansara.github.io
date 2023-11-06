---
title: "[DRAFT] Unusual Haystack: chatbots with a script"
date: 2023-11-xx
author: "ZanSara"
tags: [Haystack, "Haystack 2.0", "Canals", "Chatbots", "DAG", LLMs]
featuredImage: "/posts/2023-11-xx-haystack-chatbots-with-script/cover.png"
draft: true
---

<small>*Cover image by [DALL-E 3](https://openai.com/dall-e-3)*</small>

When we think about chatbots, we normally imagine them as assistants that react to our requests, like customer support bots or personal assistants. But what if the roles were inverted? Can LLM-based chatbots take an active role in the conversation with a human and drive the discussion like an interviewer would do?

In this post I am going to show you how to use Haystack in a very unconventional way to build very elaborate chatbots that don't simply react to the user's queries, but follow a script to get the answers out of the user in a structured form.

# The Context: Restaurant Booking

Let's imagine we are building a chatbot for a famous restaurant, one that is constantly overbooked. At such places, tables can normally can be reserved online with a simple form, but this one wants to also offer this functionality through a chatbot. 

The bot has to collect some key information from the user: the time and date of the reservation, how many people to book for, and it also has to ask about any sort of food restrictions and potentially reschedule if the menu of the selected day is not suitable for the guests. It must obtain the phone number of the reference person and its name, and make sure all the guests are informed that there is a strict dresscode at the place and that they must respect it to be allowed inside. For the sake of the example, let's imagine the restaurant has two locations, one of which has outdoor seating during the summer as well, while in the other there may be occasional TV crews as the restaurant hosts regular  cooking competitions. And let's not forget that the guests may have special requests that should also be recorded by the bot.

The process is far from straightforward, and for as good as current LLMs are nowadays at handling context, we can't always rely on them ticking all the boxes in a free-form conversation, especially if the chat itself becomes confusing. We need to make sure that the bot is always on top of the conversation.

# A Tree of Questions

One task that Haystack 2.0 really shines with is the building of complex pipelines, and one way to interpret a pipeline's graph in the context of a chatbot application is to see it as a decision tree, where each node is a unit of information that the bot should get from the user before moving on.

For example, we can try to summarize the requirements above in a script that may look like this:

![graph TD;
START --> A
B --> HUMAN
D --> END
A["Identify the restaurant and\nask for reason of the call"] --"something else"-->  B["Route to human assistant"]
A --"make reservation"--> F["Ask for the number of guests"]
F --"number is unknown"--> D["Close the call specifying\nno reservation was made"]
F --"number is given" --> C["List availability and ask for the desired\nlocation, time and date"]
C --"no match"--> D
C --"location B" --> H["Ask whether they are ok\nwith TV crews filming them"]
C --"location A\nin summer" --> G["Ask whether they prefer\nindoor or outdoor seating"]
H --"not ok with filming" --> D
C --"location A\nin winter"--> E["Ask for food restrictions\nrelated to the place/date selected"]
G --"indoor seating" --> E
G --"outdoor seating" --> E
H --"ok with filming" --> E
E --"there are\nproblems"--> C
E --"no problems" -->  I["Ask whether they are ok\nwith the dresscode"]
I --"dresscode not ok" --> D
I --"dresscode ok"--> J["Ask for nameand phone number\nfor the reservation"]
J --"they can't give contact info" --> D
J --"contact info provided" --> K["Summarize reservation details\nand end the chat"]
K --> END](/posts/2023-11-xx-haystack-chatbots-with-script/conversation-tree.png)

Unlike old-shool chatbots, each step of the above tree may not be a single question. The bot may need to iterate with the user a few times in order to get the required information fully. For example, asking the users whether they want to sit indoors or outdoors at location A might go as such:

> Bot: Location A offers indoor and outdoor seating. There's availability for both right now. What would be your preference?
>
> User: We prefer outside if it's not too cold. Is it cold there at that time of the night?
>
> Bot: Average temperatures for 8 PM in mid April range between 18C and 23C, so it's already possible to dine outdoors in good weather.
>
> User: What happens in case of rain?
>
> Bot: If rain is forecast for the evening, a few guests will be moved indoors and the remaining are going to be rescheduled for another date at our best availability.
>
> User: We will stay indoors then.

Worse yet, users may initially give a reply, and then later on in the conversation change their mind:

> Bot: So it's Location A, indoor seating. Do any of you have any food restrictions we should be aware of?
>
> User: No, none has. I'm sorry, can we change the time of the reservation? One of my friends can't make it by 8 PM. If we could move it to 9 PM that would be fantastic.
>
> Bot: I'm sorry, at 9 PM we only have availability at Location B. Is that fine for you?
> 
> User: Is it at Location B where they have the TV crews?
>
> Bot: Yes, at Location B we have a video crew every evening in April.
>
> User: That doesn't work for us. Can we select another day?

And so on. While the script for the bot is straigthforward, the user may jump through the conversation in unexpected ways, and the bot needs to be able to handle all that in a graceful way without forgetting to collect any piece of information.

# Query the user "step-by-step"

One of the most important features of the tree above is that the wider objective of "making a reservation" can be broken down into a tree of subtasks, which we can call "conversation steps". At every step the objective is quite clear: the bot has to extract one specific bit of information from the user and should not consider it done until the user has given such information.

This implies that at each conversation step we have a loop:
- The bot asks for the information.
- The user replies.
- The bot needs to assess whether the user's reply contains the required information.
- If it does, move onto the next step.
- If it does not, check whether the user changed topic of if they asked for clarifications
  - If they asked for clarifications, continue the conversation until they give the answer
  - If they changed topic, jump to the conversation step that handles such topic.

From this breakdown we already realize that there are two main components in this pipeline: one that handles the conversation steps, and one that manages sudden changes of topic. We can call them `ConversationStep` and `TopicIdentifier`.

Let's try to design them!

# Conversation Step




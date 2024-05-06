---
title: "ClozeGPT: Write Anki cloze cards with a custom GPT"
date: 2024-02-28
author: "ZanSara"
tags: [Python, LLM, GPT, Generation, "Language Learning", Anki, Clozes, GPTs, "Prompt Engineering"]
featuredImage: "/posts/2024-02-28-create-anki-cloze-cards-with-custom-gpt/cover.png"
---

As everyone who has been serious about studying with [Anki](https://apps.ankiweb.net/) knows, the first step of the journey is writing your own flashcards. Writing the cards yourself is often cited as the most straigthforward way to make the review process more effective. However, this can become a big chore, and not having enough cards to study is a sure way to not learn anything.

What can we do to make this process less tedious?

# Write simple cards

[A lot](https://www.reddit.com/r/Anki/) has been written about the best way to create Anki cards. However, as a [HackerNews commenter](https://news.ycombinator.com/item?id=39002138) once said:

> One massively overlooked way to improve spaced repetition is to make easier cards.

Cards can hardly be [too simple to be effective](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge). You don't need to write complicated tricky questions to make sure you are making the most of your reviews. On the contrary, even a long sentence where the word you need to study is highlighted is often enough to make the review worthwhile.

In the case of language learning, if you're an advanced learner one of the easiest way to create such cards is to [copy-paste a sentence](https://www.supermemo.com/en/blog/learn-whole-phrases-supertip-4) with your target word into a card and write the translation of that word (or sentence) on the back. But if you're a beginner, even these cards can be complicated both to write and to review. What if the sentence where you found the new word is too complex? You'll need to write a brand new sentence. But what if you write an incorrect sentence? And so on.

# Automating the process

Automated card generation has been often compared to the usage of [pre-made decks](https://www.reddit.com/r/languagelearning/comments/6ysx7g/is_there_value_in_making_your_own_anki_deck_or/), because the students don't see the content of the cards they're adding to their decks before doing so. However, this depends a lot on how much the automation is hiding from the user.

In my family we're currently learning Portuguese, so we end up creating a lot of cards with Portuguese vocabulary. Given that many useful words are hard to make sense of without context, having cards with sample sentences helps me massively to remember them. But our sample sentences often sound unnatural in Portuguese, even when they're correct. It would be great if we could have a "sample sentence generator" that creates such sample sentences for me in more colloquial Portuguese!

This is when we've got the idea of using an LLM to help with the task. GPT models are great sentence generators: can we get them to make some good sample sentence cards?

A [quick experiment](https://chat.openai.com/share/89c821b8-6048-45f3-9fc1-c3875fdbe1c5) proves that there is potential to this concept.

![](/posts/2024-02-28-create-anki-cloze-cards-with-custom-gpt/chatgpt-anki-card-creation.png)

# Custom GPTs

The natural next step is to store that set of instructions into a custom prompt, or as they're called now, a [custom GPT](https://help.openai.com/en/articles/8554407-gpts-faq#h_40756527ce). Making these small wrapper is [really easy](https://help.openai.com/en/articles/8554397-creating-a-gpt): it requires no coding, only a well crafted prompt and a catchy name. So we called our new GPT "ClozeGPT" and started off with a prompt like this:


    Your job is to create Portuguese Anki cloze cards. 
    I might give you a single word or a pair (word + translation). 

    Front cards:
    - Use Anki's `{{c1::...}}` feature to template in cards. 
    - You can create cards with multiple clozes.
    - Keep the verb focused, and don't rely too much on auxiliary verbs like 
      "precisar", "gostar", etc...
    - Use the English translation as a cloze hint.

    Back cards:
    - The back card should contain the Portuguese word.
    - If the word could be mistaken (e.g. "levantar" vs. "acordar"), 
      write a hint that can help me remember the difference. 
    - The hint should be used sparingly.

    Examples:

    ---------

    Input: cozinhar

    # FRONT
    ```
    Eu {{c1::cozinho::cook}} todos os dias para minha família.
    ```

    # BACK
    ```
    cozinhar - to cook
    ```
    ---------

    Input: levantar

    # FRONT
    ```
    Eu preciso {{c1::levantar::get up}} cedo amanhã para ir ao trabalho.
    ```

    # BACK
    ```
    levantar - to get up, to raise (don't mistake this with "acordar", which is to wake up from sleep)
    ```

This simple prompt already gives very nice results!

![](/posts/2024-02-28-create-anki-cloze-cards-with-custom-gpt/beber-flashcard.png)

# Bells and whistles

Naturally, once a tool works well it's hard to resist the urge to add some new features to it. So for our ClozeGPT we added a few more abilities:

    # Commands

    ## `+<<word>>`
    Expands the back card with an extra word present in the sentence.
    Include all the previous words, plus the one given.
    In this case, only the back card needs to be printed; don't show the front card again.

    ## `R[: <<optional hint>>]`
    Regenerates the response based on the hint given.
    If the hint is absent, regenerate the sentence with a different context.
    Do not change the target words, the hint most often a different context I would like to have a sentence for.

    ## `Q: <<question>>`
    This is an escape to a normal chat about a related question.
    Answer the question as usual, you don't need to generate anything.

The `+` command is useful when the generated sentence contains some other interesting word you can take the occasion to learn as well:

![](/posts/2024-02-28-create-anki-cloze-cards-with-custom-gpt/maca-flashcard.png)

The `R` command can be used to direct the card generation a bit better than with a simple press on the "Regenerate" icon:

![](/posts/2024-02-28-create-anki-cloze-cards-with-custom-gpt/morango-flashcard.png)

And finally `Q` is a convenient escape hatch to make this GPT revert back to its usual helpful self, where it can engage in conversation.

![](/posts/2024-02-28-create-anki-cloze-cards-with-custom-gpt/esquecer-flashcard.png)

# Have fun

Our small [ClozeGPT](https://chat.openai.com/g/g-wmHCaGcCZ-clozegpt) works only for Portuguese now, but feel free to play with it if you find it useful. And, of course, always keep in mind that LLMs are only [pretending to be humans](https://chat.openai.com/share/07295647-9f43-4346-97a5-b35f62251d55).

![](/posts/2024-02-28-create-anki-cloze-cards-with-custom-gpt/laranja-flashcard.png)

_Front: I like orange juice in my morning coffee._


<p class="fleuron"><a href="https://www.zansara.dev/posts/2024-05-06-teranoptia/">SDE</a></p>
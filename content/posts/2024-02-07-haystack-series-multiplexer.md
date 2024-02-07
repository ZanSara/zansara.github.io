---
title: "Build Haystack pipelines with Multiplexer"
date: 2024-02-07
author: "ZanSara"
tags: ["Haystack 2.0", Haystack, Python, LLM, GPT, Pipeline, RAG, "Hybrid Retrieval", "Self-correction loop"]
series: ["Haystack 2.0 Series"]
featuredImage: "/posts/2024-02-07-haystack-series-multiplexer/cover.jpeg"
draft: true
---

Building Pipelines is not always easy and fun. When Pipelines start including several components, branches, loops and so on, connecting everything together if often a complex task. Sometimes it even looks impossible without writing your own components!

Haystack provides a component that makes complex pipelines easier to build and reduces the amount of custom components you need: it's called [`Multiplexer`](https://docs.haystack.deepset.ai/v2.0/docs/multiplexer), and we're going to see how to use it to cover two common usecases:

1. Inputs proliferation
2. Loops

# Inputs proliferation

If you've ever build a Haystack pipeline with more than 3-4 components, you probably came across this problem. New components take some of their input from the other components of a pipeline, but many of them also require additional input from the user. As a result, the dictionary input of `pipeline.run()` grows and grows until it becomes very repetitive.

One common example is **hybrid search pipelines**, like this one:

```python
from haystack import Pipeline
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever, InMemoryEmbeddingRetriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders import OpenAITextEmbedder
from haystack.components.rankers import TransformersSimilarityRanker
from haystack.components.joiners import DocumentJoiner

prompt_template = """
Given these documents, answer the question.\nDocuments:
{% for doc in documents %}
    {{ doc.content }}
{% endfor %}
\nQuestion: {{question}}
\nAnswer:
"""
pipe = Pipeline()

pipe.add_component(instance=OpenAITextEmbedder(), name="query_embedder")
pipe.add_component(instance=InMemoryEmbeddingRetriever(document_store=document_store), name="embedding_retriever")
pipe.add_component(instance=InMemoryBM25Retriever(document_store=document_store), name="bm25_retriever")
pipe.add_component(instance=DocumentJoiner(sort_by_score=False), name="doc_joiner")
pipe.add_component(instance=TransformersSimilarityRanker(model="intfloat/simlm-msmarco-reranker", top_k=10), name="ranker")
pipe.add_component(instance=PromptBuilder(template=prompt_template), name="prompt_builder")
pipe.add_component(instance=OpenAIGenerator(), name="llm")
pipe.add_component(instance=AnswerBuilder(), name="answer_builder")

pipe.connect("query_embedder", "embedding_retriever.query_embedding")
pipe.connect("embedding_retriever", "doc_joiner.documents")
pipe.connect("bm25_retriever", "doc_joiner.documents")
pipe.connect("doc_joiner", "ranker.documents")
pipe.connect("ranker", "prompt_builder.documents")
pipe.connect("prompt_builder", "llm")
pipe.connect("llm.replies", "answer_builder.replies")
pipe.connect("llm.meta", "answer_builder.meta")
pipe.connect("doc_joiner", "answer_builder.documents")
```

<< IMMAGINE >>

In this pipeline, there are several component that need the value of `query` to operate. They are:

- the Query Embeddder
- the BM25 Retriever
- the Ranker
- the Prompt Builder
- the Answer Builder

Five components that need the same identical input, directly from the user! This means that the pipeline.run() call is going to be huge and extremely repetitive.

```python
question = "Where does Mark live?"

result = pipe.run(
    {
        "query_embedder": {"text": question},
        "bm25_retriever": {"query": question},
        "ranker": {"query": question},
        "prompt_builder": {"question": question},
        "answer_builder": {"query": question},
    }
)

print(result["answer_builder"]["answers"][0].data)
```

This approach clearly doesn't scale!

You can solve this problem by putting a Multiplexer at the top of the pipeline, and connect all the components that need `query` to it.

```python
from haystack.components.others import Multiplexer

pipe = Pipeline()

# Add a Multiplexer to the pipeline
pipe.add_component(instance=Multiplexer(str), name="multiplexer")

pipe.add_component(instance=OpenAITextEmbedder(), name="query_embedder")
pipe.add_component(instance=InMemoryEmbeddingRetriever(document_store=document_store), name="embedding_retriever")
pipe.add_component(instance=InMemoryBM25Retriever(document_store=document_store), name="bm25_retriever")
pipe.add_component(instance=DocumentJoiner(sort_by_score=False), name="doc_joiner")
pipe.add_component(instance=TransformersSimilarityRanker(model="intfloat/simlm-msmarco-reranker", top_k=10), name="ranker")
pipe.add_component(instance=PromptBuilder(template=prompt_template), name="prompt_builder")
pipe.add_component(instance=OpenAIGenerator(), name="llm")
pipe.add_component(instance=AnswerBuilder(), name="answer_builder")

# Connect the Multiplexer to all the components that need the query
pipe.connect("multiplexer.value", "query_embedder.text")
pipe.connect("multiplexer.value", "bm25_retriever.query")
pipe.connect("multiplexer.value", "ranker.query")
pipe.connect("multiplexer.value", "prompt_builder.question")
pipe.connect("multiplexer.value", "answer_builder.query")

pipe.connect("query_embedder", "embedding_retriever.query_embedding")
pipe.connect("embedding_retriever", "doc_joiner.documents")
pipe.connect("bm25_retriever", "doc_joiner.documents")
pipe.connect("doc_joiner", "ranker.documents")
pipe.connect("ranker", "prompt_builder.documents")
pipe.connect("prompt_builder", "llm")
pipe.connect("llm.replies", "answer_builder.replies")
pipe.connect("llm.meta", "answer_builder.meta")
pipe.connect("doc_joiner", "answer_builder.documents")
```

<< IMMAGINE >>

With this setup, only Multiplexer expects any input from the user. This makes the `run()` statement very straightforward once again."""

```python
result = pipe.run({"multiplexer": {"value": "Where does Mark live?"}})

print(result["answer_builder"]["answers"][0].data)
```

# Loops

When your pipeline loops, there is often one component that needs to receive input from several sources: at first by the user, that sets off the loop, and subsequently from other components, when the loop comes around and needs to start again.

An example of a this use case is a **self-correcting generative pipeline**. Such pipeline takes unstructured text as input, and uses the information contained in the text to extract structured data in JSON format.

While LLMs can address this task on their own most of the time, they don't always output valid JSON, or the JSON they produce doesn't always respect the schema we expect. So we can add a validation component after the generator that checks that the output respects our constraints. If the output is invalid, it creates a new prompt with the wrong JSON, the error message, and asks the LLM to fix its mistakes.

Let's see how such a pipeline might look like.

*Note: this example is a modified version of Tutorial 28, which you can find [here](https://colab.research.google.com/github/deepset-ai/haystack-tutorials/blob/main/tutorials/28_Structured_Output_With_Loop.ipynb#scrollTo=RZJg6YHId300).*

## Define the JSON schema with Pydantic

Let's assume we're extracting basic facts about world cities. Pydantic is a great choice to define JSON schemas, as it provides all the tools to define and handle such structures in a Pythonic way.

```python
import pydantic
from typing import List


class City(pydantic.BaseModel):
    name: str
    country: str
    population: int


class CitiesData(pydantic.BaseModel):
    cities: List[City]
```

## Define the validation component

Haystack doesnt have a JSON validation component yet, so let's build one from scratch. If you want to learn more about how to build custom components with Haystack 2.0, check out [this guide](https://docs.haystack.deepset.ai/v2.0/docs/custom-components).

```python
import json
from typing import Optional
from haystack import component


@component
class OutputValidator:
    def __init__(self, pydantic_model: pydantic.BaseModel):
        self.pydantic_model = pydantic_model  # The model to check out JSON agains

    @component.output_types(valid_replies=List[str], invalid_replies=Optional[List[str]], error_message=Optional[str])
    def run(self, replies: List[str]):
        # Try to parse the LLM's reply
        # If the LLM's reply is a valid JSON that respects the schema, return `"valid_replies"`
        try:
            output_dict = json.loads(replies[0])
            self.pydantic_model.parse_obj(output_dict)
            return {"valid_replies": replies}

        # If the LLM's reply is corrupted or not valid, return "invalid_replies" and the "error_message" for LLM to try again
        except (ValueError, pydantic.ValidationError) as e:
            return {"invalid_replies": replies, "error_message": str(e)}
```

Now let's build the pipeline. Keep in mind that we will need two PromptBuilders:
- one that takes the user's text and the JSON schema and makes the LLM try from scratch
- another one that takes the text, the schema, the wrong output and the error message and asks the LLM to retry.

So we should end up with a pipeline that should look like this:

<< IMAGE >>

Let's write it in code:

```python
from haystack import Pipeline
from haystack.components.builders import PromptBuilder

initial_prompt_template = """
Create a JSON object from the information present in this passage: {{passage}}.
Only use information that is present in the passage. Follow this JSON schema,
but only return the actual instances without any additional schema definition:
{{schema}}
Make sure your response is a dict and not a list.
"""

error_correction_prompt_template = """
Fix the following JSON file to respect the given schema, making sure that the
content of the JSON reflects the reference text's content.
The JSON is invalid or incorrect: use the error message to help yourself.

Invalid JSON:
{{ invalid_replies }}

Error message:
{{ error_message }}

Reference text:
{{ passage }}

JSON Schema:
{{ schema }}

Make sure your response is a dict and not a list.
"""

pipeline = Pipeline(max_loops_allowed=5)

# Add components to your pipeline
pipeline.add_component(instance=PromptBuilder(template=initial_prompt_template), name="initial_prompt_builder")
pipeline.add_component(instance=PromptBuilder(template=error_correction_prompt_template), name="error_correction_prompt_builder")
pipeline.add_component(instance=OpenAIGenerator(), name="llm")
pipeline.add_component(instance=OutputValidator(pydantic_model=CitiesData), name="output_validator")

# Now, connect the components to each other
pipeline.connect("initial_prompt_builder", "llm")
pipeline.connect("llm", "output_validator")
pipeline.connect("output_validator.invalid_replies", "error_correction_prompt_builder.invalid_replies")
pipeline.connect("output_validator.error_message", "error_correction_prompt_builder.error_message")
#pipeline.connect("error_correction_prompt_builder", "llm")  # This connection will fail!

# >> PipelineConnectError: Cannot connect 'error_correction_prompt_builder.prompt' with 'llm.prompt': llm.prompt is already connected to ['initial_prompt_builder'].
```

## Introduce Multiplexer

The error message is reasonable: the LLM is already receiving a query, and it does not expect more than one. How can we close this loop?

In these cases, a Multiplexer needs to be placed in front of the `prompt` input of the Generator. Multiplexer has a Variadic input, which means that you can connect any number of components to it as long as the type is correct. Multiplexer will make sure that the Generator always receives only one prompt at a time, so it can run effectively.

```python
pipeline = Pipeline(max_loops_allowed=5)

# Add components to your pipeline
pipeline.add_component(instance=PromptBuilder(template=initial_prompt_template), name="initial_prompt_builder")
pipeline.add_component(instance=PromptBuilder(template=error_correction_prompt_template), name="error_correction_prompt_builder")
pipeline.add_component(instance=OpenAIGenerator(), name="llm")
pipeline.add_component(instance=OutputValidator(pydantic_model=CitiesData), name="output_validator")
pipeline.add_component(instance=Multiplexer(str), name="multiplexer")

# Now, connect the components to each other
pipeline.connect("initial_prompt_builder", "multiplexer")
pipeline.connect("multiplexer", "llm")
pipeline.connect("llm", "output_validator")
pipeline.connect("output_validator.invalid_replies", "error_correction_prompt_builder.invalid_replies")
pipeline.connect("output_validator.error_message", "error_correction_prompt_builder.error_message")
pipeline.connect("error_correction_prompt_builder", "multiplexer")

passage = """
Berlin is the capital of Germany. It has a population of 3,850,809.
Paris, France's capital, has 2.161 million residents.
Lisbon is the capital and the largest city of Portugal with the population of 504,718.
"""
result = pipeline.run({
    "initial_prompt_builder": {"passage": passage, "schema": CitiesData.schema_json(indent=2)},
    "error_correction_prompt_builder": {"passage": passage, "schema": CitiesData.schema_json(indent=2)}
})

print(result["output_validator"]["valid_replies"][0])
```

## Watch out!

In this pipeline is impossible for Multiplexer to ever receive more than one value at a time. However, if your pipeline gets more complex, you have to make sure this assumption is correct, because Multiplexer will throw an exception if it receives multiple values at the same time.

For example, this (meaningless) pipeline accepts all the connections, but will fail at runtime:

```python
pipeline = Pipeline()

pipeline.add_component("prompt_builder_a", PromptBuilder("Question A: {{ question }}"))
pipeline.add_component("prompt_builder_b", PromptBuilder("Question B: {{ question }}"))
pipeline.add_component("multiplexer", Multiplexer(str))

pipeline.connect("prompt_builder_a", "multiplexer")
pipeline.connect("prompt_builder_b", "multiplexer")

pipeline.draw("warning-pipeline.png")
Image('warning-pipeline.png')

results = pipeline.run({
    "prompt_builder_a": {"question": "a?"},
    "prompt_builder_b": {"question": "b?"},
})

# >> ValueError: Multiplexer expects only one input, but 2 were received.
```

# Conclusions

`Multiplexer` is a very versatile component that enhances the capabilities of Pipeline in different ways, and helps you connecting components into non-trivial ways.

To learn more about it, check its official documentation as well: [Multiplexer](https://docs.haystack.deepset.ai/v2.0/docs/multiplexer).

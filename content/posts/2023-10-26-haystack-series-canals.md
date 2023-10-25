---
title: "Canals: a new concept of Pipeline"
date: 2023-10-26
author: "ZanSara"
tags: ["Haystack 2.0", Haystack, Python, Canals, Pipeline, DAG, graph, "API Design"]
series: ["Haystack 2.0 Series"]
featuredImage: "/posts/2023-10-26-haystack-series-canals/cover.png"
draft: true
# canonicalUrl: https://haystack.deepset.ai/blog/canals-a-new-concept-of-pipeline
---

As we have seen in [the previous episode of this series](/posts/2023-10-15-haystack-series-pipeline), Haystack's Pipelines are a very powerful concept that comes with its set of benefits and shortcomings. In Haystack 2.0, Pipeline was one of the first items that we focused our attention on, and it was the starting point of the entire rewrite.

What does this mean, in practice? Let's have a look at what Haystack Pipelines in 2.0 are going to be like, how they differ from their 1.x counterparts, and what are the pros and cons of this new paradigm.

## New Use Cases

I've already written [at length](/posts/2023-10-15-haystack-series-pipeline) about what made the original Pipeline concept so powerful to begin with, and what its weaknesses are. Pipelines were overly effective for the use cases that we could conceive while developing them, but they didn't generalize as well as they should for unforeseen situations.

For a long time Haystack could afford not to focus on use cases that didn't fit its architecture, as I have mentioned in my [previous post](/posts/2023-10-11-haystack-series-why) about the reasons for the rewrite. Pipeline was then more than sufficient for its purposes.

However, as LLMs and Generative AI entered the scene abruptly at the end of 2022, the situation flipped. Pipeline seemingly overfit its existing usecases, fossilized on them, and could not cope with the requirements set by the new landscape of the field.

Let's take one of these usecases and see where it leads us.

## RAG Pipelines

Let's take one simple example: [retrieval augmentated generation](https://www.deepset.ai/blog/llms-retrieval-augmentation), or RAG for short. This technique has been used since the very early days of the Generative AI boom as an easy way to strongly [reduce hallucinations](https://haystack.deepset.ai/blog/generative-vs-extractive-models) and improve alignment of LLMs. The basic idea is very simple: instead of asking the LLM a simple question, such as `"What's the capital of France?"`, we send to the model a more complex prompt, that includes both the question and the answer. Such a prompt might be:

```text
Given the following paragraph, answer the question.

Paragraph: France is a unitary semi-presidential republic with its capital in Paris, 
the country's largest city and main cultural and commercial centre; other major urban 
areas include Marseille, Lyon, Toulouse, Lille, Bordeaux, Strasbourg and Nice.

Question: What's the capital of France?

Answer:
```

In this situation, the task of the LLM becomes far easier: instead of drawing facts from its internal knowledge, which might be lacking, inaccurate or out-of-date, the model only needs to rephrase the content of the paragraph in order to answer the question.

However, it seems like we've only moved the problem instead of solving it. How can we provide the correct snippets of text to the LLM? This is where the "retrieval" keyword comes up.

One of Haystack's primary use cases have been [Extractive Question Answering](https://huggingface.co/tasks/question-answering): a system where a Retriever component searches into a Document Store (such as a vector or SQL database) for snippets of text that are the most relevant to a given question. It then sends such snippets to a Reader, which highlights the keywords that answer the original question.

By replacing a Reader model with an LLM, we get a Retrieval Augmented Generation Pipeline. Easy!

![Generative vs Extractive QA Pipeline Graph](/posts/2023-10-26-haystack-series-canals/gen-vs-ext-qa-pipeline.png)

So far, all checks out. Supporting RAG with Haystack feels not only possible, but natural. So let's take this simple example one step forward: what if, instead of getting the data from a document store, I want to retrieve data from the Internet?

## Web RAG

At first impact the task may not seem daunting. We surely need a special Retriever, that instead of searching through a DB searches through the Internet using a search engine. But the core concepts stays the same, and so, we assume, should the Pipeline's graph. The end result should be something like this:

![Initial Web RAG Pipeline Graph](/posts/2023-10-26-haystack-series-canals/initial-web-rag-pipeline.png)

However, the problem doesn't end there. Search engines return links, which need to be accessed, and the content of the webpage downloaded. Such pages may be really long and noisy, so the resulting text needs to be cleaned, reduced into paragraphs, embedded by a retrieval model, ranked against the original query, and only the top few resulting pieces of text need to be passed over to the LLM. Just by including this minimal requirements, our pipeline already looks like this:

![Linear Web RAG Pipeline Graph](/posts/2023-10-26-haystack-series-canals/linear-web-rag-pipeline.png)

And we haven't yet considered that URLs may reference not HTML pages, but PDFs, videos, zip files, and so on. We are going to need file converters, zip extractors, audio transcribers...

![Multiple File Type Web RAG Pipeline Graph](/posts/2023-10-26-haystack-series-canals/multifile-web-rag-pipeline.png)

If you remember the previous post on Pipeline, you'll notice how this usecase moved very quickly from looking like a simple query pipeline into a strange overlap of a query and an indexing pipeline. However, as we've learned from the previous post, indexing pipelines have their own set of idiosyncrasies, one of which is that they can't process files of different types simultaneously. On the other hand, we can't expect the Search Engine to limit itself to only HTML files, or only PDFs, unless we filter them out on purpose, which makes the pipeline less powerful. In fact, the pipeline above can't really be made to work reliably.

And what if, on top of this, we want to cache the resulting documents to reduce latency? What if I want to get the results from Google's page 2, but only if the content of page 1 was not enough? At this point the pipeline is even hard to draw.

Although Web RAG is possible to some degree in Haystack, it stretches very far what Pipeline was designed to handle. Can we do better?

## Distilling the issue

When we went back to the drawing board to address these concerns, one of the main hurdles was pinpointing the issue. The Pipeline abstraction seems to go from "very ergonomic" to "impossible to deal with" very rapidly, and it's not always clear at which point the transition occurs.

The problem, as it turned out, is that Haystack Pipelines treats each component as a locomotive treats its wagons. They all look the same from the Pipeline's perspective, they can all be connected in any order, and they all go from A to B rolling over the same pair of rails, passing all through the same stations.

![Cargo Train](/posts/2023-10-26-haystack-series-canals/train.png)

In Haystack 1.x, components are designed to serve the Pipeline's needs. A good Component, in this case, is a Component that does not stand out in any way from the others, provides the exact interface Pipeline expects from all of them, and can be connected to any other, in any order. On their own, the components are awkward to use due to the same `run()` method that makes Pipeline so ergonomic. Why a Ranker, that clearly needs only a query and a list of Documents, should also accepts `file_paths` and `meta` in its `run()` method? It does so uniquely to satisfy the Pipeline's requirements, which in turn exist only to make all components forcefully compatible with each other.

Just as a locomotive, Pipeline pushes the Components over the input data one by one. When seen in this light, it's painfully obvious why the indexing pipeline we've seen earlier can't work: the "pipeline train" can only go on one branch at a time. Component trains can't split mid-execution. They are designed to all see the same data all the times. Even when branching happens, all branches always see all the same data. Sending different components onto different rails is not possible by design.

## Breaking it down

When seen in this light, the core of the issue is easier to spot: Pipeline is the only object that drives the execution, while Components tend to be as passive as possible. This approach doesn't scale: as the number of Components to handle grows, and as their variety rises, Pipeline needs to always be aware of all the combinations in order to handle them properly.

Therefore, the rewrite of Pipeline focused on one core principle: in Haystack 2.0, the Components define and drive the execution process. There is no locomotive anymore: Component will need to find their way, such as grabbing the data they need from the producers and send their results to whoever needs them by declaring the proper connections. In the railway methaphor it's like putting wheels under each container: what we get is a truck, and the resulting system looks very much like a highway.

![Highway](/posts/2023-10-26-haystack-series-canals/highway.png)

Just as railways are excellent at going from A to B when you only need to take that single route and never another, highways requires every car to have a driver, but are unbeatable at reaching every possible destination with the same effort. A "highway" Pipeline requires more work from the Components' side, but it frees them to go wherever they need to with a precision that a "railway" Pipeline just cannot accomplish.

## Canals

The implementation of this new, more powerful Pipeline object found its way into its dedicated library, [Canals](https://github.com/deepset-ai/canals). By design, Canals is not geared toward specific NLP usecases, but it's a minimal, generic [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load)-like Pipeline library written purely in Python.

Canals brings two core elements to the table:

- The `Component` protocol, a well-defined API that Python classes need to respect to be understood by the Pipeline.

- The `Pipeline` object, that performs validation, resolves the execution graph and provides a few utilities on top.


## The Pipeline object

The `Pipeline` object may remind vaguely of Haystack's original Pipeline, and using one should feel familiar. For example, this is how you assemble a simple Canals Pipeline that performs a few additions.

```python
!pip install canals==0.9.0

from canals import Pipeline
from sample_components import AddFixedValue

# Create the Pipeline object
pipeline = Pipeline()

# Add the components - same syntax, except for the `inputs` parameter
pipeline.add_component("add_one", AddFixedValue(add=1))
pipeline.add_component("add_two", AddFixedValue(add=2))

# Connect them together
pipeline.connect("add_one.result", "add_two.value")

# Draw the pipeline
pipeline.draw("two_additions_pipeline.png")

# Run the pipeline
results = pipeline.run({"add_one": {"value": 1}})

print(results)
# prints '{"add_two": {"result": 4}}'
```

Creating the Pipeline requires no special attention: however, you can now pass a `max_loops_allowed` parameter, to limit looping when it's a risk. On the contrary, old Haystack Pipelines did not support loops at all.

Next, components are added by calling the `Pipeline.add_component(name, component)` method. This is also subject to very similar limitations than previous `Pipeline.add_node` had: you need unique names, some are reserved (for now, only `_debug`), instances are not reusable, the object needs to be a Component. However, we do not connect the component to each other using this function anymore: this is due to the fact that, in case of loops, validating the connection feels more awkward.

As a consequence, we introduced a new method, `Pipeline.connect()`. This method follows the syntax `("producer_component.output_name_", "consumer_component.input_name")`: so we don't simply connect two components together, but we connect one of their outputs to one of their inputs.

This allows Canals to perform a much more careful validation of such connections. As we will discover soon, Component can declare the type of all their inputs and all their outputs. In this way, Canals not only can make sure that the inputs and outputs exist for the given component, but it can also check whether their types match.

In turn, this feature allows Canals to explain connection failures in great details. For example, if there were a type mismatch between inputs and outputs, `Pipeline.connect()` will return an error such as:

```markdown
Cannot connect 'greeter.greeting' with 'add_two.value': their declared input and output 
types do not match.

greeter:
- greeting: str
add_two:
- value: int (available)
- add: Optional[int] (available)
```

Next, after components are connected together, the resulting Pipeline can be drawn. Also in this case, Pipeline drawings show far more details than their predecessors, due to the fact that the Components are forced to share many more information about what they need to run, the types of these variables, and so on.

The Pipeline above draws the following image:

![A Pipeline making two additions](/posts/2023-10-26-haystack-series-canals/two_additions_pipeline.png)

You can see how now the component class, their inputs from the pipeline and from other components are both named and typed, and how they both seem to have some Optional inputs as well!

So, how do you run such pipeline? By just providing a dictionary of input values. Each component can have its own small dictionary with all the inputs he may take. In the example above, we simply pass `1` to the `value` input of `add_one`. The results mirror the input's structure: `add_two` is at the end of the pipeline, so Pipeline will return a dictionary where under the `add_two` key there is a dictionary: `{"result": 4}`.

However, we've just noticed that these two components seem to have optional inputs too. Tehy're evidently not necessary for the pipeline to run, but they can be used to control the behavior of these components dynamically. For example:

```python
pipeline.run({"add_one": {"value": 1, "add": 2}})
# returns '{"add_two": {"result": 5}}'
```

```python
pipeline.run({"add_one": {"value": 1}, "add_two": {"add": 10}})
# returns '{"add_two": {"result": 12}}'
```

and so on.

Until the pipeline is drawn, however, it might be not entirely obvious what to provide to the run method for it to work. To help, Pipeline also offers a `Pipeline.inputs()` method that returns a structured representation of the expected input. For our pipeline it looks like:

```python
{
    "add_one": {
        "value": {
            "type": int, 
            "is_optional": False
        }, 
        "add": {
            "type": typing.Optional[int], 
            "is_optional": True
        }
    }, 
    "add_two": {
        "add": {
            "type": typing.Optional[int], 
            "is_optional": True
        }
    }
}
```


## The Component API

Now that we covered the Pipeline's API, let's have a look at what it takes for a Python class to be treated as a Canals' Component. The Component API, in fact, is quite straigthforward.

You are going to need:

- **A `@component` decorator**. All component classes must be decorated with the `@component` decorator. This allows Canals to discover and validate them.

- **A `run()` method**. This is the method where the main functionality of the component should be carried out. It's called by `Pipeline.run()`, and therefore has a few constraints, which we will describe later.

- Optionally, **a `warm_up()` method**. It can be used to defer the loading of a heavy resource (think a local LLM, or an embedding model) to the warm-up stage that occurrs right before the first execution of the Pipeline. Components that use `warm_up()` can be added to a Pipeline and connected before the heavy operations are carried out, so that the validation that Canals performs at that stage can happen before resources are wasted.

To summarize, a minimal Canals component can look like this:

```python
from canals import component

@component
class Double:

    @component.output_types(result=int)
    def run(self, value: int):
        return {"result": value * 2}
```

Note how the `run()` method has a few peculiar features. A simple trait is that all the method parameters need to be typed: if `value` was not declared as `value: int`, Canals would raise an exception demanding for typing.

This is the way Components declare to the Pipeline which inputs they expect and of which type: this is the first half of the information needed to perform the validation that `Pipeline.connect()` carries out.

The other half of the information comes from the `@component.output_types` decorator. Unsurprisingly, it's needed to declare how many outputs the component will produce, and of which type. One may ask why not rely on typing for the outputs, just as we've done for the inputs: so why not simply say:


```python
@component
class Double:

    def run(self, value: int) -> int:
        return value * 2
```

For `Double`, this is a legitimate doubt. However, let's make an example with a simple component called `CheckParity`: if a component's input value is even it sends it over the `even` output, while if it's odd, it will send it over the `odd` output. The following clearly doesn't work: there's no place where to specify when the returned value is even or odd.

```python
@component
class CheckParity:

    def run(self, value: int) -> int:
        if value % 2 == 0:
            return value
        return value
```

How about this instead?

```python
@component
class CheckParity:

    def run(self, value: int) -> Dict[str, int]:
        if value % 2 == 0:
            return {"even": value}
        return {"odd": value}
```

This approach seems to carry all the information required: but note how such information is only available at runtime. Unless we parse the method to discover all return statements and their keys (which is not always possible), Pipeline cannot know all the possible keys that the return dictionary may have, and so it can't validate that the connections when `Pipeline.connect()` is called.

The decorator bridges the gap by allowing the class to declare in advance what outputs it will produce and of which type. Pipeline trusts this information to be correct and validates the connections accordingly.

Ok, but what if the component is very dynamic? Maybe the output type depends on the input type. Maybe the number of inputs depend on some initialization parameter. In these cases, Canals also allows components to declare the inputs and output types in their init method as such:

```python
@component
class HighlyDynamicComponent:

    def __init__(self, ...):
        component.set_input_types(self, input_name=input_type, ...)
        component.set_output_types(self, output_name=output_type, ...)

    def run(self, **kwargs):
        ...
```

As you can see, no more typing is needed on `run()`, and the decorator is gone. As long as the component declares its inputs and outputs in a way that Pipeline can understand, the validation can occur.

One more interesting feature of the inputs and output declarations relates to optional and variadic values. Canals supports both, through a mix of type checking and signature inspection. For example, let's have a look at how the `AddFixedValue` we've seen earlier looks like:

```python
from typing import Optional
from canals import component


@component
class AddFixedValue:
    """
    Adds two values together.
    """

    def __init__(self, add: int = 1):
        self.add = add

    @component.output_types(result=int)
    def run(self, value: int, add: Optional[int] = None):
        """
        Adds two values together.
        """
        if add is None:
            add = self.add
        return {"result": value + add}
```

You can see that `add`, the optional parameter we met before, has a default value. Adding a default value to a parameter in the `run()` signature tells Canals that the parameter itself is optional, so that the component can run even if it's not connected to any other component.

Another component that generalizes the sum operation is `Sum`, which instead looks like this:

```python
from canals import component
from canals.component.types import Variadic

@component
class Sum:
    """
    Adds all its inputs together.
    """

    @component.output_types(total=int)
    def run(self, values: Variadic[int]):
        """
        :param values: the values to sum
        """
        return {"total": sum(v for v in values if v is not None)}
```

In this case, we used the special Canals type `Variadic` to tell Canals that the `values` input can receive from multiple producers, instead of just one. Therefore, `values` is going to be a list type, but it can be connected to single `int` outputs, making it a valuable aggregator.

## Serialization

Just as old Haystack Pipelines, also Canals Pipelines can be serialized. However, in this process as well there is a fundamental shift about who is in charge of serializing what.

The original Pipeline used to gather intrusive information about all its Components in the moment when they were initialized, leveraging the shared `BaseComponent` class. On the opposite, Canal's Pipelines delegate the serialization process entirely to its own components.

In Canals, if a component wishes to be serializable it needs to provide two additional methods, `to_dict` and `from_dict`, which performs serialization and deserialization to a dictionary. Pipeline will limit itself to calling each of its component's methods, collect their output, group them together with some limited extra information (such as the connections between them) and return.

For example, if `AddFixedValue` were serializable, its serialized version should look like this:

```python
{
    "type": "AddFixedValue",
    "init_parameters": {
        "add": 1
    }
}
```

and the entire Pipeline we used above would end up as:

```python
{
    "max_loops_allowed": 100,
    "components": {
        "add_one": {
            "type": "AddFixedValue",
            "init_parameters": {
                "add": 1
            }
        },
        "add_two": {
            "type": "AddFixedValue",
            "init_parameters": {
                "add": 2
            }
        }
    },
    "connections": [
        {
            "sender": "add_one.result", 
            "receiver": "add_two.value",
        }
    ]
}
```

Notice how Components are free to perform serialization in the way they see fit. This comes useful especially if the component's state include some non-trivial values, such as objects, API keys, and so on. Pipeline doesn't need anymore to know how to serialize everything the Components may contain: the task is fully delegated to them, which in all cases knows best what needs to be done.

## But... do we need any of this?

Having done a tour of Canals features, one might have noticed one detail. Pipelines now are a bit harder to use than before: you can't just chain every component after every other. There are connections to be made, validation to perform, graphs to assemble.

In exchange, now Pipeline is more powerful than before. Sure: but so is a plain Python script. What do we *really* need the Pipeline object for, then?

ETL frameworks often include an abstraction over the execution flow to be able to make the same high-level system execute over different infrastructures, mostly for scalability and speed. For example they may leverage the abstraction to transparenty distribute nodes on different machines, or run them in parallel, increase throughput by adding replicas, and other such features.

For now, Canals doesn't provide anything of this kind. While we don't exclude that in the future this abstraction may serve this purpose, there are a few other benefits that the Pipeline is providing us right now:

- **Validation**. While components would normally validate their inputs and outputs themselves, Pipeline does all the validation way before any of the components has run, even before the components load any heavy resource. This makes the whole system far less likely to fail at runtime for a simple input/output mismatch, which can be priceless for complex applications.

- **Serialization**. Redistributing code is always tricky: reditributing a JSON file is much more safe. Pipelines make possible to represent complex systems in a radable JSON file that can be edited, shared, stored, deployed and re-deployed on different backends at need. 

- **Drawing**: Canals offers you a way to see your system clearly and automatically, which is often very handy for debugging, inspection of the system, and to collaborate on the pipeline's design.

- On top of this, Pipeline abstractions tend to promote flatter API surfaces by discouraging component's nesting one within the other, and provides easy to use, single-responsibility components that are easy to reason about.

Having said all of this, however, we don't believe that Pipelines are what makes Haystack win or lose. Pipelines are just a bonus on top of what provides the real value: simple, easy to use Components that perform clear tasks in a reliable way. That's why the Component API does not make the `run()` method awkward to use outside of a Pipeline: `Sum.run(values=[1, 2, 3])` still feels Pythonic and always will. So if Pipeline ever becomes a hindrance, the Component won't suffer the loss.

In the next posts I'm going to explore more the world of Haystack components, starting from our now familiar use cases: RAG Pipelines.

---

*Next: Soon!*

*Previous: [Haystack's Pipeline](/posts/2023-10-13-haystack-series-pipeline)*

*See the entire series here: [Haystack 2.0 series](/series/haystack-2.0-series/)*
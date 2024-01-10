from typing import Dict, Any
from pathlib import Path
from datetime import datetime

from haystack import Pipeline
from haystack.components.websearch import SerperDevWebSearch
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.routers import FileTypeRouter
from haystack.components.rankers import TransformersSimilarityRanker
from haystack.components.builders import PromptBuilder
from haystack.components.caching import CacheChecker
from haystack.components.generators import GPTGenerator
from haystack.components.others import Multiplexer
from haystack.components.joiners import DocumentJoiner
from haystack.components.writers import DocumentWriter

from haystack.document_stores import InMemoryDocumentStore, DuplicatePolicy

template = """
Question: {{ question }}

Context:
{% for document in documents %}
- {{ document.content }}
{% endfor %}

Please reformulate the information above to answer the user's question.
"""
pipe = Pipeline()
cache = InMemoryDocumentStore()
pipe.add_component("query", Multiplexer(str))
pipe.add_component("search", SerperDevWebSearch(top_k=2))
pipe.add_component("cache_checker", CacheChecker(document_store=cache, cache_field="url", cache_field_type=str))
pipe.add_component("fetcher", LinkContentFetcher())
pipe.add_component("filter", FileTypeRouter(mime_types=["text/html"]))
pipe.add_component("converter", HTMLToDocument())
pipe.add_component("cleaner", DocumentCleaner())
pipe.add_component("splitter", DocumentSplitter(split_by="sentence", split_length=3))
pipe.add_component("writer", DocumentWriter(document_store=cache, policy=DuplicatePolicy.SKIP))
pipe.add_component("joiner", DocumentJoiner(sort_by_score=False))
pipe.add_component("ranker", TransformersSimilarityRanker())
pipe.add_component("prompt_builder", PromptBuilder(template=template))
pipe.add_component("llm", GPTGenerator())
pipe.connect("query", "search")
pipe.connect("query", "ranker")
pipe.connect("query", "prompt_builder.question")
pipe.connect("search.links", "cache_checker")
pipe.connect("cache_checker.misses", "fetcher")
pipe.connect("fetcher", "filter")
pipe.connect("filter.text/html", "converter")
pipe.connect("converter", "cleaner")
pipe.connect("cleaner", "splitter")
pipe.connect("splitter", "writer")
pipe.connect("splitter", "joiner")
pipe.connect("cache_checker.hits", "joiner")
pipe.connect("joiner", "ranker")
pipe.connect("ranker", "prompt_builder.documents")
pipe.connect("prompt_builder", "llm")

pipe.draw("pipeline.png")

import json

results = pipe.run({"query": {"value": "What's the official language of the Republic of Rose Island?"}})
print(json.dumps(results, indent=4, default=lambda x: repr(x)))

results = pipe.run({"query": {"value": "What was the official language of the Republic of Rose Island?"}})
print(json.dumps(results, indent=4, default=lambda x: repr(x)))




"""Retrieval over the vault index: text (BM25), vector (kNN) and hybrid
with reciprocal rank fusion, adapted from module 4.

Planned flow (day 3):
  - text_search: BM25 over content and title.
  - vector_search: kNN over the all-MiniLM-L6-v2 embedding of the chunk.
  - hybrid_search: RRF fusion of both rankings.
  - Every function returns chunk dicts with "path" and "content", the
    contract RAGBase expects.
"""

import os

ES_INDEX = os.getenv("ES_INDEX", "obsidian_notes")
EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")


def text_search(query, num_results=5):
    raise NotImplementedError("day 3")


def vector_search(query, num_results=5):
    raise NotImplementedError("day 3")


def hybrid_search(query, num_results=5, k=60):
    raise NotImplementedError("day 3")

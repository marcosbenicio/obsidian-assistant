"""Vault ingestion: read the Obsidian vault, chunk the notes and index
them into Elasticsearch.

Planned flow (day 2):
  1. Walk VAULT_PATH for *.md files, skipping _playground/ and .obsidian/.
  2. Parse frontmatter (tags, dates) with python-frontmatter.
  3. Clean wikilinks [[...]] from the body, keep the link text.
  4. Chunk each note (size=2000, step=1000, from module 3).
  5. Index chunks into ES_INDEX with metadata: path, title, folder,
     tags, modified_at, chunk start.
"""

import os

VAULT_PATH = os.getenv("VAULT_PATH", "/vault")
ES_INDEX = os.getenv("ES_INDEX", "obsidian_notes")


def load_vault():
    raise NotImplementedError("day 2")


def chunk_documents(documents, size=2000, step=1000):
    raise NotImplementedError("day 2")


def index_chunks(chunks):
    raise NotImplementedError("day 2")


if __name__ == "__main__":
    documents = load_vault()
    chunks = chunk_documents(documents)
    index_chunks(chunks)

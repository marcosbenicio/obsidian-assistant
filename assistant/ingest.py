"""Vault ingestion: read the Obsidian vault, chunk the notes and index
them into Elasticsearch."""

import os
import re
from datetime import datetime, timezone
from pathlib import Path

import frontmatter

VAULT_PATH = os.getenv("VAULT_PATH", "/vault")
ES_INDEX = os.getenv("ES_INDEX", "obsidian_notes")

WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
MDLINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def extract_and_clean_links(text):
    """Replace link syntax with its visible text and collect the targets
    of links that point to other notes."""
    links = []

    def wiki_repl(m):
        target, alias = m.group(1), m.group(2)
        links.append(target.strip())
        return alias or target

    def md_repl(m):
        label, target = m.group(1), m.group(2)
        if target.endswith(".md") and not target.startswith("http"):
            links.append(target)
        return label

    text = WIKILINK.sub(wiki_repl, text)
    text = MDLINK.sub(md_repl, text)
    return text, links


def iter_notes(vault):
    """Yield every note file, skipping hidden paths and the staging area."""
    for path in sorted(vault.rglob("*.md")):
        parts = path.relative_to(vault).parts
        if any(p.startswith(".") or p == "_playground" for p in parts):
            continue
        yield path


def load_vault(vault_path=VAULT_PATH):
    """Read the whole vault into a list of documents, one per note."""
    vault = Path(vault_path)
    documents = []

    for path in iter_notes(vault):
        note = frontmatter.load(path)
        content, links = extract_and_clean_links(note.content)
        rel = path.relative_to(vault)

        tags = note.metadata.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]

        documents.append({
            "path": str(rel),
            "title": path.stem,
            "folder": str(rel.parent) if str(rel.parent) != "." else "",
            "tags": tags,
            "links": links,
            "content": content,
            "modified_at": datetime.fromtimestamp(
                path.stat().st_mtime, tz=timezone.utc
            ).isoformat(),
        })

    return documents


def chunk_documents(documents, size=2000, step=1000):
    raise NotImplementedError("next step")


def index_chunks(chunks):
    raise NotImplementedError("next step")


if __name__ == "__main__":
    documents = load_vault()
    print(f"loaded {len(documents)} notes from {VAULT_PATH}")

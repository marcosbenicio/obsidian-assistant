# Obsidian Assistant

A personal knowledge assistant for an Obsidian vault: ask questions in
natural language and get answers grounded in your own notes, with sources.

Built as the final project of LLM Zoomcamp 2026. Retrieval is hybrid
(BM25 + dense vectors with reciprocal rank fusion) over Elasticsearch,
generation uses gpt-5.4-mini, every conversation is logged to Postgres
with tokens, cost and latency, answers are evaluated online by an LLM
judge and by user feedback, and Grafana dashboards monitor the whole
system. No LLM frameworks: plain Python, every layer inspectable.

Long term vision in [VISION.md](../llm-zoomcamp-2026/VISION.md): this is
phase 1 of a second brain that synthesizes new notes under human approval.

## Status

Under construction (12-day sprint).

- [x] Skeleton, compose stack, package layout
- [ ] Vault ingestion into Elasticsearch
- [ ] Hybrid retrieval
- [ ] Streamlit app with feedback
- [ ] Retrieval evaluation (hit rate, MRR)
- [ ] LLM judge
- [ ] Grafana dashboards
- [ ] Reproducibility pass

## Quickstart (will be finalized)

```bash
cp .env.example .env   # fill OPENAI_API_KEY and VAULT_PATH
docker compose up -d
make init-db
make ingest
# open http://localhost:8501
```

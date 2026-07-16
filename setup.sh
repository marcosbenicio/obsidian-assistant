#!/bin/bash
# Stack cheatsheet. Usage: ./setup.sh

set -a
source .env 2>/dev/null
set +a

cat <<EOF

================================================================
  Container status
================================================================
EOF

docker compose ps --format "  {{.Name}}: {{.Status}}" 2>/dev/null \
  || echo "  (stack not running or compose not found)"

cat <<EOF

================================================================
  URLs
================================================================

  App (Streamlit):  http://localhost:${APP_PORT:-8501}
  Jupyter Lab:      http://localhost:${JUPYTER_PORT:-8888}/?token=${JUPYTER_TOKEN:-dev}
  Grafana:          http://localhost:${GRAFANA_PORT:-3000}   (admin / ${GRAFANA_PASSWORD:-admin})
  Elasticsearch:    http://localhost:${ES_PORT:-9200}
  Postgres:         postgresql://${POSTGRES_USER:-user}:...@localhost:${POSTGRES_PORT:-5432}/obsidian_assistant
  Ollama (opt-in):  http://localhost:${OLLAMA_PORT:-11434}  (docker compose --profile ollama up -d)

================================================================
  Key environment (masked)
================================================================

  OPENAI_API_KEY = ${OPENAI_API_KEY:0:10}...
  VAULT_PATH     = ${VAULT_PATH:-./demo_vault (default)}
  LLM_MODEL      = ${LLM_MODEL:-gpt-5.4-mini (default)}
  LLM_BASE_URL   = ${LLM_BASE_URL:-(unset: OpenAI API)}
  EMBED_MODEL    = ${EMBED_MODEL:-all-MiniLM-L6-v2 (default)}
  ES_INDEX       = ${ES_INDEX:-obsidian_notes (default)}

================================================================
  Quick CLI
================================================================

  Postgres (interactive psql):
    docker compose exec postgres psql -U ${POSTGRES_USER:-user} -d obsidian_assistant

  Elasticsearch health:
    curl -s http://localhost:${ES_PORT:-9200}/_cluster/health | jq

  Index document count:
    curl -s http://localhost:${ES_PORT:-9200}/${ES_INDEX:-obsidian_notes}/_count | jq

  App logs:
    docker compose logs -f app

================================================================
  Make targets
================================================================

  make up / down     start / stop the stack
  make build         rebuild image after requirements change
  make init-db       create tables (idempotent)
  make ingest        index the vault into elasticsearch
  make check-db      last 10 conversations
  make urls          the URLs above

================================================================

EOF

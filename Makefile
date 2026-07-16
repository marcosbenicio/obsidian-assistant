# All targets run against this folder's compose stack. The app and notebook
# services share one image; code is bind-mounted, so edits apply live.

EXEC = docker compose exec --workdir /app app

up:
	docker compose up -d

build:
	docker compose up -d --build

down:
	docker compose down

init-db:
	$(EXEC) python db.py

ingest:
	$(EXEC) python ingest.py

check-db:
	docker compose exec postgres psql -U user -d obsidian_assistant \
		-c "SELECT id, question, source, cost, timestamp FROM conversations ORDER BY id DESC LIMIT 10;"

logs:
	docker compose logs -f app

urls:
	@echo "App:      http://localhost:8501"
	@echo "Jupyter:  http://localhost:8888/?token=$${JUPYTER_TOKEN:-dev}"
	@echo "Grafana:  http://localhost:3000  (admin / admin)"
	@echo "Elastic:  http://localhost:9200"

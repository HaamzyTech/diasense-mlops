.PHONY: install up down logs test lint format dvc-repro mlflow-ui airflow-ui grafana-ui seed-model migrate

install:
	pip install -r apps/backend-api/requirements.txt
	cd apps/frontend && npm install

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

test:
	pytest -q apps/backend-api/tests ml/tests

lint:
	cd apps/frontend && npm run lint

format:
	python -m pip install ruff black >/dev/null 2>&1 || true
	black apps/backend-api/app ml/src airflow/dags

dvc-repro:
	dvc repro

mlflow-ui:
	@echo "MLflow UI: http://localhost:$${MLFLOW_TRACKING_PORT:-5000}"

airflow-ui:
	@echo "Airflow UI: http://localhost:$${AIRFLOW_WEBSERVER_PORT:-8080}"

grafana-ui:
	@echo "Grafana UI: http://localhost:$${GRAFANA_PORT:-3001}"

seed-model:
	python apps/backend-api/app/db/init_db.py

migrate:
	cd apps/backend-api && alembic upgrade head

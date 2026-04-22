# diasense-mlops

End-to-end MLOps monorepo for diabetes risk prediction with a Next.js frontend, FastAPI backend, ML training pipeline (DVC + MLflow), Airflow orchestration, and Prometheus/Grafana observability.

## 1) Project overview
`diasense-mlops` provides:
- **User workflow**: submit risk-factor inputs in the UI and receive a diabetes risk estimate.
- **Backend workflow**: persist request/response metadata, proxy scoring to model-server, expose ops/metrics APIs.
- **ML workflow**: execute deterministic data-to-model pipeline via DVC; register/run tracking via MLflow.
- **Ops workflow**: orchestrate training and monitoring DAGs in Airflow and visualize service metrics in Grafana.

## 2) Final architecture summary
- **Frontend (`frontend`)**: Next.js app calling backend REST APIs.
- **Backend (`backend-api`)**: FastAPI service with `/api/v1/*` endpoints, PostgreSQL persistence, Prometheus metrics.
- **Model server (`model-server`)**: MLflow model serving endpoint on port `5001`.
- **Pipeline (`dvc`, `airflow`)**: DVC defines stages (`ingest -> validate -> preprocess -> train -> evaluate -> register`), Airflow schedules and records pipeline runs.
- **Monitoring (`prometheus`, `grafana`)**: Prometheus scrapes backend metrics, Grafana dashboards render infra/API/ML views.

## 3) Prerequisites
- Linux/macOS shell (or WSL2 on Windows)
- Docker Engine + Docker Compose plugin
- Python 3.12
- Node.js 24.14.x + npm
- Git

## 4) Exact packages/tools to install
Use these exact versions (or patch versions compatible with them):

### System tools
```bash
# Ubuntu/Debian example
sudo apt-get update
sudo apt-get install -y git make docker.io docker-compose-plugin
```

### Python runtime/tooling
```bash
# pyenv example
pyenv install 3.12.9
pyenv local 3.12.9
python -m pip install --upgrade pip==25.1.1 setuptools==80.9.0 wheel==0.45.1
python -m pip install dvc==3.60.1 pytest==8.3.5
```

### Node runtime/tooling
```bash
# nvm example
nvm install 24.14.0
nvm use 24.14.0
npm install -g npm@11.4.2
```

## 5) Exact versions used by containers/services
- PostgreSQL: `postgres:17-alpine`
- Backend runtime image: `python:3.12-alpine`
- Frontend runtime image: `node:24.14-alpine`
- Airflow: `apache/airflow:3.2.0-python3.12`
- MLflow tracking image: `ghcr.io/mlflow/mlflow:v3.11.0`
- Prometheus: `prom/prometheus:latest`
- Grafana: `grafana/grafana-oss:latest`

## 6) Clone, configure env, build, migrate, train, serve, run
```bash
git clone <YOUR_REPO_URL> diasense-mlops
cd diasense-mlops

cp .env.example .env
cp apps/backend-api/.env.example apps/backend-api/.env
cp apps/frontend/.env.example apps/frontend/.env

python -m venv .venv
source .venv/bin/activate

# backend + frontend local deps
make install

# apply DB migrations (requires postgres running/reachable)
make migrate

# seed default active model metadata row
make seed-model

# run ML training pipeline locally via DVC
make dvc-repro

# run API/frontend locally (non-docker option)
# terminal A
cd apps/backend-api && uvicorn app.main:app --host 0.0.0.0 --port 8000
# terminal B
cd apps/frontend && npm run dev
```

## 7) Launch with Docker Compose
```bash
# build and start everything
make up

# verify effective compose config
docker compose config

# view logs
make logs

# shutdown
make down
```

## 8) Run DVC pipeline
```bash
# from repo root
make dvc-repro
# OR stage-wise
dvc repro ingest
dvc repro validate
dvc repro preprocess
dvc repro train
dvc repro evaluate
dvc repro register
```

## 9) Trigger Airflow DAGs
```bash
# training DAG
docker compose exec airflow-webserver airflow dags trigger diasense_training_pipeline

# monitoring DAG
docker compose exec airflow-webserver airflow dags trigger diasense_monitoring_pipeline

# list DAG runs
docker compose exec airflow-webserver airflow dags list-runs -d diasense_training_pipeline
docker compose exec airflow-webserver airflow dags list-runs -d diasense_monitoring_pipeline
```

## 10) Access URLs
- Frontend: `http://localhost:3000`
- Backend API root: `http://localhost:8000`
- Backend health: `http://localhost:8000/api/v1/health`
- MLflow: `http://localhost:5000`
- Airflow: `http://localhost:8080`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001`

## 11) Reproduce training run by Git commit + MLflow run ID + DVC rev
1. Capture metadata:
```bash
git rev-parse HEAD
# example output: <GIT_COMMIT_HASH>

# inspect latest register artifact for mlflow run id
cat ml/artifacts/reports/register.json
# extract: mlflow_run_id + dvc_rev (if present)
```
2. Checkout exact commit and pull artifacts:
```bash
git checkout <GIT_COMMIT_HASH>
dvc pull -r origin
```
3. Re-run pipeline deterministically:
```bash
dvc repro
```
4. Validate MLflow run in UI (`http://localhost:5000`) with `mlflow_run_id` from `register.json`.

## 12) Troubleshooting
- **`ModuleNotFoundError` in ML scripts/tests**: run commands from repo root; ensure venv active; reinstall with `make install`.
- **Backend cannot connect to DB**: check `.env` DB values and that `postgres` service is healthy (`docker compose ps`).
- **Model server 404/500**: ensure a Production-stage model exists in MLflow model registry and `MODEL_SERVER_URL` points to `http://model-server:5001`.
- **Airflow DAG import errors**: confirm `airflow/Dockerfile` copied `dags`, `ml`, and `dvc.yaml` to `/opt/airflow`.
- **Frontend cannot reach API**: set `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000` in `apps/frontend/.env` for local browser execution.
- **DVC repro failures**: verify `ml/data/*` folders are writable and required Python deps are installed.

## 13) Alpine exception note
Alpine-based images are used where practical (`postgres`, backend runtime, frontend runtime). Airflow uses the official Debian-based `apache/airflow:3.2.0-python3.12` because Airflow provider compatibility and packaging are not reliably supported on Alpine.

---

## Final run order commands
```bash
cp .env.example .env
cp apps/backend-api/.env.example apps/backend-api/.env
cp apps/frontend/.env.example apps/frontend/.env
make up
make migrate
make seed-model
make dvc-repro
docker compose exec airflow-webserver airflow dags trigger diasense_training_pipeline
docker compose exec airflow-webserver airflow dags trigger diasense_monitoring_pipeline
```

## Known limitations
- Demo risk interpretation is model-dependent and not a clinical diagnosis.
- `prom/prometheus:latest` and `grafana/grafana-oss:latest` are floating tags (pin for strict reproducibility).
- Airflow in LocalExecutor mode is not horizontally scalable.

## Future improvements
- Pin Prometheus/Grafana image versions.
- Add automated DB migration checks in CI against ephemeral Postgres.
- Add OpenAPI schema contract tests and load tests for `/predict`.

# Architecture Overview

## Components
- `apps/frontend`: Next.js web app.
- `apps/backend-api`: FastAPI service + SQLAlchemy + Alembic.
- `ml/src`: DVC-controlled ML pipeline code.
- `airflow/dags`: orchestration for training and monitoring.
- `infra/prometheus`, `infra/grafana`: observability stack.

## Cross-component interactions
- Frontend -> Backend API (`/api/v1/*`).
- Backend -> Postgres (requests/results/feedback/pipeline/drift metadata).
- Backend -> Model server for scoring.
- Backend -> MLflow tracking metadata read/links.
- Airflow -> DVC CLI for deterministic stage execution.
- Prometheus -> Backend `/metrics`; Grafana -> Prometheus.

## Deployment topology
See Mermaid diagrams:
- `diagrams/high_level_architecture.mmd`
- `diagrams/low_level_architecture.mmd`

## Reliability and operability
- Health endpoints: `/api/v1/health`, `/api/v1/ready`.
- Persistent volumes for DB and MLflow.
- Airflow run logging into `pipeline_runs`.
- Backend middleware exports metrics for scraping.

## Hardening checklist applied
- Normalized ML import paths to package-safe `ml.src.utils.*` imports.
- Standardized frontend env variable to `NEXT_PUBLIC_API_BASE_URL`.
- CI expanded to install deps and run backend/ml/frontend checks.
- Documentation aligned with existing services, routes, ports, and DAG IDs.

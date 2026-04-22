# High-Level Design (HLD)

## Problem statement
Healthcare teams need a reproducible way to estimate diabetes risk from structured patient factors, while maintaining traceability from data/model lineage to prediction outcomes and operational health.

## Why this architecture was chosen
This architecture separates concerns into independently deployable services:
- Faster iteration on UI/API/ML layers.
- Independent scaling and failure isolation.
- Clear audit trail across DVC, MLflow, Airflow, and PostgreSQL.

## Service separation rationale
- **frontend**: user-facing form and results visualization.
- **backend-api**: source of truth for validation, persistence, and API contracts.
- **model-server**: stateless serving endpoint backed by MLflow registry model artifacts.
- **pipeline**: DVC for deterministic stage graph + Airflow for scheduling and operations.
- **monitoring**: Prometheus for metric collection and Grafana for dashboards.

## Operational flow
1. User submits features from frontend.
2. Backend validates request, writes `prediction_requests`.
3. Backend calls model-server `/invocations` compatible scoring path.
4. Backend writes `prediction_results` and returns risk response.
5. Clinician feedback saved in `feedback_labels`.
6. Airflow training DAG executes DVC stages and records `pipeline_runs`.
7. Monitoring DAG updates drift artifacts and emits status signals.

## Deployment model
- Local/dev deployment via `docker-compose.yml`.
- Stateful components (Postgres, MLflow artifacts) mounted as volumes.
- Service ports exposed for local observability and manual operations.

## Security assumptions
- Trusted internal network in local compose setup.
- No PHI hardening by default (demo system).
- Environment variables hold credentials/secrets; `.env` must not be committed.
- Validation constraints protect obvious malformed numeric inputs.

## Success metrics
- API health/ready availability.
- P95 prediction latency and error rate.
- Training pipeline success rate and duration.
- Drift status trend and alert frequency.
- Feedback label capture coverage over predictions.

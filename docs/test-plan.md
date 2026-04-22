# Test Plan

## Acceptance criteria
- User can submit valid prediction form and receive risk output.
- Backend persists requests/results and returns retrievable records.
- DVC pipeline completes all stages and produces expected artifacts.
- Airflow DAGs can be triggered and pipeline run rows are recorded.
- Frontend build and lint pass in CI.

## Unit tests
- ML preprocessing transforms and column handling.
- ML validation schema checks and report generation.
- Backend prediction service logic (banding/response mapping).

## Integration tests
- Backend endpoint-to-service integration for `/predict` and `/ready`.
- DB repository write/read paths for predictions and feedback.
- Model registry metadata retrieval for `/model/info`.

## API tests
- `GET /api/v1/health` returns 200 and expected shape.
- `GET /api/v1/ready` returns dependencies map.
- `POST /api/v1/predict` validates bounds and error handling.
- `POST /api/v1/feedback` returns 201 with `feedback_id`.

## Pipeline tests
- `dvc repro` all stages from clean workspace.
- Verify expected output files exist under `ml/artifacts/reports` and `ml/artifacts/models`.
- Trigger Airflow DAGs and confirm entries in `pipeline_runs`.

## Expected results
- No import/runtime failures for backend/ml test collection.
- Deterministic stage order in DVC.
- API contracts match documented request/response payloads.
- CI verifies backend tests, ML tests, frontend lint/build, DVC structure checks.

## Manual test checklist
- [ ] Launch compose stack.
- [ ] Open frontend and submit a prediction.
- [ ] Confirm result page renders risk band.
- [ ] Submit clinician feedback.
- [ ] Open `/api/v1/ops/summary` and verify statuses.
- [ ] Trigger training DAG; verify run appears.
- [ ] Open Grafana dashboards and confirm Prometheus datasource availability.

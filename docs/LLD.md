# Low-Level Design (LLD)

## 1. Endpoint definitions
Base prefix: `/api/v1`

### Health
- `GET /health`
  - Response: `{ status, service, version, timestamp }`
- `GET /ready`
  - Response: `{ status, dependencies: {postgres, model_server, mlflow_tracking}, timestamp }`

### Model
- `GET /model/info`
  - Response: `{ model_name, model_version, algorithm, stage, mlflow_run_id, metrics }`

### Prediction
- `POST /predict`
  - Request body:
    - `session_id: UUID`
    - `actor_role: string`
    - `pregnancies: int [0,30]`
    - `glucose: float [0,300]`
    - `blood_pressure: float [0,200]`
    - `skin_thickness: float [0,100]`
    - `insulin: float [0,1000]`
    - `bmi: float [0,100]`
    - `diabetes_pedigree_function: float [0,10]`
    - `age: int [1,120]`
  - Response body:
    - `request_id: UUID`
    - `model_version_id: UUID`
    - `predicted_label: bool`
    - `risk_probability: float`
    - `risk_band: string`
    - `interpretation: string`
    - `top_factors: [{feature, importance}]`
    - `latency_ms: int`
    - `created_at: string`

### Prediction history
- `GET /predictions/{request_id}`
- `GET /predictions?session_id=<uuid>&limit=<1..100>`

### Feedback
- `POST /feedback`
  - Request: `{ request_id, ground_truth_label, label_source, notes? }`
  - Response: `{ message, feedback_id }`

### Drift
- `GET /drift/latest`
  - Response: `{ report_date, overall_status, features[] }`

### Pipeline
- `GET /pipeline/runs?limit=<1..100>`
  - Response: `{ items[], count }`

### Ops summary
- `GET /ops/summary`
  - Response includes service status map, active model, latest pipeline + drift status.

## 2. Database schema (exact logical tables)
- `model_versions`
- `prediction_requests`
- `prediction_results`
- `feedback_labels`
- `drift_reports`
- `pipeline_runs`
- `system_events`

Important enums/types:
- `actor_role`: `patient | clinician | admin`
- `pipeline_status`: `queued | running | success | failed`
- `risk_band`: `low | moderate | high`

## 3. Data flow (UI -> API -> model-server -> DB)
1. UI posts `/api/v1/predict`.
2. API validates payload constraints (Pydantic + DB constraints).
3. API persists request row (`prediction_requests`).
4. API calls model-server (MLflow serving endpoint).
5. API computes/normalizes risk band + explanation payload.
6. API persists response row (`prediction_results`).
7. UI fetches detail via `/api/v1/predictions/{request_id}`.

## 4. Airflow DAG flow
### `diasense_training_pipeline`
`ingest -> validate -> preprocess -> train -> evaluate -> register -> record_pipeline_run_success_or_failure`

### `diasense_monitoring_pipeline`
`recompute_current_feature_stats_from_recent_data -> compare_against_baseline -> persist_drift_report -> emit_alert_metrics`

## 5. DVC stage flow
`ingest -> validate -> preprocess -> train -> evaluate -> register`

Artifacts include:
- raw/validated/processed datasets
- train/val/test feature splits
- best model pickle
- evaluation + training JSON reports
- register metadata report

## 6. Error handling behavior
- Domain/application errors return explicit `AppError` status + message.
- Request validation failures return `422` with field-level detail.
- Unhandled exceptions return `500` + generic message.
- `/ready` degrades dependency status per downstream health check result.

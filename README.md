# diasense-mlops

Production-ready MLOps monorepo scaffold for diabetes risk prediction.

## Container image choices
- Alpine used where practical (`postgres:17-alpine`, `python:3.12-alpine`, `node:24.14-alpine`, `prom/prometheus`, `grafana/grafana-oss`).
- `apache/airflow:3.2.0-python3.12` used because official Airflow distribution and dependency ecosystem are not reliably supported on Alpine.
- `ghcr.io/mlflow/mlflow:v3.11.0` is used for tracking and model serving stability with MLflow packaging.

## Quick start
1. Copy envs: `cp .env.example .env` and service `.env.example` files.
2. Build and start: `make up`
3. Open:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - MLflow: http://localhost:5000
   - Airflow: http://localhost:8080
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3001

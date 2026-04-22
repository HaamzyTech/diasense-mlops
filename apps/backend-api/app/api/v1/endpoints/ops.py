from fastapi import APIRouter

router = APIRouter(prefix="/ops")


@router.get("/summary")
def get_ops_summary() -> dict:
    # TODO: Build live ops summary from dependencies and DB.
    return {
        "services": {
            "backend_api": "ok",
            "model_server": "ok",
            "postgres": "ok",
            "mlflow_tracking": "ok",
            "airflow_webserver": "ok",
            "prometheus": "ok",
            "grafana": "ok",
        },
        "active_model": {
            "model_name": "diasense-diabetes-risk",
            "model_version": "1",
            "stage": "Production",
        },
        "latest_pipeline_status": "success",
        "latest_drift_status": "stable",
    }

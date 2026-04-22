from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_drift_service, get_model_registry_service, get_pipeline_service
from app.schemas.ops import OpsSummaryResponse

router = APIRouter(prefix="/ops")


@router.get("/summary", response_model=OpsSummaryResponse)
def get_ops_summary(db: Session = Depends(get_db)) -> OpsSummaryResponse:
    model = get_model_registry_service(db).get_active_model()
    pipeline_status = get_pipeline_service(db).latest_status()
    drift = get_drift_service(db).latest()

    return OpsSummaryResponse(
        services={
            "backend_api": "ok",
            "model_server": "ok",
            "postgres": "ok",
            "mlflow_tracking": "ok",
            "airflow_webserver": "ok",
            "prometheus": "ok",
            "grafana": "ok",
        },
        active_model={
            "model_name": model["model_name"],
            "model_version": model["model_version"],
            "stage": model["stage"],
        },
        latest_pipeline_status=pipeline_status,
        latest_drift_status=drift["overall_status"],
    )

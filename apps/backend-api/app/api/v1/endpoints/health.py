from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def get_health() -> dict:
    return {
        "status": "ok",
        "service": "backend-api",
        "version": "0.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/ready")
def get_ready() -> dict:
    return {
        "status": "ready",
        "dependencies": {
            "postgres": "ok",
            "model_server": "ok",
            "mlflow_tracking": "ok",
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

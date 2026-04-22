from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import get_settings

router = APIRouter()


@router.get("/health")
def get_health() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


@router.get("/ready")
def get_ready(db: Session = Depends(get_db)) -> dict:
    settings = get_settings()
    deps = {"postgres": "error", "model_server": "error", "mlflow_tracking": "error"}

    try:
        db.execute(text("SELECT 1"))
        deps["postgres"] = "ok"
    except Exception:
        deps["postgres"] = "error"

    try:
        with httpx.Client(timeout=settings.request_timeout_seconds) as client:
            resp = client.get(f"{settings.model_server_url}/ping")
            deps["model_server"] = "ok" if resp.status_code < 500 else "error"
    except Exception:
        deps["model_server"] = "error"

    try:
        with httpx.Client(timeout=settings.request_timeout_seconds) as client:
            resp = client.get(f"{settings.mlflow_tracking_uri}/")
            deps["mlflow_tracking"] = "ok" if resp.status_code < 500 else "error"
    except Exception:
        deps["mlflow_tracking"] = "error"

    return {
        "status": "ready",
        "dependencies": deps,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

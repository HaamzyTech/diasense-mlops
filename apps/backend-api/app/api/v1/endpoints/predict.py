from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter

from app.schemas.predict import PredictRequest

router = APIRouter()


@router.post("/predict")
def predict(payload: PredictRequest) -> dict:
    # TODO: Persist request and call model-server via PredictionService.
    _ = payload
    return {
        "request_id": str(uuid4()),
        "model_version_id": str(uuid4()),
        "predicted_label": True,
        "risk_probability": 0.8123,
        "risk_band": "high",
        "interpretation": "High predicted diabetes risk. This tool does not provide a medical diagnosis.",
        "top_factors": [
            {"feature": "glucose", "importance": 0.41},
            {"feature": "bmi", "importance": 0.22},
            {"feature": "age", "importance": 0.14},
        ],
        "latency_ms": 42,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

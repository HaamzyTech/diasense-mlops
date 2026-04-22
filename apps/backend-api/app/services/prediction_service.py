from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter
from uuid import UUID

from app.clients.model_server import ModelServerClient
from app.core.exceptions import NotFoundError, ValidationError
from app.metrics.prometheus import PREDICTION_COUNT
from app.repositories.model_version_repository import ModelVersionRepository
from app.repositories.prediction_repository import PredictionRepository


def map_risk_band(probability: float) -> str:
    if probability < 0.33:
        return "low"
    if probability < 0.66:
        return "moderate"
    return "high"


def interpretation_for_band(risk_band: str) -> str:
    mapping = {
        "low": "Low predicted diabetes risk. This tool does not provide a medical diagnosis.",
        "moderate": (
            "Moderate predicted diabetes risk. Consider discussing results with a healthcare professional. "
            "This tool does not provide a medical diagnosis."
        ),
        "high": "High predicted diabetes risk. This tool does not provide a medical diagnosis.",
    }
    return mapping[risk_band]


class PredictionService:
    def __init__(
        self,
        prediction_repo: PredictionRepository,
        model_repo: ModelVersionRepository,
        model_server_client: ModelServerClient,
    ) -> None:
        self.prediction_repo = prediction_repo
        self.model_repo = model_repo
        self.model_server_client = model_server_client

    def create_prediction(self, payload: dict) -> dict:
        request_row = self.prediction_repo.create_request(payload)

        active_model = self.model_repo.get_active()
        if not active_model:
            raise NotFoundError("No active model available for inference")

        start = perf_counter()
        model_output = self.model_server_client.invoke(
            [
                {
                    "pregnancies": payload["pregnancies"],
                    "glucose": payload["glucose"],
                    "blood_pressure": payload["blood_pressure"],
                    "skin_thickness": payload["skin_thickness"],
                    "insulin": payload["insulin"],
                    "bmi": payload["bmi"],
                    "diabetes_pedigree_function": payload["diabetes_pedigree_function"],
                    "age": payload["age"],
                }
            ]
        )
        latency_ms = int((perf_counter() - start) * 1000)

        first = model_output[0] if model_output else {}
        probability = float(first.get("risk_probability", 0.0))
        if not 0 <= probability <= 1:
            raise ValidationError("Model-server returned out-of-range probability")

        risk_band = map_risk_band(probability)
        interpretation = interpretation_for_band(risk_band)
        predicted_label = bool(first.get("predicted_label", probability >= 0.5))
        top_factors = first.get("top_factors", [])

        result_payload = {
            "request_id": str(request_row["id"]),
            "model_version_id": str(active_model["id"]),
            "predicted_label": predicted_label,
            "risk_probability": probability,
            "risk_band": risk_band,
            "explanation": '{"top_factors": ' + str(top_factors).replace("'", '"') + "}",
            "latency_ms": latency_ms,
        }
        result_row = self.prediction_repo.create_result(result_payload)

        created_at = result_row["created_at"]
        if isinstance(created_at, datetime):
            created_at_text = created_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        else:
            created_at_text = str(created_at)

        PREDICTION_COUNT.labels(risk_band=risk_band).inc()

        return {
            "request_id": request_row["id"],
            "model_version_id": UUID(str(active_model["id"])),
            "predicted_label": predicted_label,
            "risk_probability": round(probability, 4),
            "risk_band": risk_band,
            "interpretation": interpretation,
            "top_factors": top_factors,
            "latency_ms": latency_ms,
            "created_at": created_at_text,
        }

    def get_prediction(self, request_id: UUID) -> dict:
        row = self.prediction_repo.get_prediction(request_id=request_id)
        if not row:
            raise NotFoundError(f"Prediction request {request_id} not found")

        request = {
            "id": row["id"],
            "session_id": row["session_id"],
            "actor_role": row["actor_role"],
            "pregnancies": row["pregnancies"],
            "glucose": float(row["glucose"]),
            "blood_pressure": float(row["blood_pressure"]),
            "skin_thickness": float(row["skin_thickness"]),
            "insulin": float(row["insulin"]),
            "bmi": float(row["bmi"]),
            "diabetes_pedigree_function": float(row["diabetes_pedigree_function"]),
            "age": row["age"],
            "created_at": row["created_at"],
        }
        result = {
            "id": row.get("result_id"),
            "model_version_id": row.get("model_version_id"),
            "predicted_label": row.get("predicted_label"),
            "risk_probability": float(row["risk_probability"]) if row.get("risk_probability") is not None else None,
            "risk_band": row.get("risk_band"),
            "explanation": row.get("explanation"),
            "latency_ms": row.get("latency_ms"),
            "created_at": row.get("result_created_at"),
        }
        return {"request": request, "result": result}

    def list_predictions(self, session_id: UUID, limit: int = 20) -> dict:
        items = self.prediction_repo.list_predictions(session_id=session_id, limit=limit)
        for item in items:
            item["risk_probability"] = round(float(item["risk_probability"]), 4)
            item["created_at"] = str(item["created_at"])
            item["request_id"] = str(item["request_id"])
        return {"items": items, "count": len(items)}

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session


class PredictionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_request(self, payload: dict) -> dict:
        stmt = text(
            """
            INSERT INTO prediction_requests (
                session_id, actor_role, pregnancies, glucose, blood_pressure, skin_thickness,
                insulin, bmi, diabetes_pedigree_function, age, source
            ) VALUES (
                :session_id, :actor_role, :pregnancies, :glucose, :blood_pressure, :skin_thickness,
                :insulin, :bmi, :diabetes_pedigree_function, :age, 'web'
            )
            RETURNING id, created_at
            """
        )
        row = self.db.execute(stmt, payload).mappings().one()
        self.db.commit()
        return dict(row)

    def create_result(self, payload: dict) -> dict:
        stmt = text(
            """
            INSERT INTO prediction_results (
                request_id, model_version_id, predicted_label, risk_probability, risk_band, explanation, latency_ms
            ) VALUES (
                :request_id, :model_version_id, :predicted_label, :risk_probability, :risk_band, :explanation::jsonb, :latency_ms
            ) RETURNING id, created_at
            """
        )
        row = self.db.execute(stmt, payload).mappings().one()
        self.db.commit()
        return dict(row)

    def get_prediction(self, request_id: UUID) -> dict | None:
        stmt = text(
            """
            SELECT pr.*, res.id AS result_id, res.model_version_id, res.predicted_label, res.risk_probability,
                   res.risk_band, res.explanation, res.latency_ms, res.created_at AS result_created_at
            FROM prediction_requests pr
            LEFT JOIN prediction_results res ON pr.id = res.request_id
            WHERE pr.id = :request_id
            """
        )
        row = self.db.execute(stmt, {"request_id": str(request_id)}).mappings().first()
        return dict(row) if row else None

    def list_predictions(self, session_id: UUID, limit: int) -> list[dict]:
        stmt = text(
            """
            SELECT pr.id AS request_id, res.risk_probability, res.risk_band, res.created_at
            FROM prediction_requests pr
            JOIN prediction_results res ON pr.id = res.request_id
            WHERE pr.session_id = :session_id
            ORDER BY res.created_at DESC
            LIMIT :limit
            """
        )
        rows = self.db.execute(stmt, {"session_id": str(session_id), "limit": limit}).mappings().all()
        return [dict(row) for row in rows]

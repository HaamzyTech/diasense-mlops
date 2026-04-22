from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_prediction_service
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/predictions")


@router.get("/{request_id}")
def get_prediction(request_id: UUID, db: Session = Depends(get_db)) -> dict:
    service: PredictionService = get_prediction_service(db)
    return service.get_prediction(request_id)


@router.get("")
def list_predictions(session_id: UUID, limit: int = Query(default=20, ge=1, le=100), db: Session = Depends(get_db)) -> dict:
    service: PredictionService = get_prediction_service(db)
    return service.list_predictions(session_id=session_id, limit=limit)

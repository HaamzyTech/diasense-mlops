from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_drift_service
from app.schemas.drift import DriftResponse
from app.services.drift_service import DriftService

router = APIRouter(prefix="/drift")


@router.get("/latest", response_model=DriftResponse)
def get_latest_drift(db: Session = Depends(get_db)) -> DriftResponse:
    service: DriftService = get_drift_service(db)
    return DriftResponse(**service.latest())

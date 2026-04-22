from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_model_registry_service
from app.schemas.model_info import ModelInfoResponse
from app.services.model_registry_service import ModelRegistryService

router = APIRouter(prefix="/model")


@router.get("/info", response_model=ModelInfoResponse)
def get_model_info(
    db: Session = Depends(get_db),
) -> ModelInfoResponse:
    service: ModelRegistryService = get_model_registry_service(db)
    model = service.get_active_model()
    return ModelInfoResponse(
        model_name=model["model_name"],
        model_version=model["model_version"],
        algorithm=model["algorithm"],
        stage=model["stage"],
        mlflow_run_id=model["mlflow_run_id"],
        metrics=model["metrics"] or {},
    )

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_pipeline_service
from app.schemas.pipeline import PipelineRunsResponse
from app.services.pipeline_service import PipelineService

router = APIRouter(prefix="/pipeline")


@router.get("/runs", response_model=PipelineRunsResponse)
def list_pipeline_runs(limit: int = Query(default=20, ge=1, le=100), db: Session = Depends(get_db)) -> PipelineRunsResponse:
    service: PipelineService = get_pipeline_service(db)
    return PipelineRunsResponse(**service.list_runs(limit=limit))

from fastapi import APIRouter

router = APIRouter(prefix="/pipeline")


@router.get("/runs")
def list_pipeline_runs(limit: int = 20) -> dict:
    # TODO: Return pipeline run history.
    _ = limit
    return {"items": [], "count": 0}

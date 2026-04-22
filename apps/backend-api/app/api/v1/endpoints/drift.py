from fastapi import APIRouter

router = APIRouter(prefix="/drift")


@router.get("/latest")
def get_latest_drift() -> dict:
    # TODO: Aggregate latest drift report.
    return {"report_date": "2026-04-21", "overall_status": "stable", "features": []}

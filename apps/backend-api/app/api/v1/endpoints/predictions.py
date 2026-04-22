from fastapi import APIRouter

router = APIRouter(prefix="/predictions")


@router.get("/{request_id}")
def get_prediction(request_id: str) -> dict:
    # TODO: Load request/result by request_id from database.
    return {"request": {"id": request_id}, "result": {}}


@router.get("")
def list_predictions(session_id: str, limit: int = 20) -> dict:
    # TODO: Query predictions by session_id with limit.
    _ = (session_id, limit)
    return {"items": [], "count": 0}

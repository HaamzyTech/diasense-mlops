from uuid import uuid4

from fastapi import APIRouter, status

from app.schemas.feedback import FeedbackRequest

router = APIRouter()


@router.post("/feedback", status_code=status.HTTP_201_CREATED)
def create_feedback(payload: FeedbackRequest) -> dict:
    # TODO: Store feedback_labels row.
    _ = payload
    return {"message": "Feedback recorded", "feedback_id": str(uuid4())}

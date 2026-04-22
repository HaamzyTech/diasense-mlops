from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_feedback_repo
from app.schemas.feedback import FeedbackRequest, FeedbackResponse

router = APIRouter()


@router.post("/feedback", status_code=status.HTTP_201_CREATED, response_model=FeedbackResponse)
def create_feedback(payload: FeedbackRequest, db: Session = Depends(get_db)) -> FeedbackResponse:
    repo = get_feedback_repo(db)
    row = repo.create_feedback(payload.model_dump(mode="json"))
    return FeedbackResponse(message="Feedback recorded", feedback_id=row["id"])

from uuid import UUID

from pydantic import BaseModel


class FeedbackRequest(BaseModel):
    request_id: UUID
    ground_truth_label: bool
    label_source: str
    notes: str | None = None

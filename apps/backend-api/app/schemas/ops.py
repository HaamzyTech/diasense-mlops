from pydantic import BaseModel


class OpsSummaryResponse(BaseModel):
    services: dict[str, str]
    active_model: dict[str, str]
    latest_pipeline_status: str
    latest_drift_status: str

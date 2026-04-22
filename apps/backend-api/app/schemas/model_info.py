from pydantic import BaseModel


class ModelInfoResponse(BaseModel):
    model_name: str
    model_version: str
    algorithm: str
    stage: str
    mlflow_run_id: str
    metrics: dict

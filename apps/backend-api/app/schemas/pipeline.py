from pydantic import BaseModel


class PipelineRunItem(BaseModel):
    pipeline_name: str
    airflow_dag_id: str
    airflow_run_id: str
    status: str
    mlflow_run_id: str | None = None
    started_at: str | None = None
    ended_at: str | None = None
    duration_seconds: int | None = None

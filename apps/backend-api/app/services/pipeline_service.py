from app.repositories.pipeline_repository import PipelineRepository


class PipelineService:
    def __init__(self, pipeline_repo: PipelineRepository) -> None:
        self.pipeline_repo = pipeline_repo

    def list_runs(self, limit: int = 20) -> dict:
        items = self.pipeline_repo.list_runs(limit=limit)
        return {"items": items, "count": len(items)}

    def latest_status(self) -> str:
        return self.pipeline_repo.latest_status()

from sqlalchemy.orm import Session

from app.clients.model_server import ModelServerClient
from app.db.session import get_db
from app.repositories.drift_repository import DriftRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.model_version_repository import ModelVersionRepository
from app.repositories.pipeline_repository import PipelineRepository
from app.repositories.prediction_repository import PredictionRepository
from app.services.drift_service import DriftService
from app.services.model_registry_service import ModelRegistryService
from app.services.pipeline_service import PipelineService
from app.services.prediction_service import PredictionService


def get_prediction_service(db: Session) -> PredictionService:
    return PredictionService(
        prediction_repo=PredictionRepository(db),
        model_repo=ModelVersionRepository(db),
        model_server_client=ModelServerClient(),
    )


def get_model_registry_service(db: Session) -> ModelRegistryService:
    return ModelRegistryService(model_repo=ModelVersionRepository(db))


def get_drift_service(db: Session) -> DriftService:
    return DriftService(drift_repo=DriftRepository(db))


def get_pipeline_service(db: Session) -> PipelineService:
    return PipelineService(pipeline_repo=PipelineRepository(db))


def get_feedback_repo(db: Session) -> FeedbackRepository:
    return FeedbackRepository(db)


__all__ = [
    "get_db",
    "get_prediction_service",
    "get_model_registry_service",
    "get_drift_service",
    "get_pipeline_service",
    "get_feedback_repo",
]

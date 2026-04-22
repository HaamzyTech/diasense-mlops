from fastapi import APIRouter

from app.api.v1.endpoints import drift, feedback, health, model_info, ops, pipeline, predict, predictions

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(model_info.router)
api_router.include_router(predict.router)
api_router.include_router(predictions.router)
api_router.include_router(feedback.router)
api_router.include_router(drift.router)
api_router.include_router(pipeline.router)
api_router.include_router(ops.router)

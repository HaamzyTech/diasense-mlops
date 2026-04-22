from fastapi import APIRouter

router = APIRouter(prefix="/model")


@router.get("/info")
def get_model_info() -> dict:
    # TODO: Load active model info from model_versions table.
    return {
        "model_name": "diasense-diabetes-risk",
        "model_version": "1",
        "algorithm": "random_forest",
        "stage": "Production",
        "mlflow_run_id": "abc123",
        "metrics": {"f1": 0.78, "precision": 0.8, "recall": 0.76, "roc_auc": 0.84},
    }

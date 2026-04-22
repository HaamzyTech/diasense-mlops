from pathlib import Path

import json

import mlflow
import mlflow.pyfunc
import pandas as pd

from utils.io import ensure_dirs, read_params, save_json
from utils.modeling import top_factors
from utils.runtime import dvc_rev, git_commit_hash, mlflow_tracking_uri


class DiabetesRiskPyFunc(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        import joblib

        self.bundle = joblib.load(context.artifacts["model_bundle"])
        self.model = self.bundle["model"]

    def predict(self, context, model_input: pd.DataFrame):
        probabilities = self.model.predict_proba(model_input)[:, 1]
        predictions = self.model.predict(model_input)
        factors = top_factors(self.model)

        output = []
        for pred, prob in zip(predictions, probabilities):
            if prob < 0.33:
                band = "low"
            elif prob < 0.66:
                band = "moderate"
            else:
                band = "high"
            output.append(
                {
                    "predicted_label": bool(pred),
                    "risk_probability": round(float(prob), 4),
                    "risk_band": band,
                    "top_factors": factors,
                }
            )
        return output


def main() -> None:
    ensure_dirs()
    root = Path(__file__).resolve().parents[1]
    params = read_params(root / "params.yaml")

    mlflow.set_tracking_uri(mlflow_tracking_uri())
    mlflow.set_experiment("diasense-training")

    bundle_path = root / "artifacts" / "models" / "best_model.pkl"
    training_summary = json.loads((root / "artifacts" / "reports" / "training_summary.json").read_text(encoding="utf-8"))
    metrics = json.loads((root / "artifacts" / "reports" / "evaluation_metrics.json").read_text(encoding="utf-8"))

    with mlflow.start_run(run_name="diasense-register") as run:
        mlflow.log_params({
            "algorithm": params["model"]["algorithm"],
            "selected_model": training_summary.get("selected_model", "unknown"),
            "git_commit_hash": git_commit_hash(),
            "dvc_rev": dvc_rev(),
        })
        mlflow.log_metrics({k: float(v) for k, v in metrics.items()})
        mlflow.log_artifact(str(root / "artifacts" / "reports" / "classification_report.json"))
        mlflow.log_artifact(str(root / "artifacts" / "reports" / "confusion_matrix.json"))
        mlflow.log_artifact(str(root / "artifacts" / "reports" / "feature_importance.json"))
        mlflow.log_artifact(str(root / "params.yaml"))

        model_info = mlflow.pyfunc.log_model(
            artifact_path="model",
            python_model=DiabetesRiskPyFunc(),
            artifacts={"model_bundle": str(bundle_path)},
            registered_model_name=params["model"]["name"],
        )

        save_json(
            root / "artifacts" / "reports" / "register.json",
            {
                "run_id": run.info.run_id,
                "model_uri": model_info.model_uri,
                "registered_model_name": params["model"]["name"],
            },
        )


if __name__ == "__main__":
    main()

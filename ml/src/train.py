from pathlib import Path

import pandas as pd

from utils.constants import FEATURE_COLUMNS
from utils.io import ensure_dirs, read_params, save_json, save_model
from utils.modeling import candidate_models, compute_metrics, top_factors


def main() -> None:
    ensure_dirs()
    root = Path(__file__).resolve().parents[1]
    params = read_params(root / "params.yaml")
    random_state = int(params["train"]["random_state"])

    train_df = pd.read_csv(root / "data" / "features" / "train.csv")
    val_df = pd.read_csv(root / "data" / "features" / "val.csv")

    x_train, y_train = train_df[FEATURE_COLUMNS], train_df["outcome"]
    x_val, y_val = val_df[FEATURE_COLUMNS], val_df["outcome"]

    metrics_by_model: dict[str, dict] = {}
    trained_models: dict[str, object] = {}

    for name, model in candidate_models(random_state=random_state).items():
        model.fit(x_train, y_train)
        y_pred = model.predict(x_val)
        y_prob = model.predict_proba(x_val)[:, 1]
        model_metrics = compute_metrics(y_val.to_numpy(), y_pred, y_prob)
        model_metrics["top_factors"] = top_factors(model)
        metrics_by_model[name] = model_metrics
        trained_models[name] = model

    best_name = max(metrics_by_model.items(), key=lambda item: item[1]["f1"])[0]
    best_model = trained_models[best_name]

    bundle = {
        "model_name": best_name,
        "model": best_model,
        "feature_columns": FEATURE_COLUMNS,
        "top_factors": metrics_by_model[best_name]["top_factors"],
    }
    save_model(root / "artifacts" / "models" / "best_model.pkl", bundle)

    summary = {
        "selected_model": best_name,
        "metrics": metrics_by_model[best_name],
        "all_models": metrics_by_model,
        "row_counts": {"train": int(len(train_df)), "val": int(len(val_df))},
    }
    save_json(root / "artifacts" / "reports" / "training_summary.json", summary)


if __name__ == "__main__":
    main()

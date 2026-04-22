from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

from utils.constants import FEATURE_COLUMNS
from utils.io import ensure_dirs, load_model, save_json
from utils.modeling import compute_metrics, top_factors


def main() -> None:
    ensure_dirs()
    root = Path(__file__).resolve().parents[1]

    bundle = load_model(root / "artifacts" / "models" / "best_model.pkl")
    model = bundle["model"]

    test_df = pd.read_csv(root / "data" / "features" / "test.csv")
    x_test, y_test = test_df[FEATURE_COLUMNS], test_df["outcome"]

    y_pred = model.predict(x_test)
    y_prob = model.predict_proba(x_test)[:, 1]

    metrics = compute_metrics(y_test.to_numpy(), y_pred, y_prob)
    report = classification_report(y_test, y_pred, output_dict=True)
    conf = confusion_matrix(y_test, y_pred).tolist()

    save_json(root / "artifacts" / "reports" / "evaluation_metrics.json", metrics)
    save_json(root / "artifacts" / "reports" / "classification_report.json", report)
    save_json(root / "artifacts" / "reports" / "confusion_matrix.json", {"matrix": conf})
    save_json(root / "artifacts" / "reports" / "feature_importance.json", {"top_factors": top_factors(model)})


if __name__ == "__main__":
    main()

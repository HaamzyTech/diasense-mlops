from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from ml.src.utils.constants import FEATURE_COLUMNS
from ml.src.utils.io import ensure_dirs, save_json


def main() -> None:
    ensure_dirs()
    root = Path(__file__).resolve().parents[1]
    train_df = pd.read_csv(root / "data" / "features" / "train.csv")

    features = train_df[FEATURE_COLUMNS]
    baseline: dict[str, dict] = {}
    for col in FEATURE_COLUMNS:
        series = features[col].astype(float)
        counts, edges = np.histogram(series, bins=10)
        baseline[col] = {
            "mean": float(series.mean()),
            "variance": float(series.var()),
            "min": float(series.min()),
            "max": float(series.max()),
            "quantiles": {q: float(series.quantile(q)) for q in [0.1, 0.25, 0.5, 0.75, 0.9]},
            "histogram": {"bin_edges": edges.tolist(), "counts": counts.tolist()},
        }

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "row_count": int(len(features)),
        "feature_stats": baseline,
    }
    save_json(root / "artifacts" / "baselines" / "drift_baseline.json", payload)


if __name__ == "__main__":
    main()

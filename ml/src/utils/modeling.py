from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score

from ml.src.utils.constants import FEATURE_COLUMNS


def candidate_models(random_state: int) -> dict[str, Any]:
    return {
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=random_state),
        "random_forest": RandomForestClassifier(n_estimators=300, random_state=random_state),
        "extra_trees": ExtraTreesClassifier(n_estimators=300, random_state=random_state),
    }


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray) -> dict[str, float]:
    return {
        "f1": float(f1_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
    }


def top_factors(model: Any) -> list[dict[str, float | str]]:
    importances: np.ndarray
    if hasattr(model, "feature_importances_"):
        importances = np.asarray(model.feature_importances_)
    elif hasattr(model, "coef_"):
        coef = np.asarray(model.coef_)
        importances = np.abs(coef[0])
    else:
        importances = np.zeros(len(FEATURE_COLUMNS))

    order = np.argsort(importances)[::-1][:3]
    return [
        {"feature": FEATURE_COLUMNS[int(idx)], "importance": float(importances[int(idx)])}
        for idx in order
    ]


def to_dataframe_records(features: pd.DataFrame) -> list[dict[str, float]]:
    return features[FEATURE_COLUMNS].to_dict(orient="records")

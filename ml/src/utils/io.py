from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from config import ARTIFACTS_DIR, DATA_DIR


def ensure_dirs() -> None:
    (DATA_DIR / "raw").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "validated").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "processed").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "features").mkdir(parents=True, exist_ok=True)
    (ARTIFACTS_DIR / "reports").mkdir(parents=True, exist_ok=True)
    (ARTIFACTS_DIR / "models").mkdir(parents=True, exist_ok=True)
    (ARTIFACTS_DIR / "baselines").mkdir(parents=True, exist_ok=True)


def read_params(path: Path) -> dict[str, Any]:
    import yaml

    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def write_csv(path: Path, data: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, index=False)


def save_model(path: Path, model: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def load_model(path: Path) -> Any:
    return joblib.load(path)

from __future__ import annotations

import os
import subprocess


def git_commit_hash() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)
            .decode("utf-8")
            .strip()
        )
    except Exception:
        return "unknown"


def dvc_rev() -> str:
    try:
        return (
            subprocess.check_output(["dvc", "status", "-c"], stderr=subprocess.DEVNULL)
            .decode("utf-8")
            .strip()
            or "clean"
        )
    except Exception:
        return "unknown"


def mlflow_tracking_uri() -> str:
    return os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow-tracking:5000")

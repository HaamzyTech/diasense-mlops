from pathlib import Path

import pandas as pd

from utils.constants import EXPECTED_COLUMNS
from utils.io import ensure_dirs, save_json, write_csv


def validate_dataframe(df: pd.DataFrame) -> dict:
    report: dict = {
        "schema_ok": list(df.columns) == EXPECTED_COLUMNS,
        "expected_columns": EXPECTED_COLUMNS,
        "actual_columns": list(df.columns),
        "missing_values": df.isna().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "suspicious_ranges": {},
    }

    if not report["schema_ok"]:
        raise ValueError("Schema mismatch: expected exact columns and order")

    for column in EXPECTED_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    ranges = {
        "pregnancies": (0, 30),
        "glucose": (0, 300),
        "blood_pressure": (0, 200),
        "skin_thickness": (0, 100),
        "insulin": (0, 1000),
        "bmi": (0, 100),
        "diabetes_pedigree_function": (0, 10),
        "age": (1, 120),
        "outcome": (0, 1),
    }
    for column, (min_v, max_v) in ranges.items():
        mask = (df[column] < min_v) | (df[column] > max_v)
        report["suspicious_ranges"][column] = int(mask.sum())

    report["row_count"] = int(len(df))
    report["null_rows"] = int(df.isna().any(axis=1).sum())
    report["is_valid"] = report["schema_ok"] and report["null_rows"] == 0
    return report


def main() -> None:
    ensure_dirs()
    root = Path(__file__).resolve().parents[1]
    input_path = root / "data" / "raw" / "diabetes.csv"
    output_path = root / "data" / "validated" / "validated.csv"
    report_path = root / "artifacts" / "reports" / "validation_report.json"

    df = pd.read_csv(input_path)
    report = validate_dataframe(df)
    save_json(report_path, report)
    if not report["is_valid"]:
        raise ValueError("Validation failed; see validation_report.json")
    write_csv(output_path, df)


if __name__ == "__main__":
    main()

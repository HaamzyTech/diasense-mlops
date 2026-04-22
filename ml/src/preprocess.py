from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from ml.src.utils.constants import FEATURE_COLUMNS, IMPUTE_ZERO_AS_MISSING
from ml.src.utils.io import ensure_dirs, save_json, write_csv


def preprocess_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    processed = df.copy()
    for column in IMPUTE_ZERO_AS_MISSING:
        processed[column] = processed[column].replace(0, pd.NA)

    medians = {}
    for column in FEATURE_COLUMNS:
        processed[column] = pd.to_numeric(processed[column], errors="coerce")
        medians[column] = float(processed[column].median())
        processed[column] = processed[column].fillna(medians[column])

    processed["outcome"] = pd.to_numeric(processed["outcome"], errors="raise").astype(int)
    return processed, {"medians": medians}


def main() -> None:
    ensure_dirs()
    root = Path(__file__).resolve().parents[1]
    validated_path = root / "data" / "validated" / "validated.csv"
    raw_snapshot_path = root / "data" / "processed" / "raw_snapshot.csv"

    df = pd.read_csv(validated_path)
    write_csv(raw_snapshot_path, df)

    processed, artifact = preprocess_dataframe(df)
    write_csv(root / "data" / "processed" / "processed.csv", processed)

    train_df, temp_df = train_test_split(processed, test_size=0.3, stratify=processed["outcome"], random_state=42)
    val_df, test_df = train_test_split(temp_df, test_size=0.5, stratify=temp_df["outcome"], random_state=42)

    write_csv(root / "data" / "features" / "train.csv", train_df)
    write_csv(root / "data" / "features" / "val.csv", val_df)
    write_csv(root / "data" / "features" / "test.csv", test_df)
    save_json(root / "artifacts" / "reports" / "preprocessing_artifact.json", artifact)


if __name__ == "__main__":
    main()

import pandas as pd
import pytest

from ml.src.validate import validate_dataframe


@pytest.fixture
def valid_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "pregnancies": [1, 2],
            "glucose": [120, 150],
            "blood_pressure": [70, 80],
            "skin_thickness": [20, 25],
            "insulin": [80, 100],
            "bmi": [30.2, 31.8],
            "diabetes_pedigree_function": [0.2, 0.3],
            "age": [33, 44],
            "outcome": [0, 1],
        }
    )


def test_validate_ok(valid_df: pd.DataFrame) -> None:
    report = validate_dataframe(valid_df)
    assert report["schema_ok"] is True
    assert report["duplicate_rows"] == 0


def test_validate_schema_mismatch_raises(valid_df: pd.DataFrame) -> None:
    bad = valid_df.rename(columns={"age": "age_years"})
    with pytest.raises(ValueError, match="Schema mismatch"):
        validate_dataframe(bad)

import pandas as pd

from ml.src.preprocess import preprocess_dataframe


def test_preprocess_imputes_zero_impossible_values() -> None:
    df = pd.DataFrame(
        {
            "pregnancies": [1, 2],
            "glucose": [0, 120],
            "blood_pressure": [0, 70],
            "skin_thickness": [0, 20],
            "insulin": [0, 80],
            "bmi": [0, 30],
            "diabetes_pedigree_function": [0.2, 0.3],
            "age": [33, 44],
            "outcome": [0, 1],
        }
    )

    processed, artifact = preprocess_dataframe(df)
    assert processed.isna().sum().sum() == 0
    assert artifact["medians"]["glucose"] == 120.0

from pathlib import Path

import requests

from ml.src.utils.io import ensure_dirs, read_params


def main() -> None:
    ensure_dirs()
    root = Path(__file__).resolve().parents[1]
    params = read_params(root / "params.yaml")
    source_url = params["data"]["source_url"]
    output = root / "data" / "raw" / "diabetes.csv"

    response = requests.get(source_url, timeout=30)
    response.raise_for_status()
    output.write_text(response.text, encoding="utf-8")


if __name__ == "__main__":
    main()

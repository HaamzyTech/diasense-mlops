from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="diasense_monitoring_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["diasense", "monitoring"],
) as dag:
    drift_baseline = BashOperator(task_id="drift_baseline", bash_command="python ml/src/drift_baseline.py")

    drift_baseline

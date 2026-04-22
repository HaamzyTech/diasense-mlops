from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="diasense_training_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["diasense", "training"],
) as dag:
    ingest = BashOperator(task_id="ingest", bash_command="dvc repro ingest")
    validate = BashOperator(task_id="validate", bash_command="dvc repro validate")
    preprocess = BashOperator(task_id="preprocess", bash_command="dvc repro preprocess")
    train = BashOperator(task_id="train", bash_command="dvc repro train")
    evaluate = BashOperator(task_id="evaluate", bash_command="dvc repro evaluate")
    register = BashOperator(task_id="register", bash_command="dvc repro register")

    ingest >> validate >> preprocess >> train >> evaluate >> register

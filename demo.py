# ~/airflow/dags/say-hello.py

from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

# ① A DAG represents a workflow, a collection of tasks
with DAG(dag_id="demo", start_date=datetime(2023, 10, 1), schedule="@daily", catchup=False) as dag:

    # ② Tasks are represented as operators
    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task()
    def airflow():
        print("airflow")

    # ③ Set dependencies between tasks
    hello >> airflow()

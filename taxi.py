from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

# Spark 파일을 직접 실행하는 방법
# task 단위로 파일을 관리할 수 있다는 장점이 있음
# airflow web에서 spark connection 필요. Provider 설치해야됨.
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# Airflow 내에서 실행시키는 방법
# from airflow.providers.apache.spark.operators.spark_sql import SparkSqlOperator

with DAG(dag_id="taxi", start_date=datetime(2024, 8, 4, 0, 0, 0), schedule="@daily", catchup=False) as dag:
    # preprocess

    hello = BashOperator(task_id="hello", bash_command="echo hello")

    preprocess = SparkSubmitOperator(
        application="local:////opt/spark/work-dir/taxi.py",
        task_id="airflow-testing",
        conn_id="spark_default",
        deploy_mode="cluster",
        conf={
            'spark.master': 'k8s://https://127.0.0.1:59833',
            'spark.kubernetes.container.image': 'apache:1.2',
            'spark.kubernetes.authenticate.driver.serviceAccountName': 'spark'
        }
    )

    hello >> preprocess
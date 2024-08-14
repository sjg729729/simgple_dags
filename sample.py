from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator

# 기본 DAG 인자 설정
default_args = {
    'depends_on_past': False,
    'email': ['abcd@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG 정의
with DAG(
    'spark_kubernetes_example',
    default_args=default_args,
    description='A simple DAG to run Spark job on Kubernetes',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example']
) as dag:

    # SparkKubernetesOperator 정의
    run_spark_job = SparkKubernetesOperator(
        task_id='run_spark_job',
        application_file='/opt/airflow/dags/repo/outside_test.yaml',  # YAML 파일의 절대 경로
        namespace='spark-jobs',
        kubernetes_conn_id='myk8s',  # Kubernetes Connection ID
        # api_group='sparkoperator.k8s.io',
        # api_version='v1beta2',
        do_xcom_push=True,
        dag=dag
    )
    
    run_spark_job

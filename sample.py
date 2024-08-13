from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

# 기본 DAG 매개변수 설정
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

# DAG 정의
with DAG(
    dag_id='example_kubernetes_pod_operator',
    default_args=default_args,
    description='An example DAG using KubernetesPodOperator',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # KubernetesPodOperator를 사용하여 Pod 작업 정의
    k8s_pod_task = KubernetesPodOperator(
        task_id='run_python_script',
        name='python-script-job',
        namespace='default',  # Pod이 실행될 네임스페이스
        image='python:3.9',   # 사용할 Docker 이미지
        cmds=['python', '-c'],  # 실행할 명령
        arguments=[
            'print("Hello from Kubernetes Pod!")'
        ],
        is_delete_operator_pod=True,  # 작업 완료 후 Pod을 삭제할지 여부
        get_logs=True,  # Pod 로그를 Airflow 로그로 가져올지 여부
        dag=dag
    )

    # DAG의 기본 작업 흐름 정의
    k8s_pod_task

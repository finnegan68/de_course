from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
import subprocess

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'email': ['ilya.linetski@gmail.com'],  # Replace with your email
    'email_on_failure': False,
    'email_on_retry': False,
}

# Define DAG
with DAG(
    dag_id='process_iris',
    default_args=default_args,
    description='Run dbt model, train ML model, and send email notification',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['iris', 'ml', 'dbt'],
) as dag:

    # Step 1: Run dbt model
    run_dbt = BashOperator(
        task_id='run_dbt_model',
        bash_command="""
        cd /opt/airflow/dbt/homework && \
        dbt run --select mart.iris_processed
        """,
        env={
            'DBT_PROFILES_DIR': '/opt/airflow/dbt'
        }
    )


    def train_model():
        subprocess.run(['python', '/opt/airflow/dags/python_scripts/train_model.py'], check=True)

    train_model_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
    )


    notify_email = EmailOperator(
        task_id='send_email',
        to='your_email@example.com',  # Replace with your email
        subject='Airflow DAG process_iris Succeeded',
        html_content='The DAG <b>process_iris</b> completed successfully.',
    )


    #run_dbt >> train_model_task >> notify_email
    run_dbt
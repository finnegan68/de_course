from airflow import DAG
from datetime import timedelta
from datetime import datetime
import os
from dbt_operator import DbtOperator
from airflow.utils.dates import days_ago
from python_scripts.iris_ml_processor import process_iris_data


ANALYTICS_DB = os.getenv('ANALYTICS_DB', 'analytics')
PROJECT_DIR = os.getenv('AIRFLOW_HOME')+"/dags/dbt/models"
PROFILE = 'homework'

# Environment variables to pass to dbt
env_vars = {
    'ANALYTICS_DB': ANALYTICS_DB,
    'DBT_PROFILE': PROFILE
}

# Example of variables to pass to dbt
dbt_vars = {
    'is_test': False,
    'data_date': '{{ ds }}',  # Uses Airflow's ds (execution date) macro
}

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
    dbt_run = DbtOperator(
        task_id='dbt_run',
        profile=PROFILE,
        project_dir=PROJECT_DIR,
        # Example of selecting specific models
        models=['mart'],  # This selects all staging model
        env_vars=env_vars,
        vars=dbt_vars,
    )


    train_model_task = PythonOperator(
        task_id='train_model',
        python_callable=process_iris_data,
        provide_context=True,
    )


    notify_email = EmailOperator(
        task_id='send_email',
        to='your_email@example.com',  # Replace with your email
        subject='Airflow DAG process_iris Succeeded',
        html_content='The DAG <b>process_iris</b> completed successfully.',
    )


    #run_dbt >> train_model_task >> notify_email
    run_dbt
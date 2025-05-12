from airflow import DAG
from dbt_operator import DbtOperator
from airflow.utils.dates import days_ago
import os
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from python_scripts.train_model import process_iris_data



ANALYTICS_DB = os.getenv('ANALYTICS_DB', 'analytics')
PROJECT_DIR = os.getenv('AIRFLOW_HOME')+"/dags/dbt/homework"
PROFILE = 'my_dbt_project'


env_vars = {
    'ANALYTICS_DB': ANALYTICS_DB,
    'DBT_PROFILE': PROFILE
}


dbt_vars = {
    'is_test': False,
    'data_date': '{{ ds }}', 
}


default_args = {
    'owner': 'airflow',
    'email': ['ilya.linetski@gmail.com'],  # Replace with your email
    'email_on_failure': False,
    'email_on_retry': False,
}


dag = DAG(dag_id='process_iris',
        default_args=default_args,
        description='Run dbt model, train ML model, and send email notification',
        schedule_interval=None,
        start_date=days_ago(1),
        catchup=False,
        tags=['iris', 'ml', 'dbt']) 

    
run_dbt = DbtOperator(
        task_id='dbt_run',
        dag=dag,
        command='run',
        profile=PROFILE,
        project_dir=PROJECT_DIR,
        models=['models/mart','models/staging'],  
        env_vars=env_vars,
        vars=dbt_vars,
    )


train_model_task = PythonOperator(
        task_id='train_model',
        dag=dag,
        python_callable=process_iris_data,
        provide_context=True,
    )


notify_email = EmailOperator(
        task_id='send_email',
        dag=dag,
        to=default_args['email'],
        subject='Airflow DAG process_iris Succeeded',
        html_content='The DAG <b>process_iris</b> completed successfully.',
    )


run_dbt >> train_model_task >> notify_email

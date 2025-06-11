from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta

from utiles.functions import SimpleAgent
import os

agent = SimpleAgent( path_directory = r'/opt/airflow/data',
                    source_model='OpenAI')

with DAG(
    dag_id='text_summary_dag',
    schedule=timedelta(days=1),
    start_date=datetime(2025, 1, 1),
) as dag:
    pass

    task_check_file = PythonOperator(
        task_id = 'task_check_file',
        python_callable=agent.check_file,
    )

    task_read_file = PythonOperator(
        task_id = 'task_read_file',
        python_callable=agent.read_file,
    )

    task_llm = PythonOperator(
        task_id = 'task_llm',
        python_callable=agent.chat_completion,
    )

    task_mail = PythonOperator(
        task_id = 'task_mail',
        python_callable=agent.send_email_smtp,
    )

    task_check_file >> task_read_file >> task_llm >> task_mail

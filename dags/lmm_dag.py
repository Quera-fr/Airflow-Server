from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator

import ollama
import chromadb
from chromadb.config import Settings


# Test the ollama model by sending a simple message
# and pushing the response to XCom

def test_ollama(ti):
    response = ollama.chat(model="llama2", messages=[{"role": "user", "content": "Bonjour"}])
    ti.xcom_push(key="ollama_response", value=response["message"]["content"])
    return response["message"]["content"]


# Save the ollama response into a Chroma collection

def save_to_chroma(ti):
    message = ti.xcom_pull(task_ids="test_ollama", key="ollama_response")
    client = chromadb.PersistentClient(path="/opt/airflow/chroma")
    collection = client.get_or_create_collection("ollama_requests")
    collection.add(documents=[message], ids=["1"])
    return "saved"


with DAG(
    dag_id="lmm_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ollama", "chroma"],
    default_args={"owner": "airflow"},
) as dag:
    test = PythonOperator(task_id="test_ollama", python_callable=test_ollama)

    store = PythonOperator(task_id="store_in_chroma", python_callable=save_to_chroma)

    notify = EmailOperator(
        task_id="send_confirmation",
        to="example@example.com",
        subject="Ollama Test Succeeded",
        html_content="<p>The Ollama model responded successfully.</p>",
    )

    test >> store >> notify

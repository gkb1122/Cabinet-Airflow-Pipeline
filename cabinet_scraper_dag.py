import sys

sys.path.insert(0, "/opt/airflow")

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from app.scraper import scrape_policies
from app.database import save_policies
from app.pdf_downloader import download_all_pdfs
from app.pdf_processor import process_pdfs


def scrape_task():
    policies = scrape_policies()

    print(f"Policies Found: {len(policies)}")

    save_policies(policies)


with DAG(
    dag_id="cabinet_scraper_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    scrape = PythonOperator(
        task_id="scrape_policies",
        python_callable=scrape_task,
    )

    download = PythonOperator(
        task_id="download_pdfs",
        python_callable=download_all_pdfs,
    )

    process = PythonOperator(
        task_id="process_pdfs",
        python_callable=process_pdfs,
    )

    scrape >> download >> process
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from tasks.scraper_task import scrape_amazon
from tasks.spark_milvus_task import process_and_insert_data

with DAG(
    "amazon_pipeline",
    default_args={"retries": 3},
    schedule_interval="@daily",
    start_date=datetime(2023, 11, 1),
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=scrape_amazon,
        op_kwargs={"amazon_url": "https://www.amazon.com/s?k=laptops"},
    )

    process_and_load_task = PythonOperator(
        task_id="process_and_load_data",
        python_callable=process_and_insert_data,
    )

    extract_task >> process_and_load_task

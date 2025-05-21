#!/usr/bin/python
"""
AirflowDag module
"""
import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from ingestion.fetch_weather_data import fetch_weather
from processing.transform_weather_data import   transform_weather_data
from storage.load_to_postgres import load_weather_data

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

def etl():
    cities = ["Nairobi", "Machakos", "Kisumu"]
    for city in cities:
        raw_data = fetch_weather(city)
        logging.info(f"Fetched raw daya: {raw_data}")
        
        clean_data = transform_weather_data(raw_data)
        logging.info(f"Transformed data: {clean_data}")
        load_weather_data(clean_data)

with DAG (
    dag_id='weather_etl_pipeline',
    default_args=default_args,
    start_date=datetime(2025,5,20),
    schedule='*/5 * * * *', # Every 5 minutes
    catchup=False
) as dag:

    run_etl = PythonOperator(
        task_id='run_weather_etl',
        python_callable=etl
    )

    run_etl

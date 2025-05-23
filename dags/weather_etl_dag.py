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

# Task 1 - Extract data 

def extract_data(**context):
    cities = ["Nairobi", "Machakos", "Kisumu"]
    all_raw_data = []
    for city in cities:
        raw_data = fetch_weather(city)
        logging.info(f"Fetched raw data: {raw_data}")
        all_raw_data.append(raw_data)

    # Push data to XCom
    context['ti'].xcom_push(key='raw_weather_data', value=all_raw_data)

# Task 2: Transform data 
def transform_data(**context):
        
        raw_data = context['ti'].xcom_pull(task_ids='extract_task', key='raw_weather_data')
        clean_data = transform_weather_data(raw_data)
        logging.info(f"Transformed data: {clean_data}")

        # Push cleaned data to XCom
        context['ti'].xcom_push(key='clean_weather_data', value=clean_data)
    

# Task 3: Load data 

def load_data(**context):
     clean_data = context['ti'].xcom_pull(task_ids='transform_task', key='clean_weather_data')
     load_weather_data(clean_data)
     logging.info("loaded data to Postgresql")

# Define the DAG and TASKS
with DAG (
    dag_id='weather_etl_pipeline',
    default_args=default_args,
    start_date=datetime(2025,5,23),
    schedule='*/5 * * * *', # Every 5 minutes
    catchup=False
) as dag:

    task_1 = PythonOperator(
        task_id='extract_task',
        python_callable=extract_data,
        provide_context=True
    )

    task_2 = PythonOperator(
         task_id='transform_task',
         python_callable=transform_data,
         provide_context=True
    )

    task_3 = PythonOperator(
         task_id='load_task',
         python_callable=load_data,
         provide_context=True
    )

    task_1 >> task_2 >> task_3

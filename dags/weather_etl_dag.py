#!/usr/bin/python
"""
AirflowDag module
Makes use of the taskAPI to facilate data transfer 
between tasks
"""
import logging
from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
from datetime import datetime, timedelta
from ingestion.fetch_weather_data import fetch_weather
from processing.transform_weather_data import   transform_weather_data
from storage.load_to_postgres import load_weather_data

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

# Get Cities
@task
def get_city_list():
     default_cities =["Nairobi","Machakos","Mombasa","London","Kisumu"]
     cities_str = Variable.get("weather_cities", default_var=",".join(default_cities))
     cities = [city.strip() for city in cities_str.split(",") if city.strip()]
     logging.info(f"[Config] Cities to fecth: {cities}")
     return cities
# Task 1 - Extract data 
@task
def extract_data(cities):
    all_raw_data = []
    for city in cities:
        raw_data = fetch_weather(city)
        logging.info(f"[Extract] fetched raw data for {city}: {raw_data}")
        all_raw_data.append(raw_data)
    return all_raw_data

# Task 2: Transform data
@task
def transform_data(raw_data):
    clean_data = transform_weather_data(raw_data)
    logging.info(f"[Transform] Cleaned weather data: {clean_data}")
    return clean_data

# Task 3: Load data 
@task
def load_data(clean_data):
     load_weather_data(clean_data)
     logging.info("[Load] Weather data loaded to Postgresql db")

# Define the DAG and TASKS
with DAG (
    dag_id='weather_etl_pipeline',
    default_args=default_args,
    start_date=datetime(2025,5,29),
    schedule='*/5 * * * *', # Every 5 minutes
    catchup=False
) as dag:
    cities = get_city_list()
    raw = extract_data(cities)
    clean = transform_data(raw)
    load_data(clean)

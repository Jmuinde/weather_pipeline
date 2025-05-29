# Weather ETL Pipeline (END-to-END Data Engineering Project Built on Opne Source Tools)

## Project Overview
The project focuses on building a fully modular, end-to-end open-sourse data piple to:
- Exctract real-time weather data from the open weather API
- Clean and transform the data 
- Load the into a PostgreSQL databse 
- Orchestrate tasks with Apache Airflow 
- Deploy infrastructure using Docker compose 
- Monitor & log pipelien perfoamce 

## Project Structure 
weather_pipeline/
├── dags/ (Airflow DAGs)
├── ingestion/ (Fetch data)
├── processing/ (Transform data)
├── storage/ (Load data to DB)
├── config/ (Environment settings)
├── docker/ (Docker Compose files)
├── logs/ (Auto-generated logs)
├── requirements.txt
├── README.md
└── .env (API keys, database URL)

## Tech stack 
- Python 3.9
- PostgreSQL 13
- Apache Airflow 2.7
- Docker Compose 
- OpenWeatherMap API
- APache kafka
- Grafana (for monitoring)
- Great expectation (for data quality checks)

## How to Run Locally 
1. clone the repo
2. Set up your '.env' file to cinlude:
    - 'OPENWEATHER_API_KEY'
    - 'DATABASE_URL'
3. Launch project using Docker:
    ```bash
    cd docker
    docker-compose up
    ```
    


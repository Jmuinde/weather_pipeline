# main.py
from processing.transform_weather_data import transform_weather_data
from ingestion.fetch_weather_data import fetch_weather

if __name__ == "__main__":
    data = transform_weather_data(fetch_weather("Nairobi"))
    print(data)

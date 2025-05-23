# main.py
import time
from processing.transform_weather_data import transform_weather_data
from ingestion.fetch_weather_data import fetch_weather

if __name__ == "__main__":
	cities = ["Nairobi", "Mombasa", "Kisumu"]
	
	# Ingest and transfom data in the cities after every 5 minutes
	while True:
		for city in cities:
			raw = fetch_weather(city)
			clean = transform_weather_data(raw)
			
			print(clean)
		print("sleeping for a minute...\n")
		time.sleep(60) # sleep for 60 seconds

#!/usr/bin/python3
"""
Transform weather data module.
"""
from ingestion.fetch_weather_data import fetch_weather
def transform_weather_data(raw_data):
	""" Transfrom the fetched data from the weeather API 
		which is in json format to a stractured formart for database insertion"""
	transformed = {
		'city': raw_data['city']['name'],
		'timestamp': raw_data['list'][0]['dt'],
		'temperature':raw_data['list'][0]['main']['temp'],
		'humidity':raw_data['list'][0]['main']['humidity'],
		'pressure':raw_data['list'][0]['main']['pressure'],
		'weather': raw_data['list'][0]['weather'][0]['description']
	}
	return transformed

if __name__ == "__main__":
	
	cleaned_data = transform_weather_data(fetch_weather(city))
	# print(cleaned_data)


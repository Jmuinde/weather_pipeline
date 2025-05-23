#!/usr/bin/python3
"""
Data extraction module
"""

import requests
import sys
import os
import logging
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

def fetch_weather(city_name):
    """
    Function to fetch weather data for a given city using the openweather API.
    """
    params ={
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }
    respone = requests.get(BASE_URL, params=params)
    respone.raise_for_status()
    return respone.json()


if __name__ == "__main__":
    city = "Nairobi"
    data = fetch_weather(city)
    print(data)




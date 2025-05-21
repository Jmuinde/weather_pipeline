"""
Storage module
"""

import psycopg2
import os
import logging
from dotenv import load_dotenv
import logging
# Load enviroment variables 
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")


def load_weather_data(data):
	logging.info("Starting DB Load...")
	logging.info(f"DATABASE_URL = {DB_URL}")

	required_keys = ['city', 'timestamp', 'temperature', 'humidity', 'pressure', 'weather']
	missing_keys = [key for key in required_keys if key not in data]

	if missing_keys:
		logging.error(f"Missing required keys in data: {missing_keys}")
		return  # Abort DB insert

	try:
		conn = psycopg2.connect(DB_URL)
		cur = conn.cursor()

		# Create table if not exists
		create_table_query = """
		CREATE TABLE IF NOT EXISTS weather_data (
			id SERIAL PRIMARY KEY,
			city VARCHAR(100),
			timestamp BIGINT,
			temperature FLOAT,
			humidity INT,
			pressure INT,
			weather VARCHAR(255)
		);
		"""
		cur.execute(create_table_query)

		# Insert the data
		insert_query = """
		INSERT INTO weather_data (city, timestamp, temperature, humidity, pressure, weather)
		VALUES (%s, %s, %s, %s, %s, %s);
		"""
		cur.execute(insert_query, (
			data['city'],
			data['timestamp'],
			data['temperature'],
			data['humidity'],
			data['pressure'],
			data['weather']
		))

		conn.commit()
		logging.info("Data inserted successfully!")

	except Exception as e:
		logging.error(f"Error inserting data: {e}")

	finally:
		if 'cur' in locals(): cur.close()
		if 'conn' in locals(): conn.close()


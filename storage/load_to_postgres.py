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

	if not data:
		logging.warning("No data received in the DB")
		return

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
		for row in data:
			missing_keys = [key for key in ['city', 'timestamp', 'temperature', 'humidity', 'pressure', 'weather'] if key not in row]
			if missing_keys:
				logging.warning(f"Skipping row with missing keys: {missing_keys}")
				continue

			cur.execute(insert_query, (
				row['city'],
				row['timestamp'],
				row['temperature'],
				row['humidity'],
				row['pressure'],
				row['weather']
			))

		conn.commit()
		logging.info("All data inserted successfully!")

	except Exception as e:
		logging.error(f"Error inserting data: {e}")

	finally:
		if 'cur' in locals(): cur.close()
		if 'conn' in locals(): conn.close()
		
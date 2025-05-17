"""
Storage module
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load enviroment variables 
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def load_weather_data(data):
	""" loads the transformed data in the Postgresql database."""
	try:
		# Establish connection
		conn = psycopg2.connect(DB_URL)
		cur = conn.cursor()

		# Create table if it doesn't exist
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
		
		# Commit and close
		conn.commit()
		cur.close()
		conn.close()
		
		print("Data inserted successfully!")
	except Exception as e:
		print(f"Error inserting data: {e}")

if __name__ == "__main__":

	# Example usage
	sample_data = {
		'city': 'Nairobi',
		'timestamp':1714300500,
		'temperature': 25.5,
		'humidity': 80,
		'pressure': 1012,
		'weather': 'light rain'
	}
	
	load_weather_data(sample_data)

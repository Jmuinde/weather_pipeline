"""
Storage module
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load enviroment variables 
DB_URL = os.getenv("DATABASE_URL")



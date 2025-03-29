import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """Creates and returns a database connection."""
    try:
        # Get the database URL from the .env file
        database_url = os.getenv("DATABASE_URL")
        
        # Connect to the database
        conn = psycopg2.connect(database_url)
        
        print("Database connection established successfully!")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    


import psycopg2
from src.database.scripts.config.config import config
import sys

# Create connection object

def connect():
    conn = None
    try:
        params = config()
        print('Connecting to postgreSQL database ...')
        conn = psycopg2.connect(**params)
        # Create a cursor
        crsr = conn.cursor()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn, crsr

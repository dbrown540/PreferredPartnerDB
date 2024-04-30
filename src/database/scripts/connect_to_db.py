"""
Module: connect_to_db

This module provides a function to connect to a PostgreSQL database using the psycopg2 library.
It includes a function to establish a connection to the database and retrieve a connection object.

Functions:
    - connect: Establishes a connection to the PostgreSQL database using configuration parameters.

Dependencies:
    - psycopg2: A PostgreSQL adapter for the Python programming language.
    - config: A function from the `config` module within the `src.database.scripts.config` package,
              which provides configuration parameters for connecting to the PostgreSQL database.

Example:
    To connect to the PostgreSQL database, use the `connect` function as follows:

    >>> import psycopg2
    >>> from src.database.connection import connect

    >>> # Establish a connection to the PostgreSQL database
    >>> connection = connect()

    >>> # Use the connection object to execute SQL queries or perform database operations

Author:
    Danny Brown

Date:
    April 29, 2024

Version:
    0.1-dev
"""

# pylint: disable=E0401
import psycopg2
from src.database.scripts.config.config import config

def connect():
    """
    Connect to a PostgreSQL database.
    
    Returns:
        psycopg2.extensions.connection: A connection to the PostgreSQL database.
    """
    conn = None
    try:
        params = config()
        print('Connecting to PostgreSQL database ...')
        conn = psycopg2.connect(**params)
    except (psycopg2.Error, psycopg2.DatabaseError) as error:
        print(error)
        conn = None

    return conn

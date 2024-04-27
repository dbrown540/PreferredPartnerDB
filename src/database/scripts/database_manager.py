from connect_to_db import connect
from typing import Union, Optional, Tuple, List
import logging
import time
import psycopg2


class DatabaseManager:
    def __init__(self):
        # Establish connection with database
        self.conn = self.check_database_connection()
        
    def check_database_connection(self):
        """
        Check the database connection and re-establish if necessary.
        
        This method checks the database connection and re-establishes it if the connection is closed or doesn't exist. 
        It retries a maximum of 3 times with an exponential backoff delay starting from 1 second.
    
        Returns:
            tuple: A tuple containing the database connection and cursor.
    
        Raises:
            RuntimeError: If maximum retries are exceeded and unable to establish a database connection.
        """
        MAX_RETRIES = 3
        INITIAL_DELAY = 1
        retries = 0
        delay = INITIAL_DELAY
        
        
        
        while retries < MAX_RETRIES:
            try:
                # If the database connection is closed or doesn't exist
                if self.conn is None or self.conn.closed != 0:
                    # Re-establish the connection
                    self.conn = connect()
                    logging.info("Database connection re-established.")

                else:
                    # Log that an existing connection is being used
                    logging.info("Using existing database connection.")
                        
                return self.conn
            
            except TimeoutError:
                logging.error(f"Timeout while trying to establish the database connection. Attempting to reconnect (Attempt: {(retries + 1)} / {MAX_RETRIES})")
                
            except ConnectionError:
                logging.error(f"Connection error occurred while trying to establish the database connection. Attempting to reconnect (Attempt: {(retries + 1)} / {MAX_RETRIES})")
                
            except psycopg2.OperationalError as e:
                logging.error(f"Operational error occurred: {e}. Attempting to reconnect (Attempt: {(retries + 1)} / {MAX_RETRIES})")
            
            # Exponential backoff before retrying
            time.sleep(delay)
            delay *= 2
            retries += 1
        
        logging.critical("Maximum retries exceeded. Unable to establish database connection.")
        raise RuntimeError("Maximum retries exceeded. Unable to establish database connection.")
    
    def execute_query(self, query: str, params: Optional[Union[Tuple, None]] = None, fetch: Optional[str] = None) -> Union[str, List, None]:
        """
        Execute a SQL query with optional parameters and fetch the result based on specified amount.
        
        Args:
            query (str): The SQL query to be executed.
            params (Optional[Union[tuple, None]]): Optional parameters to be passed with the query. Defaults to None.
            fetch (Optional[str]): Specify whether to fetch 'ALL' results or 'ONE' result. Defaults to None.
        
        Returns:
            Union[str, list, None]: The fetched result based on the fetch parameter.
        
        Raises:
            psycopg2.Error: If there is an error specific to psycopg2.
            Exception: If there is a general error during query execution.
        
        Example:
            # Selecting values from the database

            # Create a DatabaseManager instance
            >>> db_manager = DatabaseManager()

            # Execute a SELECT query with parameters
            >>> fetch = 'ALL'
            >>> query = "SELECT * FROM table WHERE column = %s"
            >>> params = ("value",)  # Parameters must be tuples
            >>> db_manager.execute_query(fetch, query, params)

            # Execute a DELETE query without parameters and without fetching results
            >>> delete_query = "DELETE FROM table WHERE column = %s"
            >>> params = ("value",)
            >>> db_manager.execute_query(delete_query, params)
        """
        try:
            # Establish a database connection and create a cursor
            with self.conn, self.conn.cursor() as cursor:
                # Ensure the database connection is valid
                self.check_database_connection()  
                # Execute the query with optional parameters
                cursor.execute(query, params)  
                # Log the executed query and parameters
                logging.info(f"Executed query: {query} with parameters: {params}")
                # Fetch the result depending on specified amount
                if fetch == 'ALL':
                    result = cursor.fetchall()
                elif fetch == 'ONE':
                    result = cursor.fetchone()
                else:
                    result = None

                return result
            
        except psycopg2.Error as pg_error:
            # Log any errors specific to psycopg2
            logging.critical(f"Error executing query: {query} with parameters: {params}. psycopg2 Error: {pg_error}")
            raise
        except Exception as error:
            # Log any other general errors
            logging.critical(f"Error executing query: {query} with parameters: {params}. General Error: {error}")
            raise
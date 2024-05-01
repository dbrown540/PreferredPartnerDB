"""
This module contains imports for handling database connections and logging.

Imports include:
- Standard library: logging, time, typing, psycopg2
- Local application: connect from the database module

These imports are used for setting up database connections, performing database operations,
and logging events related to database interactions.
"""
import logging
import time
from typing import Union, Optional, Tuple, List, Dict
import psycopg2
from .connect_to_db import connect

# Configure the logging system
logging.basicConfig(filename="log.log", level=logging.INFO)

class DatabaseManager:
    """
    Database Manager provides functionality for managing database connections, 
    executing SQL queries, and handling errors related to database operations.

    This class encapsulates methods for establishing and maintaining a database connection,
    executing SQL queries with optional parameters, and handling various database-related errors.
    It integrates with the psycopg2 library to interact with PostgreSQL databases.

    Attributes:
        conn: A psycopg2 connection object representing the database connection.

    Methods:
        __init__(): Initializes a DatabaseManager instance and establishes a database connection.
        check_database_connection(): Checks the database connection 
            and re-establishes it if necessary.
        execute_query(query, params=None, fetch=None): Executes a SQL query with optional parameters
            and fetches the result based on the specified fetch mode.
    """
    def __init__(self):
        # Initialize connction to None
        self.conn = None
        # Establish connection with database
        self.conn = self.check_database_connection()

    def check_database_connection(self):
        """
        Check the database connection and re-establish if necessary.
        
        This method checks the database connection and re-establishes it if the 
        connection is closed or doesn't exist. 
        It retries a maximum of 3 times with an exponential backoff delay starting from 1 second.
    
        Returns:
            tuple: A tuple containing the database connection and cursor.
    
        Raises:
            RuntimeError: If maximum retries are exceeded and unable 
            to establish a database connection.
        """
        max_retries = 3
        initial_delay = 1
        retries = 0
        delay = initial_delay

        while retries < max_retries:
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
                error_message = (
                    f"Timeout while trying to establish the database connection. "
                    f"Attempting to reconnect (Attempt: {retries + 1} / {max_retries})"
                )

                logging.error(error_message)

            except ConnectionError:
                error_message = (
                    f"Connection error occurred while trying to establish the database connection. "
                    f"Attempting to reconnect (Attempt: {(retries + 1)} / {max_retries})"
                )
                logging.error(error_message)

            except psycopg2.OperationalError as e:
                error_message = (
                    f"Operational error occurred: {e}. Attempting to reconnect "
                    f"(Attempt: {(retries + 1)} / {max_retries})"
                )
                logging.error(error_message)

            # Exponential backoff before retrying
            time.sleep(delay)
            delay *= 2
            retries += 1

        logging.critical("Maximum retries exceeded. Unable to establish database connection.")
        raise RuntimeError("Maximum retries exceeded. Unable to establish database connection.")

    def execute_query(self, query: str, params: Optional[Union[Tuple, None]] = None,
                      fetch: Optional[str] = None) -> Union[str, List, None]:
        """
        Execute a SQL query with optional parameters and fetch the result based on specified amount.
        
        Args:
            query (str): The SQL query to be executed.
            params (Optional[Union[tuple, None]]): 
                Optional parameters to be passed with the query. Defaults to None.
            fetch (Optional[str]): 
                Specify whether to fetch 'ALL' results or 'ONE' result. Defaults to None.
        
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
            >>> params = ("value",)  # Parameter(s) must be a tuple
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
                logging_message = (
                    f"Executed query: {query} with parameters: {params}"
                )
                logging.info(logging_message)
                # Fetch the result depending on specified amount
                if fetch == 'ALL':
                    result = cursor.fetchall()
                elif fetch == 'ONE':
                    result = cursor.fetchone()
                else:
                    result = None

                # Commit the transaction
                self.conn.commit()

                return result

        except psycopg2.Error as pg_error:
            # Log any errors specific to psycopg2
            error_message = (
                f"Error executing query: {query} with parameters: "
                f"{params}. psycopg2 Error: {pg_error}"
            )
            logging.critical(error_message)
            # Roll back the transaction
            self.conn.rollback()
            raise
        except Exception as error:
            # Log any other general errors
            error_message = (
                f"Error executing query: {query} with parameters: "
                f"{params}. General Error: {error}"
            )
            logging.critical(error_message)
            # Roll back the transaction
            self.conn.rollback()
            raise

    def update_work_experience(self, work_experience: Dict[str, str], user_id: int):
        """
        Insert job experiences into the database for a given user.
        
        Args:
            work_experience (dict):
                A dictionary containing company names as 
                keys and job titles as values.
            user_id (int):
                The unique identifier of the user.
        
        Returns:
            None
        
        Prints:
            "Updated work experience into database"
        """
        # Insert job experiences into the database
        for company, job_titles in work_experience.items():
            # If job_titles is a list, insert each job title separately
            if isinstance(job_titles, list):
                for job_title in job_titles:
                    query = (
                        "INSERT INTO work_experience "
                        "(user_id, company, title) "
                        "VALUES "
                        "(%s, %s, %s)"
                    )
                    params = (user_id, company, job_title)

                    self.execute_query(query=query, params=params)
            else:
                # If job_titles is a string, insert it as a single record
                query = (
                    "INSERT INTO work_experience "
                    "(user_id, company, title) "
                    "VALUES "
                    "(%s, %s, %s)"
                )
                params = (user_id, company, job_title)

                self.execute_query(query=query, params=params)
        info_message = (
            f"Successfully updated work experience "
            f"database for user {user_id}"
        )
        logging.info(info_message)

    def send_names_to_db(self, users_name: str, profile_url: str) -> None:
        """
        Update the database with the given user's name and profile URL.

        Args:
            users_name (str): The name of the user to be updated.
            profile_url (str): The profile URL of the user.

        Returns:
            None
        """
        # Define query arguments
        query = "UPDATE users SET users_name = '%s' WHERE profile_url = '%s'"
        params = (users_name, profile_url)

        # Update the datbase
        self.execute_query(query=query, params=params)

    def update_location_in_db(self, users_location: str, profile_url: str) -> None:
        """
        Update the location of a user in the database.

        Args:
            users_location (str): The new location of the user.
            profile_url (str): The profile URL of the user.

        Returns:
            None
        """

        # Define query and params arguments
        query = (
        "UPDATE users SET location_of_user = '%s' "
                "WHERE profile_url = '%s';"
        )
        params = (users_location, profile_url)

        # Update the database to include the location of the user (locate using the profile url)
        self.execute_query(query=query, params=params)

    def update_profile_urls_from_scout(self, profile_urls: List[str]) -> None:
        """
        Updates the profile URLs in the database from the provided list of URLs.
        
        Args:
            profile_urls (List[str]): A list of profile URLs to update in the database.
        
        Returns:
            None
        
        Raises:
            IntegrityError: If a profile URL already exists in the database, a warning is logged and the function moves on to the next URL.
        """

        # Execute a query that updates the database with profile urls

        for profile_url in profile_urls:
            # Set query arguments
            query = (
                "INSERT INTO users (profile_url) "
                "VALUES (%s)"
            )
            params = (profile_url,)

            try:
                # Insert the profile URL
                self.execute_query(query=query, params=params)
                logging.info(
                    "Successfully added user link to the database.\n"
                    "Link contents = %s", profile_url
                )
            except psycopg2.IntegrityError as e:
                # Check if it's a unique constraint violation
                if 'duplicate key value' in str(e):
                    logging.warning(
                        "Link (%s) already in database", profile_url
                    )
                else:
                    # Handle other integrity errors
                    logging.error("Integrity error: %s", e)
                # Continue to the next iteration of the loop
                continue

"""
Module: config

This module provides functions to establish a connection to a PostgreSQL database 
using configuration parameters read from a specified INI file.

Functions:
    - config(filename="database.ini", section="postgresql"): 
        Read database configuration from the specified file and section.
        Args:
            filename (str): The path to the configuration file.
            section (str): The section name in the configuration file.
        Returns:
            dict: A dictionary containing the database configuration parameters.

Example:
    To establish a connection to a PostgreSQL database, you can use the `config` function
    to read the configuration parameters from a file named 'database.ini' located in the 
    'src/database/scripts/config' directory, under the 'postgresql' section:
    
    ```
    >>> from config import config

    >>> params = config()
    >>> conn = psycopg2.connect(**params)
    ```

Author:
    Danny Brown

Date:
    April 29, 2024

Version:
    0.1-dev
"""

from configparser import ConfigParser, NoSectionError
from os.path import join

def config(filename="database.ini", section="postgresql"):
    """
    Read database configuration from the specified file and section.

    Args:
        filename (str): The path to the configuration file.
        section (str): The section name in the configuration file.

    Returns:
        dict: A dictionary containing the database configuration parameters.
    """
    # Construct the full path to the configuration file
    file_path = join("src", "database", "scripts", "config", filename)

    # Create a parser object
    parser = ConfigParser()

    # Read the configuration file
    parser.read(file_path)

    # Initialize an empty dictionary to store configuration parameters
    db = {}

    # Check if the specified section exists in the configuration file
    if parser.has_section(section):
        # Get all parameters from the specified section
        params = parser.items(section)

        # Populate the dictionary with parameter key-value pairs
        for key, value in params:
            db[key] = value
    else:
        # If the specified section is not found, raise an exception
        raise NoSectionError(
            f"Section '{section}' not found in '{filename}' file."
        )

    # Print the resulting dictionary (for debugging purposes)
    print(f"This is the 'db' dictionary: {db}")

    # Return the dictionary containing database configuration
    return db

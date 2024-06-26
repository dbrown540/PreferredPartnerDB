"""
Module: bot_credentials_manager

The BotCredentialsManager module provides functionality for managing bot credentials,
including generating email headers, passwords, and updating credentials in a database.

Classes:
    BotCredentialsManager: 
        Manages bot credentials, including email headers, passwords, and database updates.

Attributes:
    None

Methods:
    __init__(self): 
        Initializes a BotCredentialsManager instance.
    _create_email_headers(self, file_path): 
        Reads a text file containing names and creates email headers.
    _generate_passwords(self, num_of_passwords, length): 
        Generates strong passwords for bots.
    _create_bot_contact_list(self, first_names, last_names, email_headers, passwords_list): 
        Creates a list of bot contacts by zipping together provided information.
    update_bot_credentials_in_database(self): 
        Updates bot credentials in the database.

Usage:

    >>> from src.bots.bot_credentials_manager import BotCredentialsManager

    >>> bot_credentials_manager = BotCredentialsManager()
    >>> bot_credentials_manager.bot_credentials_wrapper()

Author:
    Danny Brown

Date:
    May 1, 2024

Version:
    0.1-dev
""" 

import string
import secrets
import logging
from typing import List, Tuple

#pylint: disable=relative-beyond-top-level
from ....database.scripts.database_manager import DatabaseManager, BotCredentialsDatabaseManager

logging.basicConfig(filename="log.log", level=logging.INFO)

class BotCredentialsManager:
    def __init__(self):
        self.credentials_db_manager = BotCredentialsDatabaseManager()

    @staticmethod
    def create_email_headers(file_path="scrapers/src/bots/linkedin/config/names.txt") -> List[str]:
        """
        Reads a text file containing names and creates email headers.
    
        Args:
            file_path (str): Path to the text file containing names.
            
        Returns:
            List[str]: A list of email headers generated from the names.
        """
        email_headers = []
        first_names = []
        last_names = []
        with open(file=file_path, mode="r", encoding="utf-8") as names_file:
            for line in names_file:
                first_name, last_name = line.strip().split(" ")
                email_headers.append(f"{first_name.lower()}_{last_name.lower()}")
                first_names.append(first_name)
                last_names.append(last_name)

        logging.info(
            "Successfully generated first_names, last_names, and email_headers for the bots"
            )

        return first_names, last_names, email_headers

    @staticmethod
    def generate_password(
        length=12, 
        include_special_chars=True) -> List[str]:
        """
        Generates strong passwords for the bots when they go to create emails and 
        LinkedIn profiles.

        Args:
            num_of_passwords (int): Number of passwords that are to be created
            length (12): Default 12. Length of password
            include_special_chars (bool):
                Default True. True if you want to include special characters

        Returns:
            passwords_list (List[str]): List of all generated passwords
        """
        alphabet = string.ascii_letters + string.digits
        if include_special_chars:
            alphabet += string.punctuation
        
        password = ''.join(secrets.choice(alphabet) for _ in range(length))

        logging.info("Successfully generated passwords for the bots")
        return password
    
    @staticmethod
    def create_bot_contact_list_tuples(
            first_names: List[str], last_names: List[str],
            email_headers: List[str], passwords_list: List[str]
            ) -> List[Tuple[str, str, str, str]]:
        """
        Creates a list of bot contacts by zipping together the provided 
        lists of first names, last names, email headers, and passwords.
    
        Args:
            first_names (List[str]): List of first names for the bot contacts.
            last_names (List[str]): List of last names for the bot contacts.
            email_headers (List[str]): List of email headers for the bot contacts.
            passwords_list (List[str]): List of passwords for the bot contacts.
    
        Returns:
            List[Tuple[str, str, str, str]]: A list of tuples containing the zipped 
            information of first name, last name, email header, and password for 
            each bot contact.
        """
        return zip(first_names, last_names, email_headers, passwords_list)
    
    def bot_credentials_wrapper(self):
        """
        Updates bot credentials in the database.
        
        This function updates the bot credentials in the database by creating email headers, generating passwords,
        creating a bot contact list, and then updating the credentials in the database using the database manager.
        """

        new_bots = set()

        # Create email headers
        first_names, last_names, email_headers = self.create_email_headers()

        for item in zip(first_names, last_names, email_headers):
            first_name = item[0]
            last_name = item[1]
            email_header = item[2]
            # Check if the first and last name combination already exists in the database
            bot_already_exists = self.credentials_db_manager.first_and_last_exists_in_db(first=first_name, last=last_name)
            if bot_already_exists:
                logging.info("%s %s (bot) already exists. Skipping to next bot.", first_name, last_name)
                pass
            else:
                # Continue creating the bot account
                password = self.generate_password()
                new_bots.add((first_name, last_name, email_header, password))

        

        # Update bot credentials in the database
        self.credentials_db_manager.update_bot_credentials(new_bots)
        
print("Completed")

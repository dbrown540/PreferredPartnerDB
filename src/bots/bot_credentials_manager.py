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
from ..database.scripts.database_manager import DatabaseManager

logging.basicConfig(filename="log.log", level=logging.INFO)

class BotCredentialsManager:
    def __init__(self):
        self.database_manager = DatabaseManager()

    @staticmethod
    def create_email_headers(file_path="src//bots//config//names.txt") -> List[str]:
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
    def generate_passwords(
        num_of_passwords: int, length=12, 
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
        
        passwords_list = []        
        for _ in range(num_of_passwords):    
            password = ''.join(secrets.choice(alphabet) for _ in range(length))
            passwords_list.append(password)

        logging.info("Successfully generated passwords for the bots")
        return passwords_list
    
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
        if not self.database_manager.bots_exist_in_database():

            # Create email headers
            first_names, last_names, email_headers = self.create_email_headers()

            # Generate passwords
            num_of_passwords = len(first_names)  # Assuming equal number of names and passwords
            passwords_list = self.generate_passwords(num_of_passwords)

            # Create bot contact list
            contact_list = self.create_bot_contact_list_tuples(
                first_names, last_names, email_headers, passwords_list
            )

            # Update bot credentials in the database
            self.database_manager.update_bot_credentials(contact_list)
        
        else:
            logging.info("Bot data already exists in database. Will not create new credentials.")


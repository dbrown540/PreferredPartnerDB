import random
import string
import secrets
import csv
from typing import List

#pylint: disable=relative-beyond-top-level
from ..database.scripts.database_manager import DatabaseManager

class BotCredentialsManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.database_manager = DatabaseManager()

    def create_email_headers(self, file_path="src//bots//config//names.txt") -> List[str]:
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

        return first_names, last_names, email_headers


    def generate_one_strong_password(self, num_of_passwords: int, length=12) -> List[str]:
        """
        Generate a strong password of a specified length.
    
        Args:
            length (int): The length of the password to be generated.
    
        Returns:
            str: A strong password of the specified length.
        """
        passwords_list = []
        for _ in range(num_of_passwords):    
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for _ in range(length))
            passwords_list.append(password)
        return passwords_list
    
    def create_bot_contact_list(self, first_names, last_names, email_headers, password):
        zipped_contact_list = zip(first_names, last_names, email_headers, password)


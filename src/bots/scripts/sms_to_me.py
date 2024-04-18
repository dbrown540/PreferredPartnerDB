from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from ...database.scripts.connect_to_db import connect
from .bot_credentials_manager import BotCredentialsManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import logging
import time
import random
import re

class SMSToMe:
    def __init__(self):
        self.driver_path = 'chromedriver-win64/chromedriver.exe'
        self.driver = self.initialize_webdriver()
        self.wait = WebDriverWait(self.driver, 10)
        self.conn, self.crsr = connect()

    def check_if_there_are_bots_without_phone_numbers(self) -> bool:
        """Check if there are bots without phone numbers.
        
        Returns:
            bool: True if all bots have a phone number, False if there are bots without a phone number.
        """
        self.crsr.execute("SELECT COUNT(*) FROM bots WHERE phone IS NULL;")
        number_of_bots_without_phone_number = self.crsr.fetchone()[0]

        if number_of_bots_without_phone_number == 0:  # Meaning all bots have a phone number
            bots_have_phone_numbers = True
            
        else:
            bots_have_phone_numbers = False  # Meaning there are bots that don't have a phone number
        
        return bots_have_phone_numbers


    def initialize_webdriver(self):
        """Initializes chrome webdriver object"""
        try:
            options = Options()
            service = Service(self.driver_path)
            driver = WebDriver(service=service, options=options)
            logging.info(f"\nService path: {self.driver_path}\nOptions: {options}")
            return driver
        except Exception as e:
            logging.critical(f'Failed to initialize webdriver: {e}')
            raise

    def navigate_to_sms_to_me(self):
        """Navigates to the SMS to Me website for the USA country.
        
        Raises:
            Exception: If unable to access the smstome website.
        """
        try:
            self.driver.get("https://smstome.com/country/usa")

        except Exception as e:
            print(f"Could not access smstome.\nError:\n{e}")

    def find_phone_numbers(self) -> list:
        """Find phone numbers on the webpage and return a list of them.
        
            Returns:
                list: A list of phone numbers found on the webpage.
        
            Raises:
                NoSuchElementException: If 'a' tags are not found on the webpage.
                Exception: If an error occurs while looking for phone numbers.
        """
        phone_numbers_list = []
        try:
            links = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
            for link in links:
                potential_phone_number = link.text
                phone_number = re.search(r'\+\d+', potential_phone_number)

                if phone_number:
                    matched_number = phone_number.group()
                    phone_numbers_list.append(matched_number[2:])

        except NoSuchElementException:
            print("Could not find a tags")
        
        except Exception:
            print("An error occurred while looking for phone numbers")

        return phone_numbers_list
    
    def remove_database_numbers(self, phone_numbers_list):
        """Remove database numbers from the given list of phone numbers.
        
            This function removes phone numbers that already exist in the database table 'bots'.
            
            Args:
                phone_numbers_list (list): A list of phone numbers to filter.
                
            Returns:
                list: A filtered list of phone numbers that do not exist in the database.
        """
        filtered_phone_numbers = []

        for number in phone_numbers_list:
            try:
                self.crsr.execute(f"SELECT COUNT(*) FROM bots WHERE phone = '{number}'")  # Count number of bots with a specific phone number (Ideally should be 0 or 1)
                number_of_bots_with_specific_number = self.crsr.fetchone()[0]  # Fetch the result

                if number_of_bots_with_specific_number == 0:  # If the phone number is unique, add it to the filtered phone numbers list
                    filtered_phone_numbers.append(number)

                else:
                    print(f"{number} already exists in the datbase")  # Otherwise, say it already exists in the database

            except Exception as e:
                print(f"There was an issue connecting to the database.\nError:\n{e}")

        return filtered_phone_numbers



    def refresh_phone_number_list(self):

        # Only execute if there are bots without phone numbers in the database

        all_bots_have_phone_numbers = self.check_if_there_are_bots_without_phone_numbers()

        if not all_bots_have_phone_numbers:

            # Initialize the chrome webdriver
        
            self.initialize_webdriver()
        
            # Navigate to the sms to me website

            self.navigate_to_sms_to_me()

            # Find the phone numbers listed on the main page
        
            phone_numbers_list = self.find_phone_numbers()

            # Filter the phone numbers to make sure the numbers don't already exist in the database

            filtered_phone_numbers = self.remove_database_numbers(phone_numbers_list)

            # Put phone number in the database so that it is accessible to all programs

            for filtered_number in filtered_phone_numbers:
                filtered_number = str(filtered_number)
                filtered_number_tuple = (filtered_number,)
                self.crsr.execute("INSERT INTO phone_numbers (phone_number) VALUES (%s)", filtered_number_tuple)
                self.conn.commit()
import re
from typing import Union, Tuple, Optional, Dict, Set, List
import logging
import time

import psycopg2
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, WebDriverException,
    StaleElementReferenceException, ElementNotInteractableException)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from ....database.scripts.database_manager import DatabaseManager
from ...webdriver.webdriver_manager import WebDriverManager
from .linkedinbot import BaseManager

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

class PhoneNumberScraper(BaseManager):
    def __init__(self):
        super().__init__(WebDriverManager(), DatabaseManager())

    def get_to_sms_to_me_website(self):
        """
        Opens the SMS to Me website in the browser.
        
        This function navigates to the local file path where the SMS to Me website is located and waits for 10 seconds for the page to load.
        """
        self.driver.get("file://C://Users//Doug Brown//Desktop//Dannys Stuff//Job//PreferredPartnerDB//testing//smstome.html")
        time.sleep(10)

    def locate_container_divs(self):
        """Locates and returns a list of container div elements within a section element."""
        container_divs = self.driver.find_elements(
            By.XPATH, "//section[@class='container']/div[@class='row']"
        )

        return container_divs
    
    def locate_individual_phone_number_divs(self, container_divs: List[WebElement]):
        """
        Locates individual phone number divs within the given container divs.
        
        Args:
            self: The object instance.
            container_divs (List[WebElement]): A list of WebElements representing container divs.
        
        Returns:
            List[WebElement]: A list of WebElements representing individual phone number divs found within the container divs.
        """
        indiviual_phone_number_divs = []
        for container_div in container_divs:
            individual_divs = container_div.find_elements(
                By.XPATH, "div"
            )
            for ind_div in individual_divs:
                indiviual_phone_number_divs.append(ind_div)

        return indiviual_phone_number_divs
    
    def locate_a_tag_text(self, indiviual_phone_number_divs: List[WebElement]):
        """
        Locates and retrieves the text from <a> tags within a list of WebElement phone number divs.
    
        Args:
            self: The object instance.
            indiviual_phone_number_divs (List[WebElement]): A list of WebElement phone number divs.
    
        Returns:
            List[str]: A list of unparsed phone numbers extracted from the <a> tags within the provided WebElement phone number divs.
        """
        unparsed_phone_numbers = []
        for indiviual_phone_number_div in indiviual_phone_number_divs:
            a_tag = indiviual_phone_number_div.find_element(
                By.TAG_NAME, "a"
            )
            unparsed_phone_number = a_tag.text
            unparsed_phone_numbers.append(unparsed_phone_number)

        return unparsed_phone_numbers
                
    def parse_phone_number(self, unparsed_phone_numbers):
        """
        Parses phone numbers by removing the country code if present.
        
        Args:
            unparsed_phone_numbers (list): A list of unparsed phone numbers.
        
        Returns:
            list: A list of parsed phone numbers with country code removed.
        """
        parsed_phone_numbers = []
        for phone_number in unparsed_phone_numbers:
            if "+" in phone_number:
                # Parse the number
                phone_number = phone_number[2:]
                parsed_phone_numbers.append(phone_number)

        return parsed_phone_numbers

    def wrapper(self):
        """
        Wrapper function that retrieves phone numbers from a website.
        
        This function performs the following steps:
        1. Navigates to the SMS to Me website.
        2. Locates container divs on the webpage.
        3. Prints the number of container divs found.
        4. Locates individual phone number divs within the container divs.
        5. Retrieves the text from the <a> tags within the individual phone number divs.
        6. Parses the phone numbers from the retrieved text.
        7. Prints the parsed phone numbers.
        
        Returns:
            None
        """
        self.get_to_sms_to_me_website()
        container_divs = self.locate_container_divs()
        print(len(container_divs))
        indiviual_phone_number_divs = self.locate_individual_phone_number_divs(container_divs=container_divs)
        unparsed_phone_numbers = self.locate_a_tag_text(indiviual_phone_number_divs=indiviual_phone_number_divs)
        parsed_phone_numbers = self.parse_phone_number(unparsed_phone_numbers=unparsed_phone_numbers)
        print(parsed_phone_numbers)
        self.database_manager.update_phone_numbers(parsed_phone_numbers)
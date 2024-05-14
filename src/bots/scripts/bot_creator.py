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

from src.database.scripts.database_manager import DatabaseManager
from ..webdriver_manager import WebDriverManager
from .linkedinbot import BaseManager

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

class PhoneNumberScraper(BaseManager):
    def __init__(self):
        super().__init__(WebDriverManager(), DatabaseManager())

    def get_to_sms_to_me_website(self):
        self.driver.get("file://C://Users//Doug Brown//Desktop//Dannys Stuff//Job//PreferredPartnerDB//testing//smstome.html")
        time.sleep(10)


    def wrapper(self):
        self.get_to_sms_to_me_website()
        self.scrape_phone_numbers()

    def get_to_sms_to_me_website(self):
        self.webdriver_manager("https://smstome.com")
    
    def scrape_phone_numbers(self):
    
        elements = WebDriverManager.find_elements_by_tag_name('a')

        phone_numbers = []

        for elements in elements:
            href = elements.get_attribute('href')
            phone = re.finall(r'tel:\+?\d+', href)
            if phone:
                phone_numbers.extend(phone)

    
    print(scrape_phone_numbers)

      

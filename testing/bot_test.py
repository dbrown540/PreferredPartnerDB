from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from src.database.scripts.connect_to_db import connect
from src.database.scripts.database_manager import DatabaseManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import logging
import time
import random
import re

class LinkedInBot:
    def __init__(self):
        self.driver_path = 'chromedriver-win64/chromedriver.exe'
        # Initialize the WebDriver with the random user agent
        self.driver = self.initialize_webdriver()
        self.wait = WebDriverWait(self.driver, 10)
        # Create a database manager object
        self.database_manager = DatabaseManager()

    def initialize_webdriver(self):
        """Initializes Chrome WebDriver object"""
        try:
            options = Options()
            options.add_argument('--start-maximized')
            service = Service(self.driver_path)
            driver = WebDriver(service=service, options=options)
            logging.info(f"\nService path: {self.driver_path}\nOptions: {options}")
            return driver
        
        except Exception as e:
            logging.critical(f'Failed to initialize WebDriver: {e}')
            raise

    @staticmethod
    def access_linkedn(driver: WebDriver):
        driver.get("https://google.com")

    @staticmethod
    def access_feddb(driver:WebDriver):
        driver.get("https://feddb.net")



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

class ProxyManager:
    def __init__(self):
        self.driver_path = 'chromedriver-win64/chromedriver.exe'
        # self.driver = self.initialize_webdriver()
        # self.wait = WebDriverWait(self.driver, 10)
        self.conn, self.crsr = connect()

    def initialize_webdriver(self):
        """Initializes chrome webdriver object"""
        try:
            options = Options()
            # Add your custom Chrome options here
            options.add_argument('--headless')  # Run Chrome in headless mode
            options.add_argument('--no-sandbox')  # Required for headless mode on Linux
            service = Service(self.driver_path)
            driver = WebDriver(service=service, options=options)
            logging.info(f"\nService path: {self.driver_path}\nOptions: {options}")
            return driver
        except Exception as e:
            logging.critical(f'Failed to initialize webdriver: {e}')
            raise

    def load_proxies(self):
        with open("src/bots/config/proxies.txt", "r") as proxyfile:
            file_contents = proxyfile.read()
            print(file_contents)

    def check_proxy(self, proxy):
        pass


    def execute(self):
        # Access the text file list
        self.load_proxies()

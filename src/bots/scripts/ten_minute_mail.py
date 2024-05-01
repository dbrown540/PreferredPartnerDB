from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from ...database.scripts.connect_to_db import connect
from ....utils.config.bot_credentials_manager import BotCredentialsManager
from .sms_to_me import SMSToMe
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
import logging
import time
import random
import re

class BurnerEmailManager:
    def __init__(self):
        self.driver_path = 'chromedriver-win64/chromedriver.exe'
        self.driver = self.initialize_webdriver()
        self.conn, self.crsr = connect()
        self.wait = WebDriverWait(self.driver, 30)



    def initialize_webdriver(self):
        """Initializes chrome webdriver object"""
        try:
            options = ChromeOptions()
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36")
            options.add_argument("--incognito")
            options.add_argument("--maximized")
            service = Service(self.driver_path)
            driver = WebDriver(service=service, options=options)
            driver.maximize_window()
            logging.info(f"\nService path: {self.driver_path}\nOptions: {options}")
            return driver
        except Exception as e:
            logging.critical(f'Failed to initialize webdriver: {e}')
            raise

    def access_10_minute_mail(self):
        try:
            self.driver.get("https://temp-mail.org/en/")

        except Exception as e:
            print(e)

    def scrape_email(self):
        try:
            # Look for the copy icon
            copy_icon = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/form/div[2]/button')))
            copy_icon.click()
            print("Email is copied")

        except NoSuchElementException as e:
            print("Could not find copy button")

    def check_inbox(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mail_message")))

        except NoSuchElementException:
            print("Element not found")

        except Exception as e:
            print(e)

    def execute(self):

        # Access 10minutemail

        self.access_10_minute_mail()

        # Scrape the email address

        time.sleep(5)

        self.scrape_email()

        # Check inbox for message elements

        #self.check_inbox()


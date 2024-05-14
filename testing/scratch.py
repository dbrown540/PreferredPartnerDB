# module.py

import re
import logging
import time

import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementNotInteractableException
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

from src.database.scripts.database_manager import DatabaseManager
from bots.webdriver.webdriver_manager import WebDriverManager
from src.bots.scripts.linkedinbot import BaseManager

class PhoneNumberScraper(BaseManager):
    
    def __init__(
            self, webdriver_manager: WebDriverManager,
            database_manager: DatabaseManager):
        super().__init__(webdriver_manager, database_manager)

    def access_website(self):
        self.driver.get("file://C://Users//Doug Brown//Desktop//Dannys Stuff//Job//PreferredPartnerDB//testing//smstome.html")

    def find_class_element(self, xpath):
        element = self.driver.find_element(
            By.XPATH, xpath
        )
        return element

class Wrapper(BaseManager):
   
    def __init__(self):
        super().__init__(WebDriverManager(), DatabaseManager())

        self.phone_number_object = PhoneNumberScraper(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager
        )

    def execute(self):
        self.phone_number_object.access_website()
        element = self.phone_number_object.find_class_element("/html/body/div[2]/main/div[6]/div/div/div[2]/div/div[1]/div/h3/a")
        self.webdriver_manager.humanize_click(element)

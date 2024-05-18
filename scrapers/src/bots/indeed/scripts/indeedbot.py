import logging
import random
import time
from typing import Union, Tuple, Optional, Set, List
import re
from datetime import datetime

import psycopg2
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, WebDriverException,
    StaleElementReferenceException, ElementNotInteractableException)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from ....database.scripts.database_manager import DatabaseManager
from ...webdriver.webdriver_manager import WebDriverManager
from ...linkedin.scripts.linkedinbot import BaseManager

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

class SalaryFinder(BaseManager):
    def __init__(self) -> None:
        super().__init__(WebDriverManager(), DatabaseManager())

    def access_indeed_salaries(self):
        self.webdriver_manager.driver.get("https://www.indeed.com/career/salaries")

    def locate_job_title_input(self):
        job_title_input = self.webdriver_manager.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='What']"))
        )
        return job_title_input
    
    def fetch_job_title(self):
        pass

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

class NetWorthCalculator(BaseManager):
    def __init__(self, webdriver_manager: WebDriverManager, database_manager: DatabaseManager) -> None:
        super().__init__(webdriver_manager, database_manager)

    def access_calculator(self):
        self.webdriver_manager.driver.get("https://dqydj.com/net-worth-by-age-calculator/")

    def wrapper(self, user_id):
        # Get the age from the database
        work_periods = self.database_manager.get_work_periods()
        print(work_periods)
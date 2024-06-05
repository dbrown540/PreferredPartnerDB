import logging
import random
import time
from typing import Union, Tuple, Optional, Set, List
import re
from datetime import datetime
import os

import psycopg2
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, WebDriverException,
    StaleElementReferenceException, ElementNotInteractableException,
    InvalidArgumentException, ElementClickInterceptedException)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from geopy.geocoders import Nominatim

from .....database.scripts.database_manager import DatabaseManager, DukeDatabaseManager
from ....webdriver.webdriver_manager import WebDriverManager
from ....linkedin.utils.location_formatter.location_formatter import LocationFormatter
from ....linkedin.scripts.linkedinbot import BaseManager

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

class SignInManager(BaseManager):
    def __init__(self, webdriver_manager: WebDriverManager, database_manager: DukeDatabaseManager) -> None:
        super().__init__(webdriver_manager, database_manager)

    def access_duke_alumni_login(self):
        self.driver.get("https://alumni.duke.edu/")

    def click_alumni_network_button(self):
        register_or_log_in_button = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "alum-directory"))
        )
        register_or_log_in_button.click()
        time.sleep(5)

    def open_one_link(self):
        one_link_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "expand-onelink"))
        )

        one_link_button.click()

    def send_username(self):
        username_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "gigya_userid"))
        )

        username_input.send_keys("mdkoepke")
    
    def send_password(self):
        password_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "gigya_password"))
        )

        password_input.send_keys("Koreanspa2015!")

    def click_log_in_button(self):
        button = self.driver.find_element(
            By.ID, "onelink-login"
        )

        button.click()

    def send_creds(self):
        self.open_one_link()
        time.sleep(3)
        self.send_username()
        self.send_password()

class Searcher(BaseManager):
    def __init__(self, webdriver_manager: WebDriverManager, database_manager: DukeDatabaseManager) -> None:
        super().__init__(webdriver_manager, database_manager)

    def click_professional(self):
        professional_div = self.wait.until(
            EC.presence_of_element_located((By.ID, "PROFESSIONAL"))
        )

        professional_div.click()

    def type_industry(self, industry: str):
        industry_input = self.driver.find_element(
            By.XPATH, "//input[@aria-label='Industry']"
        )

        industry_input.clear()
        industry_input.click()
        industry_input.send_keys(industry)
        time.sleep(5)
        industry_input.send_keys(Keys.ENTER)

    def type_current_employer(self, current_employer: str):
        current_employer_input = self.driver.find_element(
            By.XPATH, "//input[@aria-label='Current Employer']"
        )

        current_employer_input.clear()
        current_employer_input.send_keys(current_employer)
        current_employer_input.send_keys(Keys.ENTER)

    def type_current_job_title(self, current_job_title_list: List[str]):
        current_job_title_div = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Current Job Title']"))
        )

        for job_title in current_job_title_list:
            current_job_title_div.clear()
            current_job_title_div.send_keys(job_title)
            time.sleep(5)
            current_job_title_div.send_keys(Keys.ENTER)
            time.sleep(3)

    def click_search(self):
        try:
            # Wait until the element is visible and clickable
            search_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.facet-footer .filter a'))
            )

            # Scroll the element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", search_button)

            # Click using JavaScript
            self.driver.execute_script("arguments[0].click();", search_button)

            logging.info("Search button clicked successfully.")

        except (ElementClickInterceptedException, TimeoutException, StaleElementReferenceException) as e:
            logging.error(f"Error clicking search button: {e}")
            # Optionally, you can implement a retry mechanism here

    def professional_search_wrapper(self, industry, current_employer, current_job_title):
        self.click_professional()
        time.sleep(1)
        self.type_industry(industry=industry)
        time.sleep(1)
        self.type_current_employer(current_employer=current_employer)
        time.sleep(1)
        self.type_current_job_title(current_job_title_list=current_job_title)
        time.sleep(1)

class SearchResultScraper(BaseManager):
    def __init__(self, webdriver_manager: WebDriverManager, database_manager: DukeDatabaseManager) -> None:
        super().__init__(webdriver_manager, database_manager)

    def scrape_profile_urls(self) -> List[WebElement]:
        profile_urls = set()
        try:
            a_tags: List[WebElement] = self.wait.until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
            )
            for a_tag in a_tags:
                href = a_tag.get_attribute("href")
                if href and "https://alumni.duke.edu/people/" in href:
                    profile_urls.add(href)

        except NoSuchElementException:
            logging.info("No results for this search query.")

        return list(profile_urls)
    
    def show_more_button_exists(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        try:
            show_more_button = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-default"))
            )
            if show_more_button:
                return True
        except TimeoutException:
            logging.info("No more profiles to load.")
        return False

    
    def click_show_more(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        try:
            show_more_button = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-default"))
            )
            show_more_button.click()
            return True
        except TimeoutException:
            logging.info("No more profiles to load.")
            return False

        
        
    def scrape_main_page(self) -> List[str]:
        all_profile_urls = set()
        while True:  # Change to an infinite loop
            profile_urls = self.scrape_profile_urls()
            all_profile_urls.update(profile_urls)
            print(f"Collected {len(profile_urls)} URLs, total so far: {len(all_profile_urls)}")
            if not self.show_more_button_exists():
                break  # Exit the loop if either condition is met
            self.click_show_more()
            time.sleep(random.uniform(25, 45))
        # One last scrape to get the remaining URLs after the last click
        time.sleep(4)
        profile_urls = self.scrape_profile_urls()
        all_profile_urls.update(profile_urls)
        print(f"Final collection: {len(all_profile_urls)} URLs.")
        return list(all_profile_urls)
    
class ProfileScraper(BaseManager):
    def __init__(self, webdriver_manager: WebDriverManager, database_manager: DukeDatabaseManager) -> None:
        super().__init__(webdriver_manager, database_manager)

    def access_profile(self, profile_url: str):
        self.driver.get(profile_url)

    def locate_emails(self):
        try:
            div_containing_email_h3 = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h3[text()='EMAIL']/.."))
            )
            email_element = div_containing_email_h3.find_element(By.XPATH, "div[contains(text(), '@')]")
            email = email_element.get_attribute('textContent')
            print("Emails: ", email)
            return email
        except NoSuchElementException as e:
            print("No emails found for this person")
            return ''
        except TimeoutException:
            print("No emails found for this person")
            return ''

    def locate_phone_numbers(self):
        try:
            div_containing_phone_h3 = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h3[text()='PHONE']/.."))
            )
            phone_elements = div_containing_phone_h3.find_elements(By.XPATH, "div")
            
            # Regular expression pattern to match sequences of digits with optional separators,
            # and optionally prefixed with country code or other characters
            digit_pattern = r'(?:\+\d{1,3}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?){1,4}\d{1,4}'
            
            # List to store matched strings containing digits
            digit_strings = []
            
            for phone_element in phone_elements:
                text = phone_element.text
                matched_digits = re.findall(digit_pattern, text)
                digit_strings.extend(matched_digits)
            
            return digit_strings[0]
        except NoSuchElementException as e:
            return ''
        
        except TimeoutException:
            return ''

    def locate_linkedin_url(self):
        try:
            a_tags = self.wait.until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
            )
            for a_tag in a_tags:
                href = a_tag.get_attribute("href")
                if "linkedin" in href:
                    return href
        except:
            return None
        
    def locate_name(self):
        try:
            h1_tags = self.wait.until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "h1"))
            )
            full_name_string = h1_tags[1].text
            name = full_name_string.split(',')[0]
            print(name)
            return name
        
        except:
            print("Couldn't find name for this profile")


class DukeBot(BaseManager):
    dukeDatabaseManager = DukeDatabaseManager()

    def __init__(self, webdriver_manager: Optional[WebDriverManager] = None, database_manager: DukeDatabaseManager = None) -> None:
        if webdriver_manager is None:
            webdriver_manager = WebDriverManager()  # Replace with actual initialization
        if database_manager is None:
            database_manager = DukeDatabaseManager()  # Replace with actual initialization

        super().__init__(webdriver_manager, database_manager)

        self.sign_in_manager = SignInManager(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager,
        )
        self.searcher = Searcher(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager,
        )
        self.search_results_scraper = SearchResultScraper(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager,
        )
        self.profile_scraper = ProfileScraper(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager,
        )

    def run_bot(self):
        alumni_urls_list = []
        email_list = []
        phone_list = []
        linkedin_url_list = []
        names_list = []

        self.sign_in_manager.access_duke_alumni_login()
        self.sign_in_manager.click_alumni_network_button()
        self.sign_in_manager.send_creds()
        self.sign_in_manager.click_log_in_button()
        time.sleep(5)

        self.searcher.professional_search_wrapper("Information Technology", "", ["Chief Executive Officer", "CEO"])
        if_correct = input("Press enter if the query is correct")
        if if_correct:
            pass
        self.searcher.click_search()
        time.sleep(6)

        profile_urls = self.search_results_scraper.scrape_main_page()

        time.sleep(10)
        
        for url in profile_urls:
            self.profile_scraper.access_profile(url)
            time.sleep(1)
            email = self.profile_scraper.locate_emails()
            time.sleep(1)
            phone = self.profile_scraper.locate_phone_numbers()
            time.sleep(1)
            linkedin_url = self.profile_scraper.locate_linkedin_url()
            time.sleep(1)
            name = self.profile_scraper.locate_name()

            alumni_urls_list.append(url)
            email_list.append(email)
            phone_list.append(phone)
            linkedin_url_list.append(linkedin_url)
            names_list.append(name)

            time.sleep(random.uniform(25, 45))

        zipped_list = zip(alumni_urls_list, email_list, phone_list, linkedin_url_list, names_list)

        self.dukeDatabaseManager.send_duke_info_to_db(zipped_list)

    def test(self):
        self.driver.get("file://C://Users//Doug Brown//Desktop//Dannys Stuff//Job//PreferredPartnerDB//scrapers//src//bots//alumni_databases//duke//testing//search.html")
        email = self.profile_scraper.locate_emails()
        phone = self.profile_scraper.locate_phone_numbers()
        name = self.profile_scraper.locate_name()
        print("Returned emails: ", email)
        print("Returned Phone: ", phone)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from src.database.scripts.connect_to_db import connect
import logging
import random
import time
import csv

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

class Scout:
    def __init__(self):
        self.driver_path = 'C://Users//Daniel.Brown//Desktop//PreferredPartnerDB//chromedriver-win64//chromedriver.exe'
        self.max_retries = 3
        self.retry_delay_seconds = 5
        self.driver = self.initialize_webdriver()
        self.last_known_names_index = 0
        self.last_known_links_index = 0
        self.conn, self.crsr = connect()
        

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

    def search_linkedin_profiles(self, attempt=1):
        """Searches for LinkedIn profiles related to CMS on Google."""
        try:
            self.driver.get('https://www.google.com')  # Corrected URL
            wait = WebDriverWait(self.driver, 3)
            search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
            search_box.send_keys('site://linkedin.com/in "CMS" or "Centers for Medicare and Medicaid Services"')
            search_box.send_keys(Keys.ENTER)
        except TimeoutException as e:
            if attempt <= self.max_retries:
                self.handle_timeout(e, attempt)
            else:
                logging.critical("Maximum retries reached. Unable to navigate to Google: %s", e)
        except Exception as e:
            self.handle_other_exception(e)

    def handle_timeout(self, e, attempt):
        """Handles TimeoutExceptions during navigation."""
        self.driver.quit()
        logging.error("Timeout has occurred - Retrying (Attempt %d): %s", attempt, e)
        time.sleep(self.retry_delay_seconds)
        self.driver = self.initialize_webdriver()  # Reinitialize webdriver
        self.search_linkedin_profiles(attempt=attempt+1)  # Retry with incremented attempt count

    def handle_other_exception(self, e):
        """Handles other exceptions during navigation."""
        logging.error('An error has occurred: %s', e)

    def locate_names(self, attempt=1) -> list:
        """Finds the links and names and returns a list"""
        parsed_names_list = []
        logging.info('self.last_known_index = %d', self.last_known_names_index)

        try: 
            names_wait = WebDriverWait(self.driver, 10)
            names_wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'LC20lb.MBeuO.DKV0Md')))
            names = self.driver.find_elements(By.CLASS_NAME, 'LC20lb.MBeuO.DKV0Md')
            
            # Start scraping from the last known index
            new_elements = names[self.last_known_names_index:]

            logging.info("Length of names: %d", len(names))
            logging.info("Last known index: %d", self.last_known_names_index)
            logging.info("Length of new elements: %d", len(new_elements))

            # Parse the names and add to list
            parsed_names_list = [name.text.split(' -')[0] for name in new_elements]

            # Update the last known index
            self.last_known_names_index += len(new_elements)

        except Exception as e:
            if attempt <= self.max_retries:
                logging.warning('Name elements not found. Retrying in %d seconds. (Attempt %d/%d)', self.retry_delay_seconds, attempt, self.max_retries)
                return self.locate_names(attempt + 1)
            else:
                logging.critical("Maximum retries. Check class name or try again later.\nError log:\n%s", e)

        return parsed_names_list
            
    def locate_links(self, attempt=1) -> list:
        """Finds the LinkedIn profile links and returns a list"""
        parsed_links = []
        logging.info('self.last_known_index (links)= %d', self.last_known_links_index)

        try:
            # Wait for the links to load
            links_wait = WebDriverWait(self.driver, 10)
            links_wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
            
            # Collect all links
            links = self.driver.find_elements(By.TAG_NAME, 'a')

            # Start scraping from the last known index
            new_elements = links[self.last_known_links_index:]

            # Only keep the LinkedIn links
            parsed_links = [link.get_attribute('href') for link in new_elements if link.get_attribute('href') is not None and 'www.linkedin.com/in' in link.get_attribute('href')]

            # Update the last known index
            self.last_known_links_index = len(links)


        except Exception as e:
            if attempt <= self.max_retries:
                logging.warning('Link elements not found. Retrying in %d seconds. (Attempt %d/%d)', self.retry_delay_seconds, attempt, self.max_retries)
                return self.locate_links(attempt + 1)
            else:
                logging.critical("Maximum retries. Check class name or try again later")

        return parsed_links
    
    def scroll(self):
        """Scrolls down to load more search results"""
        time.sleep(random.uniform(3, 5))
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            more_results_button = WebDriverWait(self.driver, random.uniform(5, 7)).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="botstuff"]/div/div[3]/div[4]/a[1]/h3/div/span[2]')
                )
            )
            more_results_button.click()
            print('"More Results" button found and clicked')
        except Exception as e:
            print('No "More Results" button found')

    def scroll_and_fetch_data(self, final_user_count: int):
        """Scrolls down to load more search results and fetches links and names"""
        parsed_names_list = []
        parsed_links = []
        try:
            while len(parsed_names_list) < final_user_count and len(parsed_links) < final_user_count:
                # Scroll down
                self.scroll()
                time.sleep(2)

                # Fetch links
                new_links = self.locate_links()
                parsed_links.extend(new_links)

                # Fetch names
                new_names = self.locate_names()
                parsed_names_list.extend(new_names)

                logging.info("Total links fetched: %d", len(parsed_links))
                logging.info("Total names fetched: %d", len(parsed_names_list))

        except Exception as e:
            logging.error("An error occurred while scrolling and fetching data: %s", e)

        return parsed_names_list, parsed_links
    
    def count_users_table_rows(self):
        # Find out how many rows are in the database
        self.crsr.execute('SELECT COUNT(*) FROM users;')
        number_of_rows_in_users_table = self.crsr.fetchone()[0]
        return number_of_rows_in_users_table
    

    def zip_lists(self, parsed_names_list, parsed_links_list):
        zipped_list = list(zip(parsed_names_list, parsed_links_list))
        return zipped_list
    

    def update_database(self, zipped_list):
        try:
            for name, url in zipped_list:
                # Check if the user already exists in the database
                self.crsr.execute(
                    "SELECT COUNT(*) FROM users WHERE users_name = %s",
                    (name,)
                )
                count = self.crsr.fetchone()[0]
                
                # If the user doesn't exist, insert into the database
                if count == 0:
                    self.crsr.execute(
                        "INSERT INTO users (users_name, profile_url) VALUES (%s, %s)",
                        (name, url)
                    )
                    print(f"Data for {name} inserted into database successfully.")
                
                # If the user already exists, skip insertion
                else:
                    print(f"Data for {name} already exists in the database. Skipping insertion.")
            
            self.conn.commit()
        except Exception as e:
            print(f"Failed to insert data into database: {e}")
            self.conn.rollback()



    def execute(self, final_user_count: int):

        # Navigate to Google and search for linkedin profiles

        self.search_linkedin_profiles()
        
        # Count the number of rows in the existing database

        parsed_names_list, parsed_links = self.scroll_and_fetch_data(final_user_count)

        # Zip the lists together

        zipped_list = self.zip_lists(parsed_names_list, parsed_links)

        # Update the database

        self.update_database(zipped_list)
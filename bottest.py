from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from src.database.scripts.connect_to_db import connect
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
        # Connect to the database
        self.conn, self.crsr = connect()

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

    def get_profile_urls(self, bot_id, number_of_users_per_bot=20):
        # Access the database 
        starting_index = 1
        # Only assign a certain portion of the database to the bot
        self.crsr.execute(f"SELECT profile_url FROM users WHERE user_id BETWEEN {(number_of_users_per_bot * (bot_id - 1)) + starting_index} AND {number_of_users_per_bot * bot_id} ORDER BY user_id;")
        #self.crsr.execute("SELECT profile_url FROM users WHERE user_id = 2;")  # Test case
        profile_urls = self.crsr.fetchall()
        profile_urls = [url[0] for url in profile_urls]
        return profile_urls

    def access_linkedin(self):
        try:
            self.driver.get("file://C://Users//Doug Brown//Desktop//Dannys Stuff//Job//PreferredPartnerDB//prettified_danny.html")
        except TimeoutError as e:
            print(f"Timeout has occurred while trying to find LinkedIn\n{e}")
        except Exception as e:
            print(f"An error occurred while trying to get to LinkedIn\n{e}")
    
    def scroll_down(self):
        # Generate a random scroll distance between 750 and 1250 units
        scroll_distance = random.randint(750, 1250)
        
        # Execute JavaScript to scroll down
        js_script = f"window.scrollBy(0, {scroll_distance});"
        self.driver.execute_script(js_script)

    def locate_list_elements_in_new_page(self):
        try:
            # Wait for all the list elements to load
            list_elements = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated.pvs-list__item--one-column"))
            )

            return list_elements
        
        except Exception as e:
            print(f"Could not locate li elements.\n{e}")


    def locate_work_experience_if_multiple_positions_at_one_company(self, list_elements, user_id) -> dict:
        work_experience_dict = {}
        print(f"User ID: {user_id}")
        try:
            for i, list_element in enumerate(list_elements):
                print(f"List element: {i}")
                print(len(list_elements))
                anchor_tags_within_li_elements = list_element.find_elements(By.XPATH, ".//a[contains(@class, 'flex-column')]")
                if anchor_tags_within_li_elements:
                    for anchor in anchor_tags_within_li_elements:
                        # Look for company names nested under the parent anchor tag
                        # If a company name is not found, don't do anything
                        company_name = anchor.find_element(By.XPATH, ".//span").text
                        if company_name:
                            job_titles = list_element.find_elements(By.XPATH, "div/div/div/div/ul/li/div/div/div/ul/li/div/div/div/div/a/div/div/div/div/span[@aria-hidden='true']")
                            company_jobs = [job.text for job in job_titles]
                            if company_name in work_experience_dict:
                                # If company_name already exists in the dictionary, extend its list of jobs
                                work_experience_dict[company_name].extend(company_jobs)
                                print(work_experience_dict)
                            else:
                                # If company_name is not yet in the dictionary, add it with its list of jobs
                                work_experience_dict[company_name] = company_jobs
                                print(work_experience_dict)

                            break  # Break out of the inner loop once we've found the company name
                else:
                    # Find the work experience where there was only one position
                    job_title_element = list_element.find_element(By.XPATH, "div/div/div/div/div/div/div/div/div/span[@aria-hidden='true']")
                    job_title = job_title_element.text
                    job_title = job_title.split('\n')[0].strip()
                    print(f"JOB TITLE TESt: {job_title}")
                    # Get company name by traversing up the DOM hierarchy
                    company_name_ancestor_div_element = job_title_element
                    for _ in range(5):  # Loop 4 times to ascend to the desired ancestor
                        company_name_ancestor_div_element = company_name_ancestor_div_element.find_element(By.XPATH, "..")
                    company_name_element = company_name_ancestor_div_element.find_element(By.XPATH, "./span[@class='t-14 t-normal']/span[@aria-hidden='true']")
                    company_name = company_name_element.text
                    print(f"Company: {company_name}. Job title: {job_title}")
                    work_experience_dict[company_name] = job_title
        except:
            print("could not find")

        return work_experience_dict

    def update_db_with_work_experience(self, work_experience, user_id):
        # Insert job experiences into the database
        for company, job_titles in work_experience.items():
            # If job_titles is a list, insert each job title separately
            if isinstance(job_titles, list):
                for job_title in job_titles:
                    self.crsr.execute("INSERT INTO work_experience (user_id, company, title) VALUES (%s, %s, %s)", (user_id, company, job_title))
            else:
                # If job_titles is a string, insert it as a single record
                self.crsr.execute("INSERT INTO work_experience (company, title) VALUES (%s, %s, %s)", (user_id, company, job_titles))

        self.conn.commit()

    
    def scrape_experiences_in_new_page(self):
        time.sleep(random.uniform(3, 6))
        self.scroll_down()
        
        list_elements = self.locate_list_elements_in_new_page()
        work_experience_dict = self.locate_work_experience_if_multiple_positions_at_one_company(list_elements, user_id=2)
        # self.update_db_with_work_experience(work_experience=work_experience_dict, user_id=2)

        print(work_experience_dict)

    def locate_work_experience_on_original_page(self):
        work_experience = {}
        
        # Locate the div with id="experience", our entry point for all experience information
        experience_div_element = self.wait.until(
            EC.presence_of_element_located((By.ID, "experience"))
        )
        
        # Find the sibling div tag containing the experience information
        sibling_div_tag = experience_div_element.find_element(By.XPATH, './following-sibling::div[2]')
        
        # Find all list items within the sibling div tag
        list_items = sibling_div_tag.find_elements(By.XPATH, 'ul/li')
        
        # Iterate through each list item
        for item in list_items:
            # Check if there are multiple experiences for one company
            anchor_tags = item.find_elements(By.XPATH, ".//a[contains(@class, 'flex-column')]")
            if len(anchor_tags) > 2:
                names_list = [anchor.find_element(By.XPATH, ".//span").text for anchor in anchor_tags]
                company_name = names_list[0]
                jobs = names_list[1:]
                work_experience[company_name] = jobs
            else:
                # Extract company name, job title, and other metadata
                company = item.find_element(By.XPATH, "div/div/div/div/span/span[@aria-hidden='true']").text.split(' ·')[0]
                job_title = item.find_element(By.XPATH, "div/div/div/div/div/div/div/div/span[@aria-hidden='true']").text
                work_experience[company] = job_title

        return work_experience



        

    def execute(self):

        # Access the linkedin.com website

        self.access_linkedin()

        work_experience = self.locate_work_experience_on_original_page()
        print(work_experience)


        




from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from ...database.scripts.connect_to_db import connect
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


    def access_linkedin(self):
        try:
            self.driver.get("https://www.linkedin.com/")
        except TimeoutError as e:
            print(f"Timeout has occurred while trying to find LinkedIn\n{e}")
        except Exception as e:
            print(f"An error occurred while trying to get to LinkedIn\n{e}")

    def click_sign_in(self):
        try:
            # Locate the sign in button
            sign_in_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "nav__button-secondary.btn-md.btn-secondary-emphasis")))
            print("Found the sign in button for the click_sign_in method in the LinkedInBot")
            sign_in_button.click()

        except NoSuchElementException as e:
            print(f"Could not locate the sign in button\n{e}")
        
        except Exception as e:
            print(f"An error occurred while trying to locate the sign in button.\n{e}")

    def send_username(self, bot_id):
        # Fetch username from database

        try:
            self.crsr.execute(f"SELECT bot_email FROM bots WHERE bot_id = {bot_id}")
            username = self.crsr.fetchone()[0]

            try:
                # Locate the username form
                username_form = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
                print("username form located")
                username_form.send_keys(username)

            except NoSuchElementException as e:
                print(f"Could not locate the username form\n{e}")

            except Exception as e:
                print(f"Error occurred while trying to locate the username form.\n{e}")

        except Exception as e:
            print(f"An error occurred while trying to get the username from the database {e}")

        

    def send_password(self, bot_id):
        try:
            self.crsr.execute(f"SELECT bot_email_password FROM bots WHERE bot_id = {bot_id}")
            password = self.crsr.fetchone()[0]
            try:
                # Locate the password form
                password_form = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
                print("Password form located")
                password_form.send_keys(password)

            except NoSuchElementException as e:
                print(f"Could not locate the password form.\n{e}")

            except Exception as e:
                print(f"An error occured while looking for the password form.\n{e}")

        except Exception as e:
            print("An error occurred while trying to locate the bot password")

        
    def click_login_signin_button(self):
        try:
            # Locate the sign in button after typying in username and password
            sign_in_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
            print("Sign in button located")
            sign_in_button.click()

        except NoSuchElementException as e:
            print(f"Could not locate the sign in button.\n{e}")

        except Exception as e:
            print(f"An error occured while looking for the sign in button.\n{e}")

    def handle_captcha(self):
        is_captcha_solved = input("Type y when you solve the captcha:\n")

        if is_captcha_solved == 'y':
            pass

    def get_profile_urls(self, bot_id, number_of_users_per_bot=20):
        # Access the database 
        starting_index = 1
        # Only assign a certain portion of the database to the bot
        self.crsr.execute(f"SELECT profile_url FROM users WHERE user_id BETWEEN {(number_of_users_per_bot * (bot_id - 1)) + starting_index} AND {number_of_users_per_bot * bot_id} ORDER BY user_id;")
        #self.crsr.execute("SELECT profile_url FROM users WHERE user_id = 2;")  # Test case
        profile_urls = self.crsr.fetchall()
        profile_urls = [url[0] for url in profile_urls]
        return profile_urls
    
    def visit_user(self, profile_url):
        try:
            self.driver.get(f"{profile_url}")

        except Exception as e:
            print("Could not access users profile")

    def find_users_name(self):
        try:
            users_name = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-heading-xlarge"))
            )
            users_name = users_name.text
            return users_name

        except NoSuchElementException as e:
            print(f"Could not locate the name.\n{e}")
        
        except Exception as e:
            print(f"Error finding the name\n{e}")
            
    def send_names_to_db(self, users_name, profile_url):
        # Update the datbase
        try:
            self.crsr.execute(f"UPDATE users SET users_name = '{users_name}' WHERE profile_url = '{profile_url}'")
            # Commit the transaction
            self.conn.commit()
        except Exception as e:
            print(e)
        
    def extract_current_location(self):
        # Locate the users location found under their name
        try:
            users_location = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]'))
            )
            users_location = users_location.text
            return users_location

        except NoSuchElementException as e:
            print(f"Unable to find the users location.\n{e}")
            return None
        
        except Exception as e:
            print(f"There was an error trying to find the users location.\n{e}")
            return None
        
    def update_location_in_db(self, users_location, profile_url):
        # Checks if the location was found in the scraping
        if users_location is not None:
            # SQL query that updates the database
            self.crsr.execute(f"UPDATE users SET location_of_user = '{users_location}' WHERE profile_url = '{profile_url}';")
            # Commit the transaction
            self.conn.commit()

        else:
            logging.INFO("The location was not found")
            pass

    def connect_with_user(self):
        try:
            connect_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[@id="ember62"]'))
            )

            connect_button.click()

            try:
                send_without_note_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@id="ember191"]'))
                )
                send_without_note_button.click()

            except NoSuchElementException as e:
                print(f"Could not find the send without a message button\n{e}")
            

        except NoSuchElementException as e:
            print(f"Connect button was not found.\n{e}")

        except Exception as e:
            print(f"Error occurred with connect_with_user()\n{e}")   

    def download_html_content(self, filename):
        """Downloads the HTML content of the current web page.
        
            Returns:
                str: The HTML content of the current web page.
        """
        html_content = self.driver.page_source
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_content)

    def locate_show_all_experiences_button(self):
        try:
            # Wait for the presence of at least one matching element
            buttons = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(span[@class='pvs-navigation__text'], 'Show all') and contains(span[@class='pvs-navigation__text'], 'experiences')]"))
            )

            # Iterate through each button
            for button in buttons:
                # Check if the button's href attribute contains the LinkedIn domain
                href = button.get_attribute("href")
                if href and 'linkedin.com' in href:
                    return href

        except Exception as e:
            print(f"An error occurred: {e}")

        return None
    
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
                self.crsr.execute("INSERT INTO work_experience (user_id, company, title) VALUES (%s, %s, %s)", (user_id, company, job_titles))

        self.conn.commit()

        print("Updated work experience into database")

    
    def scrape_experiences_in_new_page(self, user_id):
        time.sleep(random.uniform(3, 6))
        self.scroll_down()
        
        list_elements = self.locate_list_elements_in_new_page()
        work_experience_dict = self.locate_work_experience_if_multiple_positions_at_one_company(list_elements, user_id=user_id)
        self.update_db_with_work_experience(work_experience=work_experience_dict, user_id=user_id)

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
    
    def scrape_experiences_in_original_page(self, user_id):
        time.sleep(random.uniform(3, 6))
        self.scroll_down()
        
        work_experience_dict = self.locate_work_experience_on_original_page()
        self.update_db_with_work_experience(work_experience=work_experience_dict, user_id=user_id)

        print(work_experience_dict)
        

    def execute(self):

        # Access the linkedin.com website

        self.access_linkedin()

        # Click the sign in button (Sign into existing account) 

        self.click_sign_in()

        # Send in the username to the username input field
        #  Make sure to get this from the database

        self.send_username(bot_id=1)

        # Send the password to the password input field
        #  Make sure to get this from the databse

        self.send_password(bot_id=1)

        # Click the sign in button
        time.sleep(random.uniform(6, 8))
        self.click_login_signin_button()

        # Handle the captcha manually

        self.handle_captcha()
        
        # Assign user profiles to a bot
        
        profile_urls = self.get_profile_urls(bot_id=1)

        print(profile_urls)
        
        profile_urls[0] = 'https://www.linkedin.com/in/mattcaccavale/'  # Test case

        # Loop through urls in the list

        for profile_url in profile_urls:

            # Get user_id

            self.crsr.execute(f"SELECT user_id FROM users WHERE profile_url = '{profile_url}'")
            user_id = self.crsr.fetchone()[0]
            
            time.sleep(random.uniform(5, 9))
            # Visit the user's profile

            self.visit_user(profile_url)

            # Find their name print it then update the database

            users_name = self.find_users_name()
            print(users_name)
            self.send_names_to_db(users_name, profile_url)
            print("Database updated")

            # Find the user's location then update the database

            users_location = self.extract_current_location()
            print(f"Locations is {users_location}")
            self.update_location_in_db(users_location, profile_url)

            # Check for a show all experiences button

            button_href = self.locate_show_all_experiences_button()

            if button_href:
                self.driver.get(button_href)
                self.scrape_experiences_in_new_page(user_id=user_id)
            else:
                print("Could not find button href")
                # Collect experience in current page
                self.scrape_experiences_in_original_page(user_id=user_id)

            time.sleep(1000)




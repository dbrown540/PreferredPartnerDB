from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from ...database.scripts.connect_to_db import connect
from ...database.scripts.database_manager import DatabaseManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import logging
import time
import random
import re
import psycopg2
from typing import object, Union

class LinkedInBot:
    def __init__(self):
        self.driver_path = 'chromedriver-win64/chromedriver.exe'
        # Initialize the WebDriver with the random user agent
        self.driver = self.initialize_webdriver()
        self.wait = WebDriverWait(self.driver, 10)
        # Create a database manager object
        self.database_manager = DatabaseManager()

    def initialize_webdriver(self) -> WebDriver:
        """
        Initializes a WebDriver instance with specified options and service.
    
        Returns:
            WebDriver: A WebDriver instance with specified options and service.
    
        Raises:
            WebDriverException: If there is an issue initializing the WebDriver.
            Exception: If an unexpected error occurs while initializing the WebDriver.
        """
        try:
            options = Options()
            options.add_argument('--start-maximized')
            service = Service(self.driver_path)
            driver = WebDriver(service=service, options=options)
            # Log the webdriver information
            logging.info(f"\nService path: {self.driver_path}\nOptions: {options}")
            return driver
        except WebDriverException:
            logging.critical('Failed to initialize WebDriver: ', exc_info=True)
            raise
        except Exception:
            # For other exceptions, log the error and provide a generic error message
            logging.critical('An unexpected error occurred while initializing WebDriver: ', exc_info=True)
            raise

    def access_linkedin(self) -> None:
        """
        Access the LinkedIn website using the Selenium WebDriver.
    
        This function navigates to the LinkedIn website by accessing the provided URL.
        
        Raises:
            WebDriverException: If there is an error related to the WebDriver.
            Exception: If there is an unexpected error while trying to access LinkedIn.
        """
        try:
            # Access the LinkedIn website
            self.driver.get("https://www.linkedin.com/")

        except WebDriverException as driver_error:
            # Log and raise any error related to the WebDriver
            logging.critical("A WebDriver-related error occurred while trying to connect to LinkedIn.", exc_info=True)
            raise driver_error
        
        except Exception as unexpected_error:
            # Log and raise any unexpected errors
            logging.critical("An error occurred while trying to get to LinkedIn.", exc_info=True)
            raise unexpected_error

    def click_sign_in(self):
        """Click the sign-in button on the LinkedInBot page.
        
        This function locates the sign-in button on the LinkedInBot page and clicks it.
        
        Raises:
            NoSuchElementException: If the sign-in button cannot be located.
            Exception: If an unexpected error occurs while trying to locate the sign-in button.
        """
        try:
            # Locate the sign-in button
            sign_in_button = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "nav__button-secondary.btn-md.btn-secondary-emphasis"))
            )

            # Log a message indicating successful sign-in button detection
            logging.info("Successfully located the sign-in button.")

            # Click the sign-in button
            sign_in_button.click()

        except NoSuchElementException:
            # Log and raise a critical error if the sign-in button cannot be located
            logging.critical("Failed to locate the sign-in button.", exc_info=True)
            raise
            
        except Exception:
            # Log and raise a critical error if an unexpected error occurs
            logging.critical("An unexpected error occurred while locating the sign-in button.", exc_info=True)
            raise

    def type_email_in_linkedin_login(self, bot_id):
        """Fetches the email associated with the provided bot_id from the database and types it into the email input field on the LinkedIn login screen.
        
        Args:
            bot_id (int): The unique identifier of the bot.
        
        Raises:
            psycopg2.Error: If there is an error while fetching the email from the database.
            NoSuchElementException: If the username input field on the LinkedIn login screen is not found.
            Exception: If an unexpected error occurs during the process.
        
        Returns:
            None
        """
        try:
            # Define query arguments
            query = "SELECT bot_email FROM bots WHERE bot_id = %s"
            params=(bot_id,)
            fetch = "ONE"

            # Retrieve email from database for corresponding bot ID then store as a variable
            email = self.database_manager.execute_query(query=query, params=params, fetch=fetch)[0]

            # Log a message indicating the successful location and typing of the email input on the LinkedIn login screen
            logging.info(f"Successfully retrieved email {email} from the database.")

            # Locate the username input on the LinkedIn login screen
            email_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )

            # Type the email into the login input field
            email_input.send_keys(email)

            # Log a message indicating the successful location of the email input
            logging.info("Successfully typed email into the input field.")

            # Close the cursor and database connection
            self.crsr.close()
            self.conn.close()
            logging.info("Closed the cursor and database connection after ")

        except psycopg2.Error as db_error:
            # Log a database error if the email cannot be retrieved
            logging.critical("Failed to fetch email from the database.", exc_info=True)
            raise db_error

        except NoSuchElementException:
            # Log and raise critical error if the username input is not found.
            logging.critical("Failed to locate the username input on the LinkedIn login screen.", exc_info=True)
            raise

        except Exception as unexpected_error:
            # Log and raise critical error if an unexpected error if any other exception occurs
            logging.critical(f"An unexpected error occurred.", exc_info=True)
            raise unexpected_error

        

    def type_password_in_linkedin_login(self, bot_id):
        """Type the password into the LinkedIn login form using the provided bot_id.
        
        Args:
            bot_id (int): The unique identifier of the bot whose password needs to be typed.
        
        Raises:
            psycopg2.Error: If there is an error with the database connection or query.
            NoSuchElementException: If the password input field cannot be located on the LinkedIn login screen.
            Exception: For any other unexpected errors.
        
        Logs:
            - Successful retrieval of the password from the database.
            - Successful typing of the password into the password input field.
            - Failure to fetch LinkedIn password from the database.
            - Failure to locate the password input field on the LinkedIn login screen.
            - An unexpected error occurred.
        """
        try:
            # Define query arguments
            query = "SELECT bot_email_password FROM bots WHERE bot_id = %s" 
            params = (bot_id,) 
            fetch = "ONE"

            # Fetch bot password from the database with a corresponding bot_id
            password = self.database_manager.execute_query(query=query, params=params, fetch=fetch)

            # Log the successful retrieval of the password from the database
            logging.info(f"Successfully retrieved the linkedin password {password} from the database.")

            # Locate the password form
            password_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "password"))
            )

            # Type the password
            password_input.send_keys(password)

            # Log a message indicating the successful typing of the password into the input field
            logging.info("Successfully typed password in the password input")

        except psycopg2.Error:
            # Log and raise critical database error if the query failed
            logging.critical("Failed to fetch LinkedIn password from the database.", exc_info=True)
            raise

        except NoSuchElementException:
            # Log and raise a critical WebDriver error if the password input was unable to be located
            logging.critical("Failed to locate the password input field on the LinkedIn login screen.", exc_info=True)
            raise

        except Exception:
            # Log and raise a critical unexpected error.
            logging.critical("An unexpected error occurred.", exc_info=True)
            raise


    def click_login_signin_button(self) -> None:
        """
        Clicks the sign-in button on the login screen.

        This function attempts to locate and click the sign-in button on the login screen. 
        It retries a specified number of times if the button is not immediately found.

        Raises:
            NoSuchElementException: If the sign-in button element is not found on the page.
            TimeoutException: If a timeout occurs while waiting for the sign-in button to become clickable.

        Returns:
            None
        """

        MAX_RETRIES = 3
        INITIAL_DELAY = 1

        for retry in range(MAX_RETRIES):
            try:
                # Locate the sign in button after typing in username and password
                sign_in_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
                )

                # Log a message indicating the successful location of the sign-in button
                logging.info("Sign in button located on the login screen.")

                # Click the sign-in button
                sign_in_button.click()

                # Exit the loop if the click was successful
                break

            except NoSuchElementException:
                # Raise and log a critical error if the sign in button is not found
                logging.critical("Could not find the sign in button.", exc_info=True)
                raise

            except TimeoutException:
                # Log the retry attempt
                logging.error(f"Timeout error occurred. Attempt: {retry + 1}/{MAX_RETRIES}. Retrying in {INITIAL_DELAY} seconds.")
                time.sleep(INITIAL_DELAY)

        else:
            # Log and raise a critical error if the maximum number of retries is reached
            logging.critical("Maximum retries reached.", exc_info=True)
            raise



    def handle_captcha(self):
        is_captcha_solved = input("Type y when you solve the captcha:\n")

        if is_captcha_solved == 'y':
            pass

    def get_profile_urls(self, bot_id: int, number_of_users_per_bot: int = 20) -> list:
        """
        Get profile URLs for a specific bot from the database.
    
        Args:
            bot_id (int): The ID of the bot for which profile URLs are to be retrieved.
            number_of_users_per_bot (int, optional): The number of users per bot. Defaults to 20.
    
        Returns:
            list: A list of profile URLs for the specified bot.
        """

        # Create query
        query = "SELECT profile_url FROM users WHERE user_id BETWEEN %s AND %s ORDER BY user_id;"
        
        # Calculate parameter values
        starting_index = 1
        start_user_id = (number_of_users_per_bot * (bot_id - 1)) + starting_index
        end_user_id = number_of_users_per_bot * bot_id

        # Query the database and store the urls in a list
        raw_profile_urls = self.database_manager.execute_query(query, params=(start_user_id, end_user_id), fetch="ALL")

        # Extract urls from the tuples
        profile_urls = [url[0] for url in raw_profile_urls]

        return profile_urls
    
    def visit_user(self, profile_url: str) -> None:
        """
        Visits the user's profile by navigating to the provided profile URL.
    
        Args:
            profile_url (str): The URL of the user's profile to visit.
    
        Raises:
            WebDriverException: If a WebDriver related error occurs while trying to access the user's profile.
            Exception: If an unexpected error occurs while attempting to visit the user's profile.
        """
        try:
            self.driver.get(f"{profile_url}")

        except WebDriverException:
            # Log and raise a critical WebDriver exception if there was a driver related error
            logging.critical(f"A WebDriver related error occurred while trying to access the user's profile. Link:\n{profile_url}", exc_info=True)
            raise

        except Exception:
            # Log and raise a critical error if an unexpected error occurred
            logging.critical(f"An unexpected error occurred while attempting to visit the user's profile. Link:\n{profile_url}")
            raise

    def find_users_name(self) -> Union[str, None]:
        """
        Find the user's name on their profile.
        
        Returns:
            str: The user's name if found, None otherwise.
        """
        try:
            # Locate the name on the user's profile
            users_name = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-heading-xlarge"))
            ).text

            return users_name
        
        except TimeoutException:
            # Log and handle timeout exception
            logging.error(f"Could not locate user's name due to timeout.")
            return None

        except NoSuchElementException:
            # Log and handle element not found exception
            logging.error("Could not locate the element containing the user's name on their profile.")
            return None
        
        except Exception as e:
            # Log and handle other unexpected exceptions
            logging.error(f"An unexpected error occurred while trying to locate the user's name. {str(e)}")
            return None
            
    def send_names_to_db(self, users_name: str, profile_url: str) -> None:
        """
        Update the database with the given user's name and profile URL.
        
        Args:
            users_name (str): The name of the user to be updated.
            profile_url (str): The profile URL of the user.
    
        Returns:
            None
        """
        # Define query arguments
        query = "UPDATE users SET users_name = '%s' WHERE profile_url = '%s'"
        params = (users_name, profile_url)

        # Update the datbase
        self.database_manager.execute_query(query=query, params=params)

        
    def extract_current_location(self) -> Union[str, None]:
        """
        Extracts the current location of the user.
    
        This function locates the span element that contains the user's location on the webpage.
    
        Returns:
            str: The user's location.
            None: If unable to locate the user's location due to a timeout, missing element, or unexpected error.
        """
        try:
            # Locate the span element that contains the user's location
            users_location = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]'))
            ).text

            return users_location

        except TimeoutException:
            # Log and handle a timeout error
            logging.error("Timeout error occurred while attempting to find the HTML element containing the user's location.")
            return None

        except NoSuchElementException as e:
            # Log and handle NoSuchElement exception
            logging.error("Could not locate the HTML element containing the user's name.")
            return None
        
        except Exception as e:
            # Log and handle unexpected errors
            logging.error(f"An unexpected error occurred while trying to find the user's location. {str(e)}")
            return None
        
    def update_location_in_db(self, users_location: str, profile_url: str) -> None:
        """
        Update the location of a user in the database.
    
        Args:
            users_location (str): The new location of the user.
            profile_url (str): The profile URL of the user.
    
        Returns:
            None
        """

        # Define query and params arguments
        query = "UPDATE users SET location_of_user = '%s' WHERE profile_url = '%s';"
        params=(users_location, profile_url)
    
        # Update the database to include the location of the user (locate using the profile url)
        self.database_manager.execute_query(query=query, params=params)


    def connect_with_user(self):
        try:
            # Locate the connect button on the user's main screen
            connect_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[@id="ember62"]'))
            )

            # Click the connect button
            connect_button.click()

            # Locate the button that allows you to connect without sending a note
            send_without_note_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[@id="ember191"]'))
            )

            # Click the "Send without note" button to connect with the user
            send_without_note_button.click()

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
        print(work_experience_dict)
        self.update_db_with_work_experience(work_experience=work_experience_dict, user_id=user_id)

    def locate_skills_button(self):
        try:
            # Wait for the presence of at least one matching element
            buttons = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//a[contains(span[@class='pvs-navigation__text'], 'Show all') and contains(span[@class='pvs-navigation__text'], 'skills')]")
                )
            )

            # Iterate through each button to find the one with LinkedIn domain
            for button in buttons:
                href = button.get_attribute("href")
                if href and 'linkedin.com' in href:
                    return href

        except Exception as e:
            print(f"An error occurred: {e}")

    def create_skills_set(self, list_elements) -> set:
        skills_set = set()
        for i, list_element in enumerate(list_elements):
            print("index: ", i)
            # Attempt to locate the span text within the list element
            span_element = list_element.find_element(By.XPATH, "div/div/div/div/a/div/div/div/div/span[@aria-hidden='true']")
            if span_element:
                span_text = span_element.text
                if span_text != '':
                    skills_set.add(span_text)

        return skills_set

    def locate_skills_list_elements_in_new_page(self):
        # Locate list elements
        list_elements = self.driver.find_elements(By.XPATH, '//li[contains(@class, "pvs-list__paged-list-item")]')
        return list_elements
        
    def scrape_skills_on_new_page(self):
        time.sleep(random.uniform(3, 6))
        self.scroll_down()
        list_elements = self.locate_skills_list_elements_in_new_page()
        print(len(list_elements))

        skills_set = self.create_skills_set(list_elements)

        return skills_set

    def scrape_skills_on_original_page(self):
        time.sleep(random.uniform(3, 6))
        self.scroll_down()
        skills_set = self.locate_skills_list_element_on_original_page()
        return skills_set

    def locate_skills_list_element_on_original_page(self):
        skills_set = set()
        # Locate the skills section
        skills_div = self.wait.until(
            EC.presence_of_element_located((By.ID, "skills"))
        )
        # Switch to sibling element
        sibling_div_tag = skills_div.find_element(By.XPATH, './following-sibling::div[2]')
        if sibling_div_tag:
            # Locate the list elements
            list_elements = sibling_div_tag.find_elements(By.XPATH, "ul/li[contains(@class, 'artdeco-list__item')]")
            for list_element in list_elements:
                # Look for anchor tags in each list element
                anchor_element = list_element.find_element(By.TAG_NAME, "a")
                # Locate the span tag within the anchor element tree
                span_tag = anchor_element.find_element(By.XPATH, './/span[@aria-hidden="true"]')
                span_text = span_tag.text
                print(span_text)
                skills_set.add(span_text)
        else:
            print("could not find the sibling tag")

        return skills_set

    def scrape_skills(self):
        button_href = self.locate_skills_button()
        print(f"BUTTON HREF: {button_href}")
        if button_href:
            self.driver.get(button_href)
            skills_set = self.scrape_skills_on_new_page()
        else:
            print("Button href not found. Scraping skills off original site.")
            skills_set = self.scrape_skills_on_original_page()
            self.driver.back()

        return skills_set

    def update_skills_database(self, skills_set, user_id):
        for skill in skills_set:
            print(f"SKILL: {skill}")
            self.crsr.execute(f"INSERT INTO skills (skill_name, user_id) VALUES (%s, %s)", (skill, user_id))

        self.conn.commit()
        print("All skills were added to the database")

        

    def execute(self):

        # Access the linkedin.com website

        self.access_linkedin()

        # Click the sign in button (Sign into existing account) 

        self.click_sign_in()

        # Send in the username to the username input field
        #  Make sure to get this from the database

        self.type_password_in_linkedin_login(bot_id=1)

        # Send the password to the password input field
        #  Make sure to get this from the databse

        self.type_password_in_linkedin_login(bot_id=1)

        # Click the sign in button
        time.sleep(random.uniform(6, 8))
        self.click_login_signin_button()

        # Handle the captcha manually

        self.handle_captcha()
        
        # Assign user profiles to a bot
        
        profile_urls = self.get_profile_urls(bot_id=1)

        print(profile_urls)

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
                self.driver.back()
            else:
                print("Could not find button href")
                # Collect experience in current page
                self.scrape_experiences_in_original_page(user_id=user_id)
            
            skills_set = self.scrape_skills()
            self.update_skills_database(skills_set, user_id)

            time.sleep(random.randint(4, 8))
            
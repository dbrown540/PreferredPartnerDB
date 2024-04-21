from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from ...database.scripts.connect_to_db import connect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import logging
import time
import random
import re

class LinkedInBot:
    def __init__(self):
        self.driver_path = 'chromedriver-win64/chromedriver.exe'
        self.driver = self.initialize_webdriver()
        self.wait = WebDriverWait(self.driver, 10)
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

    # Do something about rotating proxies

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
        self.crsr.execute(f"SELECT profile_url FROM users WHERE user_id BETWEEN {(number_of_users_per_bot * (bot_id - 1)) + starting_index} AND {number_of_users_per_bot * bot_id}")
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
        



    def click_on_show_all_experience(self):
        """Clicks on the 'Show All Experience' button.
        
            Returns:
                bool: True if the button is clicked successfully, False otherwise.
        """
        try:
            see_all_experience = self.wait.until(
                EC.element_to_be_clickable((By.ID, "navigation-index-see-all-experiences"))
            )

            see_all_experience.click()

            return True

        except:
            return False     


    def locate_work_experience_list_items(self):
        try:
            list_elements = self.wait.until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "li"))
            )

            for element in list_elements:
                print(element)
        except Exception as e:
            print(e)


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

        self.click_login_signin_button()

        # Handle the captcha manually

        self.handle_captcha()
        
        # Assign user profiles to a bot
        
        profile_urls = self.get_profile_urls(bot_id=1)
        
        profile_urls[0] = 'https://www.linkedin.com/in/daniel-brown-5a93441b6'  # Test case

        # Loop through urls in the list

        for profile_url in profile_urls:


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

            '''# Connect with the user
                # This is bugged

            self.connect_with_user()'''

            # Fetch work experience

            work_experience_button_exists = self.click_on_show_all_experience()  # Returns True if the button exists and is clicked

            if work_experience_button_exists:  # If a work experience button exists      
                self.locate_work_experience_list_items()  # Find the <li> elements that contain each work experience

            else:




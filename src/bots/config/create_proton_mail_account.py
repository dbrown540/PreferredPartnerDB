from ...scout.scout import Scout
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import logging
import time
import csv

class Proton(Scout):
    def access_proton_mail(self):
        """Access Proton Mail website using Selenium WebDriver.
        
            This function navigates to the Proton Mail website by opening a new browser window using the Selenium WebDriver instance provided as 'self.driver'.
        
            Raises:
                Exception: If there is an error accessing the Proton Mail website.
        
            Example:
                access_proton_mail(self)
        """
        try:
            self.driver.get("https://proton.me/mail")
        except Exception as e:
            print("Error accessing Proton Mail:", e)

    def click_create_account(self):
        """Clicks on the 'Create Account' link on the webpage.
        
            This function locates the 'Create Account' link on the webpage and clicks on it.
            
            Args:
                self: The object instance of the class.
                
            Returns:
                None
        """
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
            possible_create_account_links = self.driver.find_elements(By.TAG_NAME, "a")

            for possible_link in possible_create_account_links:
                attribute = possible_link.get_attribute('href')
                if 'https://proton.me/mail/pricing' in attribute:
                    try:
                        # Click on the link
                        possible_link.click()
                        time.sleep(3)
                        logging.INFO("Create Account link clicked successfully")
                        break
                    except Exception as e:
                        print("Error clicking on the link:", e)
        except Exception as e:
            print("Error clicking create account:", e)

    def click_get_proton_free(self):
        """Clicks on the Proton free plan link after waiting for 2 seconds.
        
            This function waits for the presence of all elements located by tag name 'a' and then clicks on the link that contains 'plan=free' in its href attribute.
            
            Args:
                self: The object instance of the class.
                
            Returns:
                None
        """
        try:
            time.sleep(2)
            self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
            possible_proton_free_links = self.driver.find_elements(By.TAG_NAME, "a")
            for possible_proton_free_link in possible_proton_free_links:
                proton_attribute = possible_proton_free_link.get_attribute("href")
                if 'plan=free' in proton_attribute:
                    try:
                        possible_proton_free_link.click()
                        time.sleep(3)
                        break
                    except Exception as e:
                        logging.critical("Free plan link not found\nError:\n%s", e)

        except Exception as e:
            print("Error clicking get Proton free:", e)

    def fetch_bot_email_header(self, row):
        """Fetch the email header from the database.

        Args:
            row (int): The row number to select from the database.

        Returns:
            str: The email header fetched from the database.
        """
        try:
            self.crsr.execute(f"SELECT bot_email_header FROM bots OFFSET {row} LIMIT 1;")
            email_header = self.crsr.fetchone()[0]
            print("Email header:", email_header)
            # Commit the transaction and close the cursor
            self.conn.commit()
            self.crsr.close()
            return email_header

        except Exception as e:
            logging.critical("Error occurred while querying the database:\n%s", e)

    def interact_with_username_input(self, email_header):
        """Interact with the username input field.

        Args:
            email_header (str): The email header to input into the username field.

        Raises:
            TimeoutException: Timeout waiting for the username iframe.
            NoSuchElementException: Input field not found within iframe.
            Exception: Error while interacting with input field within iframe.
        """

        try:
            wait = WebDriverWait(self.driver, 10)
            time.sleep(3)  # You might not need this sleep anymore
            username_iframe = wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="Username"]')))
            self.driver.switch_to.frame(username_iframe)

            try:
                username_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'email-input-field')))
                username_input.send_keys(email_header)
            except NoSuchElementException:
                logging.error("Input field not found within iframe.")
            except Exception as e:
                logging.error("Error while interacting with input field within iframe:\n%s", e)
            finally:
                # Always switch back to the default content after interacting with elements within an iframe
                self.driver.switch_to.default_content()
        
        except TimeoutException:
            logging.error("Timeout waiting for the username iframe.")
        except Exception as e:
            logging.error("Error occurred while trying to switch to the username iframe:\n%s", e)

    def fetch_bot_email_header_and_interact(self, row):
        """Fetch email header from database and interact with username input field.

        Args:
            row (int): The row number to select from the database.
        """
        email_header = self.fetch_bot_email_header(row)
        if email_header:
            self.interact_with_username_input(email_header)

    def fetch_bot_password(self, row):
        """Fetch bot password from the database.

        Args:
            row (int): The row number to fetch bot password from the database.

        Returns:
            str: The bot email password fetched from the database.
        """
        try:
            self.crsr = self.conn.cursor()
            self.crsr.execute(f"SELECT bot_email_password FROM bots OFFSET {row} LIMIT 1")
            bot_email_password = self.crsr.fetchone()[0]
            self.conn.commit()
            self.crsr.close()
            return bot_email_password

        except Exception as e:
            logging.error("Error occurred while fetching bot password from the database:\n%s", e)
            return None

    def interact_with_password_inputs(self, bot_email_password):
        """Interact with password input fields on a web page.

        Args:
            bot_email_password (str): The bot email password to input into the password fields.

        Raises:
            NoSuchElementException: If the password input fields are not found on the web page.
            Exception: If an unexpected error occurs while interacting with the input fields.
        """
        try:
            password_input_field = self.driver.find_element(By.ID, 'password')
            password_input_field.send_keys(bot_email_password)

            repeat_password_input_field = self.driver.find_element(By.ID, 'repeat-password')
            repeat_password_input_field.send_keys(bot_email_password)

        except NoSuchElementException as e:
            logging.error("Password input fields not found on the web page:\n%s", e)

        except Exception as e:
            logging.error("Error occurred while interacting with password input fields:\n%s", e)

    def fetch_bot_password_and_interact(self, row):
        """Fetch bot password from database and interact with password input fields on a web page.

        Args:
            row (int): The row number to fetch bot password from the database.
        """
        try:
            bot_email_password = self.fetch_bot_password(row)
            if bot_email_password:
                self.interact_with_password_inputs(bot_email_password)

        except Exception as e:
            logging.error("An error occurred during bot password fetching and interaction:\n%s", e)

    def click_submit_button(self) -> None:
        """Clicks the submit button on the web page.
        
            This function finds the submit button element by CSS selector and clicks on it.
        
            Raises:
                NoSuchElementException: If the button element is not found on the web page.
                Exception: If an unexpected error occurs while looking for the button.
        """
        try:
            button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            button.click()
            time.sleep(5)

        except NoSuchElementException as e:
            logging.error("Button not found with current CSS selector.\nError:\n%s", e)

        except Exception as e:
            logging.error("Something went wrong while looking for the button.\nError:\n%s", e)

    def bot_email_account_exists_and_equals_row_count(self, row_count):
        try:
            self.crsr = self.conn.cursor()
            self.crsr.execute("SELECT COUNT(bot_email) FROM bots;")
            number_of_existing_bot_emails = self.crsr.fetchone()[0]

            if number_of_existing_bot_emails != row_count:
                return False
            
            return True

        except Exception as e:
            logging.error("Unable to access database.\nError:\n%s", e)

    def confirm_at_next_page(self):
        try:
            wait = WebDriverWait(self.driver, 10000)

            notification_content = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "notification--error")))
            if notification_content:
                print("Found the notification")

            else:
                print("We did not find the notification")

            
        except NoSuchElementException as e:
            logging.info("Captcha page not found")

    def solve_captcha(self):
        solved = input("Type y when you solve the captcha")
        if solved == 'y':
            print("captcha solved")

    def click_maybe_later(self):
        wait = WebDriverWait(self.driver, 10)
        
        try:
            button = wait.until(EC.element_to_be_clickable(By.CLASS_NAME, 'button-ghost-norm'))
            button.click()
            time.sleep(5)

        except NoSuchElementException as e:
            logging.error("Button not found with current CSS selector.\nError:\n%s", e)

        except Exception as e:
            logging.error("Something went wrong while looking for the button.\nError:\n%s", e)

    def number_of_name_rows(self):
        row_count = 0
        for row in open("src/bots/config/names.txt"):
            row_count += 1
        return row_count
    
    def store_email_in_db(self, row, email_header):
        try:
            self.crsr = self.conn.cursor()

            try:
                bot_email = str(email_header) + '@proton.me'
                self.crsr.execute(f"UPDATE bots SET bot_email = '{bot_email}' WHERE bot_id = {row + 1}")
                
            except Exception as e:
                logging.error("Problem updating table.\nError:\n%s", e)

        except Exception as e:
            logging.error("Problem creating a cursor object.\nError:\n%s", e)

    def execute(self):
        row_count = self.number_of_name_rows()
        bot_email_account_exists = self.bot_email_account_exists_and_equals_row_count(row_count)
        if not bot_email_account_exists:
            # Check if bot_email is empty for any entry in the database
            self.crsr = self.conn.cursor()
            self.crsr.execute("SELECT bot_email FROM bots WHERE bot_email IS NULL OR bot_email = ''")
            empty_emails_exist = self.crsr.fetchone()
            print(empty_emails_exist)
            # If there are no empty bot_email entries, proceed with the loop
            if not empty_emails_exist:
                for i in range(row_count):
                    self.access_proton_mail()
                    self.click_create_account()
                    self.click_get_proton_free()
                    email_header = self.fetch_bot_email_header(row=i)
                    self.interact_with_username_input(email_header)
                    self.fetch_bot_email_header_and_interact(row=i)
                    self.fetch_bot_password_and_interact(row=i)
                    self.click_submit_button()
                    self.confirm_at_next_page()
                    self.solve_captcha()
                    self.click_submit_button()
                    self.click_maybe_later()
                    self.store_email_in_db(row=i, email_header=email_header) # Maybe make this a bot manager task?
                    i += 1
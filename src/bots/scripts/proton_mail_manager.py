from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from ...database.scripts.connect_to_db import connect
from .bot_credentials_manager import BotCredentialsManager
from .sms_to_me import SMSToMe
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import logging
import time
import random

class Proton:
    def __init__(self):
        self.driver_path = 'chromedriver-win64/chromedriver.exe'
        self.driver = self.initialize_webdriver()
        self.conn, self.crsr = connect()
        self.wait = WebDriverWait(self.driver, 5)

        # Create an instance of the BotCredentialsManager
        sms_object = SMSToMe()

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

    def find_bots_in_db_without_email(self):
        """Find bots in the database without an email address.
        
        Returns:
            list: A list of bots without an email address.
        """
        self.crsr.execute("SELECT * FROM bots WHERE bot_email IS NULL ORDER BY bot_id")
        bots_without_email = self.crsr.fetchall()
        return bots_without_email

    def access_proton_mail(self):
        """Accesses the ProtonMail website using the Selenium driver.
        
            This function navigates to the ProtonMail website by accessing the URL 
            "https://account.proton.me/mail/signup?plan=free&billing=12&minimumCycle=12&currency=USD" 
            using the Selenium driver provided as a parameter.
        
            Raises:
                Exception: If there is an error accessing the ProtonMail website, it will log the error using the logging module.
        
            Returns:
                None
        """
        try:
            self.driver.get("https://account.proton.me/mail/signup?plan=free&billing=12&minimumCycle=12&currency=USD")
        
        except Exception as e:
            logging.error(f"Cannot access proton mail:\nError:\n{e}")

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
            username_iframe = wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="Username"]')))
            self.driver.switch_to.frame(username_iframe)

            try:
                username_input = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'email-input-field')))
                username_input.clear()
                username_input.send_keys(email_header)
            except NoSuchElementException:
                logging.error("Input field not found within iframe.")
            except Exception as e:
                logging.error("Error while interacting with input field within iframe:\n%s", e)
            finally:
                # Switch to default frame
                self.driver.switch_to.default_content()
        
        except TimeoutException:
            logging.error("Timeout waiting for the username iframe.")
        except Exception as e:
            logging.error("Error occurred while trying to switch to the username iframe:\n%s", e)


    def interact_with_password_inputs(self, bot_email_password):
        """Interact with password input fields on a web page.

        Args:
            bot_email_password (str): The bot email password to input into the password fields.

        Raises:
            NoSuchElementException: If the password input fields are not found on the web page.
            Exception: If an unexpected error occurs while interacting with the input fields.
        """

        wait = WebDriverWait(self.driver, 10)
        
        try:
            password_input_field = wait.until(EC.element_to_be_clickable((By.ID, 'password')))  # Locate password input field
            password_input_field.clear()  # Clear the current password field
            password_input_field.send_keys(bot_email_password)  # Type in the bot password to the input field
            repeat_password_input_field = self.driver.find_element(By.ID, 'repeat-password')  # Do the same for the repeat password section
            repeat_password_input_field.send_keys(bot_email_password)  # ..

        except NoSuchElementException as e:
            logging.error("Password input fields not found on the web page:\n%s", e)

        except Exception as e:
            logging.error("Error occurred while interacting with password input fields:\n%s", e)

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

    def handle_verification(self):
        try:
            # Attempt to handle case where proton asks for an email verification
            get_verification_code_button = self.driver.find_element(By.XPATH, "//button[text()='Get verification code']")
            if get_verification_code_button:
                print("Found verification code button")
                return True

        except Exception as e:
            print(f"Error finding verification button {e}")

        return False
    
    def handle_captcha(self):
        """Handles CAPTCHA verification process.
        
            This function waits for the CAPTCHA text to be present in the element, prompts the user to complete the CAPTCHA, 
            switches to the necessary iframes, and clicks the Next button on the CAPTCHA page.
        
            Returns:
                bool: True if CAPTCHA handling is successful, False otherwise.
        """
        try:
            
            # Wait for the CAPTCHA text
            captcha_text_element = self.wait.until(
                EC.text_to_be_present_in_element((By.XPATH, "//span[text()='CAPTCHA']"), "CAPTCHA")
            )

            if captcha_text_element:
                response = input("Type 'y' when you complete the CAPTCHA:\n").lower()
                if response == 'y':
                    # Switch to the parent iframe
                    parent_iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="Captcha"]')))
                    self.driver.switch_to.frame(parent_iframe)

                    print("switched to parent frame")

                    # Wait for the nested iframe to be present
                    nested_iframe = self.wait.until(EC.presence_of_element_located((By.NAME, "pcaptcha")))
                    self.driver.switch_to.frame(nested_iframe)

                    print("switched to nested frame")

                    # Locate and click the Next button on the CAPTCHA page
                    next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']")))
                    next_button.click()

                    return True  # CAPTCHA handling successful
                
        except NoSuchElementException as e:
            print(f"Error: {e}. Element not found")

        except TimeoutException:
            print("Timeout occurred while waiting for an element.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return False  # CAPTCHA handling failed
    
    def username_already_used(self):
        try:
            # Wait for the notification to appear
            username_already_used_notification = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "notification__content")))

            if username_already_used_notification:
                print("Notification found")

                # Wait for the notification to disappear
                self.wait.until_not(EC.visibility_of_element_located((By.CLASS_NAME, "notification_content")))
                
                # Add additional logic here if needed
                
                return True  # Notification handled successfully

        except TimeoutException:
            print("Notification did not appear within the expected time.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return False  # Notification handling failed

    
    def handle_verification_or_captcha(self):
        """
        Handles both captcha and email verification pages.

        This method first attempts to handle a captcha page, and if none is found,
        it proceeds to handle an email verification page.

        Returns:
            bool: True if captcha or verification page is successfully handled, False otherwise.
        """
        captcha_found = self.handle_captcha()

        if not captcha_found:
            verification_handled = self.handle_verification()
            if not verification_handled:
                print("Neither captcha nor verification page found.")
            return verification_handled

        return True  # Captcha page handled successfully




    def execute_account_creation(self):
        # Only process entries in the database without an email address
        bots_without_email = self.find_bots_in_db_without_email()
        
        for bot_without_email in bots_without_email:
            try:
                # Access the ProtonMail website
                self.access_proton_mail()

                # Extract bot information
                bot_id = int(bot_without_email[0])
                email_header = str(bot_without_email[3])
                bot_email_password = bot_without_email[-2]

                # Interact with the username input
                self.interact_with_username_input(email_header=email_header)

                # Interact with the password input
                self.interact_with_password_inputs(bot_email_password=bot_email_password)

                # Click the submit button
                self.click_submit_button()

                # Check if the username is already used
                if self.username_already_used():
                    # Change the email header
                    random_trailing_numbers = random.randint(10000, 99999)
                    new_email_header = email_header.replace(email_header[-5:], str(random_trailing_numbers))

                    # Update the database with the new email header
                    self.crsr.execute(
                        f"UPDATE bots SET bot_email_header = '{new_email_header}' WHERE bot_id = {bot_id};"
                    )
                    self.conn.commit()
                    print(f"Bot header changed from {email_header} to {new_email_header}")

                    # Restart the process by continuing to the next iteration
                    continue

                # Handle the captcha or verification page
                self.handle_verification_or_captcha()

                # Click submit button to confirm display name
                self.click_submit_button()

                # Handle phone number

                # Wait for some time before proceeding to the next iteration
                time.sleep(10000)

            except Exception as e:
                print(f"Could not create proton account for {bot_without_email}.\nError:\n{e}")

            finally:
                # Close the webdriver and create a new session
                self.driver.quit()
                self.driver = self.initialize_webdriver()

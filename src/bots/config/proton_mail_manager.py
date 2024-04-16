from ...database.scripts.connect_to_db import connect
from ...scout.scout import Scout
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import logging
import time

class Proton:
    def __init__(self):
        self.scout = Scout()
        self.driver_path = 'chromedriver-win64/chromedriver.exe'
        self.conn, self.crsr = connect()
        self.driver = self.scout.initialize_webdriver()
        self.wait = WebDriverWait(self.driver, 5)

    def find_bots_in_db_without_email(self):
        """Find bots in the database without an email address.
        
        Returns:
            list: A list of bots without an email address.
        """
        self.crsr.execute("SELECT * FROM bots WHERE bot_email IS NULL")
        bots_without_email = self.crsr.fetchall()
        return bots_without_email

    def access_proton_mail(self):
        """Accesses the ProtonMail website using the Selenium driver.
        
            This function navigates to the ProtonMail website by accessing the URL "https://account.proton.me/mail/signup?plan=free&billing=12&minimumCycle=12&currency=USD" using the Selenium driver provided as a parameter.
        
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
            time.sleep(10)
            username_iframe = wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="Username"]')))
            self.driver.switch_to.frame(username_iframe)

            try:
                username_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'email-input-field')))
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
            time.sleep(5)
            password_input_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
            password_input_field.send_keys(bot_email_password)

            repeat_password_input_field = self.driver.find_element(By.ID, 'repeat-password')
            repeat_password_input_field.send_keys(bot_email_password)

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


    def execute_account_creation(self):
        # Only make an email address for empty entries in the database
        bots_without_email = self.find_bots_in_db_without_email()
        
        for bot_without_email in bots_without_email:

            # Access proton mail website
            self.access_proton_mail()

            try:
                # Try to use the original email header to create an account.
                # If that doesn't work, generate a new email header.

                # Fetch original email header

                email_header = bot_without_email[3]

                print(f"Creating account with header {email_header}")

                # Interact with username input

                self.interact_with_username_input(email_header=email_header)

                # Fetch generate password

                bot_email_password = bot_without_email[-2]

                # Interact with password input

                self.interact_with_password_inputs(bot_email_password=bot_email_password)

                # Click Submit button

                self.click_submit_button()

                time.sleep(2)

            except Exception as e:
                print(f"Could not create proton account for {bot_without_email}.\nError:\n{e}")

            finally:
                # Close webdriver and create a new session
                self.driver.quit()
                self.driver = self.scout.initialize_webdriver()
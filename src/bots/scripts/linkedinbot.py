"""
Module Description:

This module contains classes for managing various aspects of web scraping and database 
interaction in the context of LinkedIn profiles. Each class is designed to handle specific tasks 
such as sign-in functionality, profile interaction, data extraction, and database updates.

Classes:
- BaseManager:
    Base class for managing WebDriver and DatabaseManager instances.
- LinkedInSignInManager:
    Manages sign-in functionality for LinkedIn accounts.
- UserProfileInteractor:
    Interacts with user profiles, retrieves profile URLs, and visits profiles.
- MainUserPageScraper:
    Scrapes data from the main user page, including name and location.
- ExperiencesManager:
    Handles experience extraction and database updates from user profiles.
- SkillsManager:
    Handles skills extraction and database updates from user profiles.
- LinkedInBot:
    Handles instances of LinkedIn bots.

Each class provides detailed docstrings describing its purpose, attributes, and methods.

Author:
    Danny Brown

Date:
    April 30, 2024

Version:
    0.1-dev
"""
# pylint: disable=too-many-lines

import logging
import random
import time
from typing import Union, Tuple, Optional, Dict, Set, List

import psycopg2
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, WebDriverException,
    StaleElementReferenceException, ElementNotInteractableException)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from src.database.scripts.database_manager import DatabaseManager  # pylint: disable=import-error
from .webdriver_manager import WebDriverManager

class BaseManager:  # pylint: disable=too-few-public-methods
    """
    Base class for managing WebDriver and DatabaseManager instances.

    This class provides common initialization logic for classes that need to
    interact with WebDriver and a database.

    Args:
        webdriver_manager (WebDriverManager):
            The WebDriverManager instance responsible for managing WebDriver operations.
        database_manager (DatabaseManager):
            The DatabaseManager instance for interacting with the database.

    Attributes:
        webdriver_manager (WebDriverManager):
            The WebDriverManager instance responsible for managing WebDriver operations.
        driver (WebDriver):
            The WebDriver instance used for web automation.
        wait (WebDriverWait):
            The WebDriverWait instance used for waiting for elements.
        database_manager (DatabaseManager):
            The DatabaseManager instance for interacting with the database.

    """
    def __init__(
            self, webdriver_manager: WebDriverManager,
            database_manager: DatabaseManager) -> None:
        """
        Initializes a BaseManager object with the provided 
        WebDriverManager and DatabaseManager instances.

        Args:
            webdriver_manager (WebDriverManager):
                The WebDriverManager instance responsible for managing WebDriver operations.
            database_manager (DatabaseManager):
                The DatabaseManager instance for interacting with the database.

        Returns:
            None

        Raises:
            None
        """
        # WebDriver
        self.webdriver_manager = webdriver_manager
        self.driver = webdriver_manager.driver
        self.wait = webdriver_manager.wait

        # Database
        self.database_manager = database_manager

class LinkedInSignInManager(BaseManager):
    """
    A class responsible for managing sign-in functionality for LinkedIn.

    This class provides methods to interact with the LinkedIn website,
    including accessing the website, clicking the sign-in button,
    retrieving user credentials from the database, and handling captchas.

    Attributes:
        driver (WebDriver):
            The WebDriver instance for interacting with the web browser.
        wait (WebDriverWait):
            The WebDriverWait instance for waiting for page elements.
        database_manager (DatabaseManager):
            The DatabaseManager instance for database interactions.

    Methods:
        access_linkedin:
            Accesses the LinkedIn website using the WebDriver.
        click_sign_in:
            Clicks the sign-in button on the LinkedIn login page.
        fetch_email_from_database:
            Retrieves the user's email from the database.
        type_email_in_linkedin_login:
            Enters the user's email into the LinkedIn login form.
        fetch_password_from_database:
            Retrieves the user's password from the database.
        type_password_in_linkedin_login:
            Enters the user's password into the LinkedIn login form.
        locate_and_click_signin_button:
            Locates and clicks the sign-in button on the login screen.
        click_login_signin_button_with_retry:
            Clicks the sign-in button with retry logic.
        handle_captcha:
            Handles the captcha verification process.
    """

    def __init__(
            self, webdriver_manager: WebDriverManager,
            database_manager: DatabaseManager, bot_id: int):
        """
        Initializes a new instance of the class.

        Args:
            webdriver_manager (WebDriverManager): 
                The WebDriverManager instance responsible 
                for managing the WebDriver configuration.
            database_manager (DatabaseManager):
                The DatabaseManager instance responsible
                for managing database interactions.
            bot_id (int): 
                The unique identifier for the bot.

        Attributes:
            bot_id (int): 
                The unique identifier for the bot.
        """
        super().__init__(webdriver_manager, database_manager)
        self.bot_id = bot_id

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
            self.driver.get("https://www.linkedin.com/")  # pylint: disable=no-member

        except WebDriverException as driver_error:
            # Log and raise any error related to the WebDriver
            error_message = (
                "A WebDriver-related error occurred while "
                "trying to connect to LinkedIn."
            )
            logging.critical(error_message, exc_info=True)
            raise driver_error

        except Exception as unexpected_error:
            # Log and raise any unexpected errors
            logging.critical(
                "An error occurred while trying to get to LinkedIn.", exc_info=True)
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
            class_name = (
                "nav__button-secondary.btn-md.btn-secondary-emphasis"
            )
            # pylint: disable=no-member
            sign_in_button = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            )

            # Log a message indicating successful sign-in button detection
            logging.info("Successfully located the sign-in button.")

            # Click the sign-in button
            sign_in_button.click()

        except NoSuchElementException:
            # Log and raise a critical error if the sign-in button cannot be located
            logging.critical(
                "Failed to locate the sign-in button.", exc_info=True)
            raise

        except ElementNotInteractableException:
            # Log and raise a critical error if the sign-in button cannot be located
            critical_message = (
                "Failed to click the sign in button"
                " as this element is not interactable."
            )
            logging.critical(critical_message, exc_info=True)
            raise

        except Exception:
            # Log and raise a critical error if an unexpected error occurs
            error_message = (
                "An unexpected error occurred while locating the sign-in button."
            )
            logging.critical(error_message, exc_info=True)
            raise

    def _fetch_email_from_database(self, bot_id: int) -> str:
        """Fetches the email associated with the provided bot_id from the database.

        Args:
            bot_id (int): The unique identifier of the bot.

        Raises:
            psycopg2.Error: If there is an error while fetching the email from the database.
            Exception: If an unexpected error occurs during the process.

        Returns:
            email (str): The email associated with the provided bot_id.
        """
        try:
            # Define query arguments
            query = "SELECT bot_email FROM bots WHERE bot_id = %s"
            params = (bot_id,)
            fetch = "ONE"

            # Retrieve email from database for corresponding bot ID then store as a variable
            email = self.database_manager.execute_query(
                query=query, params=params, fetch=fetch)[0]

            # Log a message indicating the successful retrieval of the email from the database
            info_message = (
                f"Successfully retrieved email {email} from the database."
            )
            logging.info(info_message)

            return email

        except psycopg2.Error as db_error:
            # Log a database error if the email cannot be retrieved
            logging.critical(
                "Failed to fetch email from the database.", exc_info=True)
            raise db_error

        except Exception as unexpected_error:
            # Log and raise critical error if an unexpected error if any other exception occurs
            error_message = (
                "An unexpected error occurred."
            )
            logging.critical(error_message, exc_info=True)
            raise unexpected_error

    def type_email_in_linkedin_login(self, bot_id: int) -> None:
        """Types the fetched email into the email input field on the LinkedIn login screen.

        Args:
            bot_id (int): The unique identifier of the bot.

        Raises:
            NoSuchElementException: If the username input 
            field on the LinkedIn login screen is not found.

            Exception: If an unexpected error occurs during the process.

        Returns:
            None
        """
        try:
            # Fetch email from the database
            email = self._fetch_email_from_database(bot_id)

            # Locate the username input on the LinkedIn login screen
            email_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )

            # Type the email into the login input field
            email_input.send_keys(email)

            # Log a message indicating the successful location of the email input
            logging.info("Successfully typed email into the input field.")

        except NoSuchElementException:
            # Log and raise critical error if the username input is not found.
            error_message = (
                "Failed to locate the username input "
                "on the LinkedIn login screen."
            )
            logging.critical(error_message, exc_info=True)
            raise

        except Exception as unexpected_error:
            # Log and raise critical error if an unexpected error if any other exception occurs
            error_message = "An unexpected error occurred."
            logging.critical(error_message, exc_info=True)
            raise unexpected_error

    def _fetch_password_from_database(self, bot_id: int) -> str:
        """Fetches the password associated with the provided bot_id from the database.

        Args:
            bot_id (int): The unique identifier of the bot.

        Raises:
            psycopg2.Error: If there is an error with the database connection or query.
            Exception: For any other unexpected errors.

        Returns:
            str: The password associated with the provided bot_id.
        """
        try:
            # Define query arguments
            query = "SELECT bot_email_password FROM bots WHERE bot_id = %s"
            params = (bot_id,)
            fetch = "ONE"

            # Fetch bot password from the database with a corresponding bot_id
            password = self.database_manager.execute_query(
                query=query, params=params, fetch=fetch)

            # Log the successful retrieval of the password from the database
            info_message = (
                f"Successfully retrieved the LinkedIn password "
                f"{password} from the database."
            )

            logging.info(info_message)

            return password

        except psycopg2.Error:
            # Log and raise critical database error if the query failed
            logging.critical(
                "Failed to fetch LinkedIn password from the database.", exc_info=True)
            raise

        except Exception as unexpected_error:
            # Log and raise a critical unexpected error.
            logging.critical("An unexpected error occurred.", exc_info=True)
            raise unexpected_error

    def type_password_in_linkedin_login(self, bot_id: int) -> None:
        """Type the fetched password into the password input field on the LinkedIn login screen.

        Args:
            bot_id (int): The unique identifier of the bot whose password needs to be typed.

        Raises:
            NoSuchElementException: If the password input field 
            cannot be located on the LinkedIn login screen.
            Exception: For any other unexpected errors.

        Returns:
            None
        """
        try:
            # Fetch password from the database
            password = self._fetch_password_from_database(bot_id)

            # Locate the password form
            password_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "password"))
            )

            # Type the password
            password_input.send_keys(password)

            # Log a message indicating the successful typing of the password into the input field
            logging.info("Successfully typed password in the password input")

        except NoSuchElementException:
            # Log and raise a critical WebDriver error if
            # the password input was unable to be located.
            error_message = (
                "Failed to locate the password input "
                "field on the LinkedIn login screen."
            )
            logging.critical(error_message, exc_info=True)
            raise

        except Exception as unexpected_error:
            # Log and raise a critical unexpected error.
            logging.critical("An unexpected error occurred.", exc_info=True)
            raise unexpected_error

    def locate_and_click_signin_button(self) -> None:
        """
        Locates and clicks the sign-in button on the login screen.

        Raises:
            NoSuchElementException: If the sign-in button element is not found on the page.
        """
        try:
            # Locate the sign-in button
            sign_in_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[@type="submit"]'))
            )

            # Log a message indicating the successful location of the sign-in button
            logging.info("Sign-in button located on the login screen.")

            # Click the sign-in button
            sign_in_button.click()

        except NoSuchElementException:
            # Raise and log a critical error if the sign-in button is not found
            logging.critical(
                "Could not find the sign-in button.", exc_info=True)
            raise

    def click_signin_button_with_retry(self, max_retries: int = 3,
                                             initial_delay: int = 1) -> None:
        """
        Attempts to click the sign-in button with retry mechanism.
    
        Args:
            max_retries (int): The maximum number of retry attempts (default is 3).
            initial_delay (int): The initial delay in seconds between retry attempts (default is 1).
    
        Raises:
            RuntimeError: If the maximum number of retries is reached without successful click.
    
        Returns:
            None
        """
        for retry in range(max_retries):
            try:
                # Attempt to locate and click the sign-in button
                self.locate_and_click_signin_button()
                # Exit the loop if the click was successful
                break
            except NoSuchElementException:
                # Log the retry attempt
                error_message = (
                    f"Retry attempt {retry + 1}/{max_retries}. "
                    f"Retrying in {initial_delay} seconds.")

                logging.error(error_message)
                time.sleep(initial_delay)
        else:
            # Log and raise a critical error if the maximum number of retries is reached
            logging.critical("Maximum retries reached.", exc_info=True)
            raise RuntimeError("Maximum number of retries reached. "
                               "Unable to click sign-in button.")

    def handle_captcha(self) -> None:
        """
        Get's user input on if a captcha was solved

        Returns:
            None
        """

        is_captcha_solved = input("Type y when you solve the captcha:\n")

        if is_captcha_solved == 'y':
            pass

    def sign_in_wrapper(self, bot_id) -> None:
        """
        Sign in the bot with the given bot_id.
    
        Args:
            self: The object itself.
            bot_id (int): The ID of the bot to sign in.
    
        Returns:
            None
        """
        # Access the LinkedIn website
        self.access_linkedin()

        # Click the sign-in button
        self.click_sign_in()

        # Fetch and type email into the login form
        self.type_email_in_linkedin_login(bot_id=bot_id)

        # Fetch and type password into the password form
        self.type_password_in_linkedin_login(bot_id=bot_id)

        # Click sign in (handle retries)
        self.click_signin_button_with_retry()

        # Handle the captcha
        self.handle_captcha()

class UserProfileInteractor(BaseManager):
    """
    A class responsible for interacting with user profiles.

    This class provides methods to retrieve profile URLs of users from a database
    and visit individual user profiles using a WebDriver instance.

    Attributes:
        driver (WebDriver):
            The WebDriver instance for interacting with the web browser.
        database_manager (DatabaseManager):
            The DatabaseManager instance for database interactions.

    Methods:
        get_profile_urls:
            Retrieves the profile URLs of users from the database based on 
            the provided bot ID and number of users per bot.
        visit_user:
            Visits the user's profile by navigating to the provided profile URL.
    """

    def __init__(
            self, webdriver_manager: WebDriverManager,
            database_manager: DatabaseManager, bot_id: int):
        """
        Initializes a new instance of the class.

        Args:
            webdriver_manager (WebDriverManager): 
                The WebDriverManager instance responsible 
                for managing the WebDriver configuration.
            database_manager (DatabaseManager):
                The DatabaseManager instance responsible
                for managing database interactions.
            bot_id (int): 
                The unique identifier for the bot.

        Attributes:
            bot_id (int): 
                The unique identifier for the bot.
        """
        super().__init__(webdriver_manager, database_manager)
        self.bot_id = bot_id

    def get_profile_urls(self, number_of_users_per_bot: int = 20) -> list:
        """
        Retrieves the profile URLs of users from the database based on the 
        provided bot ID and number of users per bot.

        Args:
            bot_id (int):
                The ID of the bot for which profile URLs are to be retrieved.
            number_of_users_per_bot (int, optional):
                The number of users per bot. Default is 20.

        Returns:
            list:
                A list containing the profile URLs of users within 
                the specified range for the given bot ID.
        """
        # Create query
        query = "SELECT profile_url FROM users WHERE user_id BETWEEN %s AND %s ORDER BY user_id;"

        # Calculate parameter values
        starting_index = 1
        start_user_id = (number_of_users_per_bot * (self.bot_id - 1)) + starting_index
        end_user_id = number_of_users_per_bot * self.bot_id

        # Query the database and store the urls in a list
        raw_profile_urls = self.database_manager.execute_query(
            query=query,
            params=(start_user_id, end_user_id),
            fetch="ALL"
        )

        # Extract urls from the tuples
        profile_urls = [url[0] for url in raw_profile_urls]

        return profile_urls


    def visit_user(self, profile_url: str) -> None:
        """
        Visits the user's profile by navigating to the provided profile URL.

        Args:
            profile_url (str): 
                The URL of the user's profile to visit.

        Raises:
            WebDriverException: 
                If a WebDriver related error occurs 
                while trying to access the user's profile.
            Exception: 
                If an unexpected error occurs while 
                attempting to visit the user's profile.
        """
        try:
            self.driver.get(f"{profile_url}")

        except WebDriverException:
            # Log and raise critical WebDriver exception for a driver related error
            error_message = (
                f"A WebDriver related error occurred while trying to "
                f"access the user's profile. Link:\n{profile_url}"
            )
            logging.critical(error_message, exc_info=True)
            raise

        except Exception:
            # Log and raise a critical error if an unexpected error occurred
            error_message = (
                f"An unexpected error occurred while "
                f"attempting to visit the user's profile. "
                f"Link:\n{profile_url}"
            )

            logging.critical(error_message)
            raise

class MainUserPageScraper(BaseManager):
    """
    A class responsible for scraping data from the main user page.

    This class provides methods to interact with the main user page of a website,
    including finding the user's name, extracting their current location, and updating
    the database with the retrieved information.

    Attributes:
        webdriver_manager (WebDriverManager): 
            The WebDriverManager instance responsible for managing the WebDriver configuration.
        driver (WebDriver): 
            The WebDriver instance for interacting with the web browser.
        wait (WebDriverWait): 
            The WebDriverWait instance for waiting for page elements.
        database_manager (DatabaseManager): 
            The DatabaseManager instance for database interactions.
        bot_id (int): 
            The unique identifier for the bot.

    Methods:
        find_users_name():
            Find the user's name on their profile.
        send_names_to_db(users_name: str, profile_url: str):
            Update the database with the given user's name and profile URL.
        extract_current_location():
            Extracts the current location of the user.
        update_location_in_db(users_location: str, profile_url: str):
            Update the location of a user in the database.
    """
    def __init__(
            self, webdriver_manager: WebDriverManager,
            database_manager: DatabaseManager, bot_id: int):
        """
        Initializes a new instance of the class.

        Args:
            webdriver_manager (WebDriverManager): 
                The WebDriverManager instance responsible 
                for managing the WebDriver configuration.
            database_manager (DatabaseManager):
                The DatabaseManager instance responsible
                for managing database interactions.
            bot_id (int): 
                The unique identifier for the bot.

        Attributes:
            bot_id (int): 
                The unique identifier for the bot.
        """
        super().__init__(webdriver_manager, database_manager)
        self.bot_id = bot_id

    def find_users_name(self) -> Union[str, None]:
        """
        Find the user's name on their profile.

        Returns:
            str: The user's name if found, None otherwise.
        """
        try:
            # Locate the name on the user's profile
            users_name = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h1.text-heading-xlarge"))
            ).text

            return users_name

        except TimeoutException:
            # Log and handle timeout exception
            logging.error("Could not locate user's name due to timeout.")
            return None

        except NoSuchElementException:
            # Log and handle element not found exception
            logging.error(
                "Could not locate the element containing "
                "the user's name on their profile."
            )
            return None

    def extract_current_location(self) -> Union[str, None]:
        """
        Extracts the current location of the user.

        This function locates the span element that contains the user's location on the webpage.

        Returns:
            str: 
                The user's location.
            None: 
                If unable to locate the user's location due to a timeout, 
                missing element, or unexpected error.
        """
        try:
            # Locate the span element that contains the user's location
            location_xpath = (
                '//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]'
                '/div[2]/div[2]/div[2]/span[1]'
            )
            users_location = self.wait.until(
                EC.presence_of_element_located((By.XPATH, location_xpath))
            ).text

            return users_location

        except TimeoutException:
            # Log and handle a timeout error
            error_message = (
                "Timeout error occurred while attempting to find the "
                "HTML element containing the user's location."
            )
            logging.error(error_message)
            return None

        except NoSuchElementException as e:
            # Log and handle NoSuchElement exception
            error_message = (
                "Could not locate the HTML element "
                "containing the user's name."
            )

            logging.error(error_message, e)

            return None

        except StaleElementReferenceException as e:
            # Log and handle StaleElementReferenceException
            error_message = (
                "The referenced element is no longer present in the DOM."
            )

            logging.error(error_message, e)

            return None

    def main_user_page_scraper_wrapper(self, profile_url):
        """
        Wrapper method for scraping data from a user's main page.

        This method orchestrates the process of extracting the user's name and location
        from their main page and updating the database with the retrieved information.

        Args:
            profile_url (str):
                The URL of the user's main page.

        Returns:
            None
        """
        # Extract the name from the user's main page
        users_name = self.find_users_name()

        # Send the user's name to the database
        self.database_manager.send_names_to_db(
            users_name=users_name, profile_url=profile_url
        )

        # Extract the location from the user's main page
        location = self.extract_current_location()

        # Update the database with the user's location
        self.database_manager.update_location_in_db(
            users_location=location, profile_url=profile_url
        )

class ExperienceManager(BaseManager):  # pylint: disable=too-few-public-methods
    """
    A class for managing and scraping user experiences from LinkedIn profiles.

    This class provides functionality to scrape and store user experiences from
    LinkedIn profiles. It utilizes a WebDriverManager for web scraping and a
    DatabaseManager for storing the extracted data.

    Args:
        webdriver_manager (WebDriverManager): 
            The WebDriverManager instance responsible 
            for managing the WebDriver configuration.
        database_manager (DatabaseManager):
            The DatabaseManager instance responsible
            for managing database interactions.
        user_id (int): 
            The unique identifier for the user.

    Attributes:
        user_id (int): 
            The unique identifier for the user.

    Methods:
        _locate_show_all_experiences_button(self) -> Optional[str]:
            Locate and return the href attribute of the 'Show all experiences' 
            button on the page.

        _locate_list_elements_in_new_page(self) -> Optional[list]:
            Locates and returns a list of elements on a new page.

        _locate_work_experience_elements_for_multiple_positions(
                self, list_elements: list) -> list:
            Locate work experience elements within a list of elements.

        _extract_work_experience_data_for_multiple_positions(
                self, work_experience_elements: list) -> Dict[str, str]:
            Extract work experience data from a list of work experience elements.

        _locate_and_extract_work_experience(
                self, list_elements: list) -> Dict[str, str]:
            Locate and extract work experience data from a list of elements.

        _scrape_and_store_experiences_from_new_page(self, user_id: int) -> None:
            Scrape and update work experiences for a user on a new page.

        _locate_experience_container(self) -> Optional[WebElement]:
            Locates the main container div element ('#experience') on the original page.

        _extract_work_experiences(self, sibling_div: WebElement) -> Dict[str, str]:
            Extracts information about work experiences from the provided sibling div.

        _extract_company_and_job_title(self, list_item: Optional[WebElement]) -> Tuple[str, str]:
            Parses and extracts company name and job title from the provided list item.

        _scrape_and_store_experiences_from_original_page(self) -> dict:
            Locates and extracts work experiences from the original page.

        _update_work_experience_in_database(
                self, work_experience_dictionary: Dict[str, str]) -> None:
            Update the work experience information in the database.

        experiences_wrapper(self, user_id: int) -> None:
            Wrapper method for scraping and storing user experiences from LinkedIn.
    """

    def _locate_show_all_experiences_button(self) -> Optional[str]:
        """
        Locate and return the href attribute of the 'Show all experiences' button on the page.
        
        Returns:
            str: The href attribute of the button if found, None otherwise.
        """
        try:
            # Wait for the presence of at least one matching element
            button_xpath = (
                "//a[contains(span[@class='pvs-navigation__text'], 'Show all')"
                " and contains(span[@class='pvs-navigation__text'], 'experiences')]"
            )

            buttons = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, button_xpath))
            )

            # Iterate through each button
            for button in buttons:
                # Check if the button's href attribute contains the LinkedIn domain
                href = button.get_attribute("href")
                if href and 'linkedin.com' in href:
                    return href

        except NoSuchElementException:
            error_message = "The button could not be found"
            logging.error(error_message)

        return None
    # New page methods
    def _locate_list_elements_in_new_page(self) -> Optional[list]:
        """
        Locates and returns a list of elements on a new page.
    
        Returns:
            list: A list of elements located on the new page.
            None: If <li> tags aren't located on the new page.

        Raises:
            NoSuchElementException:
                If unable to locate the list elements on the new page.
            TimeoutException:
                If timed out while waiting for list elements to appear.
            StaleElementReferenceException:
                If encountered a stale element reference while locating elements.
            WebDriverException:
                If WebDriver encounters an exception during element location.
        """
        try:
            # Wait for all the list elements to load
            list_element_class = (
                "pvs-list__paged-list-item.artdeco-list__item."
                "pvs-list__item--line-separated.pvs-list__item--one-column"
            )
            list_elements = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, list_element_class))
            )

            return list_elements

        except NoSuchElementException as element_exception:
            logging.error("Could not locate the list elements. %s", element_exception)
            return None

        except TimeoutException as timeout_exception:
            logging.error("Timed out while waiting for list elements. %s", timeout_exception)
            return None

        except StaleElementReferenceException as stale_element_exception:
            logging.error("Stale element reference encountered. %s", stale_element_exception)
            return None

        except WebDriverException as webdriver_exception:
            logging.error("WebDriver encountered an exception. %s", webdriver_exception)
            return None

    def _locate_work_experience_elements_for_multiple_positions(
            self, list_elements: list) -> list:
        """
        Locate work experience elements within a list of elements.

        Args:
            list_elements (list): List of elements containing work experience information.

        Returns:
            list: List of elements representing work experience entries.
        """
        work_experience_elements = []
        for list_element in list_elements:
            anchor_tags_within_li_elements = list_element.find_elements(
                By.XPATH, ".//a[contains(@class, 'flex-column')]")
            if anchor_tags_within_li_elements:
                work_experience_elements.append(list_element)
        return work_experience_elements

    def _extract_work_experience_data_for_multiple_positions(
            self, work_experience_elements: list) -> Dict[str, str]:
        """
        Extract work experience data from a list of work experience elements.

        Args:
            work_experience_elements (list): 
                List of elements representing work experience entries.

        Returns:
            dict: A dictionary containing the extracted work experience data.
        """
        work_experience_dict = {}
        for list_element in work_experience_elements:
            company_name = list_element.find_element(
                By.XPATH, ".//span").text
            job_titles = list_element.find_elements(
                By.XPATH, ".//span[@aria-hidden='true']")
            company_jobs = [job.text for job in job_titles]
            work_experience_dict[company_name] = company_jobs
        return work_experience_dict

    def _locate_and_extract_work_experience(
            self, list_elements: list) -> Dict[str, str]:
        """
        Locate and extract work experience data from a list of elements.

        Args:
            list_elements (list): List of elements containing work experience information.

        Returns:
            dict: A dictionary containing the extracted work experience data.
        """
        work_experience_elements = self._locate_work_experience_elements_for_multiple_positions(
            list_elements
        )
        return self._extract_work_experience_data_for_multiple_positions(work_experience_elements)

    def _scrape_and_store_experiences_from_new_page(self, user_id):
        """
        Scrape and update work experiences for a user on a new page.

        This method simulates the scraping process by waiting for a random
        duration (between 3 to 6 seconds), locating list elements on the page,
        extracting work experience information, and updating the database with
        the extracted data.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            None
        """
        time.sleep(random.uniform(3, 6))
        self.webdriver_manager.scroll_down()

        list_elements = self._locate_list_elements_in_new_page()
        work_experience_dict = self._locate_and_extract_work_experience(list_elements=list_elements)
        self.database_manager.update_work_experience(
            work_experience=work_experience_dict, user_id=user_id
        )

        logging.info("Added %s to the database.", work_experience_dict)

    # Original Page methods
    def _locate_experience_container(self) -> Optional[WebElement]:
        """
        Locates the main container div element ('#experience') on the original page.

        Returns:
            WebElement: The main container div element if found, None otherwise.
        """
        return self.wait.until(
            EC.presence_of_element_located((By.ID, "experience"))
        )

    def _extract_work_experiences(self, sibling_div: WebElement) -> Dict[str, str]:
        """
        Extracts information about work experiences from the provided sibling div.

        Args:
            sibling_div (WebElement): The sibling div containing experience information.

        Returns:
            dict: A dictionary containing extracted work experiences.
        """
        work_experience = {}
        list_items = sibling_div.find_elements(By.XPATH, 'ul/li')

        for item in list_items:
            company_name, job_title = self._extract_company_and_job_title(item)
            work_experience[company_name] = job_title

        return work_experience

    def _extract_company_and_job_title(self, list_item: Optional[WebElement]) -> Tuple[str, str]:
        """
        Parses and extracts company name and job title from the provided list item.

        Args:
            list_item (WebElement): The list item containing company and job title information.

        Returns:
            tuple: A tuple containing company name and job title.
        """
        anchor_tags = list_item.find_elements(
            By.XPATH, ".//a[contains(@class, 'flex-column')]")
        if len(anchor_tags) > 2:
            names_list = [anchor.find_element(
                By.XPATH, ".//span").text for anchor in anchor_tags]
            company_name = names_list[0]
            jobs = names_list[1:]
            return company_name, jobs

        company = list_item.find_element(
            By.XPATH, "div/div/div/div/span/span[@aria-hidden='true']"
        ).text.split(' ·')[0]

        job_title = list_item.find_element(
            By.XPATH, "div/div/div/div/div/div/div/div/span[@aria-hidden='true']"
        ).text

        return company, job_title

    def _scrape_and_store_experiences_from_original_page(self) -> dict:
        """
        Locates and extracts work experiences from the original page.

        Returns:
            dict: A dictionary containing extracted work experiences.
        """
        # Locate the main div container element (#experience) on the original page
        experience_container = self._locate_experience_container()

        # Hop to the 2nd sibling div element
        sibling_div = experience_container.find_element(By.XPATH, './following-sibling::div[2]')

        # Create the work experiences dictionary
        work_experiences_dict = self._extract_work_experiences(sibling_div)

        # Store the work experineces dictionary into the database
        self._update_work_experience_in_database(work_experiences_dict)

    # Shared methods
    def _update_work_experience_in_database(
            self, work_experience_dictionary: Dict[str, str,]) -> None:
        """
        Update the work experience information in the database.

        Args:
            work_experience_dictionary (dict): 
                A dictionary containing the updated work experience information,
                where keys are company names and values are job titles.

        Returns:
            None
        """
        self.database_manager.update_work_experience(
            work_experience=work_experience_dictionary, user_id=self.get_user_id())

    def experiences_wrapper(self, user_id):
        """
        Wrapper method for scraping and storing user experiences from LinkedIn.

        This method acts as the entry point for users to interact with the class.
        It handles the logic for determining whether to scrape experiences from
        the original profile page or from the 'Show all experiences' page, based
        on the availability of the respective button. It then delegates the scraping
        and storing tasks to appropriate internal methods.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            None
        """

        # Locate the show all experiences button
        # If there is an href, continue with new page logic
        # If None, continue with original page logic

        button_href = self._locate_show_all_experiences_button()

        if button_href:
            # Visit new page
            self.driver.get(button_href)
            # Handle new page logic
            self._scrape_and_store_experiences_from_new_page(user_id=user_id)

        else:
            # Continue with original page logic
            self._scrape_and_store_experiences_from_original_page()

class SkillsManager(BaseManager):
    """
    A class for managing skills extraction and database updates from user profiles.

    This class provides methods to locate and extract skills from user profiles,
    update the database with the extracted skills, and handle the scraping process
    for both the original and new pages.

    Args:
        webdriver_manager (WebDriverManager):
            The WebDriverManager instance responsible for managing WebDriver operations.
        database_manager (DatabaseManager):
            The DatabaseManager instance for interacting with the database.

    Attributes:
        webdriver_manager (WebDriverManager):
            The WebDriverManager instance responsible for managing WebDriver operations.
        driver (WebDriver):
            The WebDriver instance used for web automation.
        wait (WebDriverWait):
            The WebDriverWait instance used for waiting for elements.
        database_manager (DatabaseManager):
            The DatabaseManager instance for interacting with the database.

    Methods:
        locate_skills_button():
            Locates the 'Show all skills' button on the page.
        navigate_to_new_page(button_href: Optional[str]) -> None:
            Navigates to the new skills page.
        create_skills_set(list_elements: List[str]) -> Set[str]:
            Creates a set of unique skills from the given list of elements.
        locate_skills_list_elements_in_new_page() -> Optional[List[WebElement]]:
            Locates and returns a list of WebElement elements on a new page.
        scrape_skills_on_new_page() -> Set[str]:
            Scrapes skills on a new page.
        scrape_skills_on_original_page() -> Set[str]:
            Scrapes skills from the original page.
        locate_skills_list_element_on_original_page() -> Set[str]:
            Locate skills list elements on the original page.
        scrape_skills() -> Set[str]:
            Scrapes skills from user profile.
        update_skills_database(skills_set: Set[str], user_id: int) -> None:
            Update the skills database with the provided skills set for a specific user.
        skills_wrapper(user_id: int) -> None:
            Generates skill set from user profile then updates the database.
    """
    def locate_skills_button(self) -> Optional[str]:
        """
        Locates the 'Show all skills' button on the page.

        This method finds and returns the href attribute of the 'Show all skills' button,
        ensuring that the button belongs to the LinkedIn domain.

        Returns:
            str or None: The href attribute of the button if found and belongs to LinkedIn domain,
                        None otherwise.

        Raises:
            NoSuchElementException: If the 'Show all skills' button could not be located.
            TimeoutException: If timed out while waiting for the 'Show all skills' button to appear.
        """
        try:
            # Wait for the presence of at least one matching element
            buttons_xpath = (
                "//a[contains(span[@class='pvs-navigation__text'], 'Show all')"
                " and contains(span[@class='pvs-navigation__text'], 'skills')]"
            )
            buttons = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, buttons_xpath)
                )
            )

            # Iterate through each button to find the one with LinkedIn domain
            for button in buttons:
                href = button.get_attribute("href")
                if href and 'linkedin.com' in href:
                    return href

        except NoSuchElementException as element_exception:
            logging.error(
                "The buttons could not be located. Check the XPATH. Error: %s", element_exception
            )

        except TimeoutException as timeout_exception:
            error_message = ("Timed out while waiting for the skills buttons to appear. "
                            "Error: %s")
            logging.error(error_message, timeout_exception)

        return False

    def navigate_to_new_page(self, button_href: Optional[str]) -> None:
        """
        Navigates to the new skills page
        """
        self.driver.get(button_href)

    def create_skills_set(self, list_elements: List[str]) -> Set[str]:
        """
        Create a set of unique skills from the given list of elements.
    
        Args:
            list_elements (List): A list of elements to extract skills from.
    
        Returns:
            Set: A set containing unique skills extracted from the list of elements.
        """
        skills_set = set()
        for i, list_element in enumerate(list_elements):
            print("index: ", i)
            # Attempt to locate the span text within the list element
            span_element = list_element.find_element(
                By.XPATH, "div/div/div/div/a/div/div/div/div/span[@aria-hidden='true']")
            if span_element:
                span_text = span_element.text
                if span_text != '':
                    skills_set.add(span_text)

        return skills_set

    def locate_skills_list_elements_in_new_page(self) -> Optional[List[WebElement]]:
        """
        Locates and returns a list of WebElement elements on a new page.
    
        Returns:
            Optional[List[WebElement]]: A list of WebElement elements found on the new page.
        """
        # Locate list elements
        list_elements = self.driver.find_elements(
            By.XPATH, '//li[contains(@class, "pvs-list__paged-list-item")]')
        return list_elements

    def scrape_skills_on_new_page(self):
        """
        Scrapes skills on a new page by pausing for a random amount of time, 
        scrolling down the page, locating list elements, creating a skills set, 
        and returning it.
        """
        # Pause for a random amount of time
        time.sleep(random.uniform(3, 6))

        # Scroll down the page
        self.webdriver_manager.scroll_down()

        # Locate the list elements
        list_elements = self.locate_skills_list_elements_in_new_page()

        # Create the skills set
        skills_set = self.create_skills_set(list_elements)

        return skills_set

    def scrape_skills_on_original_page(self):
        """Scrapes the skills from the original page.
        
            Returns:
                list: A list of skills scraped from the original page.
        """
        # Sleep for a random amount of time to avoid detection
        time.sleep(random.uniform(3, 6))

        # Scroll down
        self.webdriver_manager.scroll_down()

        # Generate a skills set if on the original page
        skills_set = self.locate_skills_list_element_on_original_page()

        return skills_set

    def locate_skills_list_element_on_original_page(self):
        """Locate skills list elements on the original page.
        
        This function locates the skills section on the original page and 
        extracts the list elements containing skills. 
        It returns a set of skills found on the page.
        
        Returns:
            set: A set of skills extracted from the page.
        """
        skills_set = set()
        # Locate the skills section
        skills_div = self.wait.until(
            EC.presence_of_element_located((By.ID, "skills"))
        )
        # Switch to sibling element
        sibling_div_tag = skills_div.find_element(
            By.XPATH, './following-sibling::div[2]')
        if sibling_div_tag:
            # Locate the list elements
            list_elements = sibling_div_tag.find_elements(
                By.XPATH, "ul/li[contains(@class, 'artdeco-list__item')]")
            for list_element in list_elements:
                # Look for anchor tags in each list element
                anchor_element = list_element.find_element(By.TAG_NAME, "a")
                # Locate the span tag within the anchor element tree
                span_tag = anchor_element.find_element(
                    By.XPATH, './/span[@aria-hidden="true"]')
                span_text = span_tag.text
                print(span_text)
                skills_set.add(span_text)
        else:
            print("could not find the sibling tag")

        return skills_set

    def scrape_skills(self):
        """Scrapes skills from user profile.
        
        Returns:
            set: A set of skills scraped from the webpage.
        """
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

    def update_skills_database(self, skills_set: Set[str], user_id: int) -> None:
        """Update the skills database with the provided skills set for a specific user.
        
            Args:
                skills_set (list): A list of skills to be added to the database.
                user_id (int): The ID of the user for whom the skills are being added.
        
            Returns:
                None
        
            Example:
                update_skills_database(['Python', 'SQL', 'JavaScript'], 123)
        """
        for skill in skills_set:
            print(f"SKILL: {skill}")
            self.database_manager.execute_query(
                "INSERT INTO skills (skill_name, user_id) VALUES (%s, %s)", (skill, user_id)
            )
            logging.info("Added Skill: %s for User ID: %s into database", skill, user_id)

        print("All skills were added to the database")

    def skills_wrapper(self, user_id):
        """
        Generates skill set from user profile then updates the database
        """
        skills_set = self.scrape_skills()
        self.update_skills_database(skills_set, user_id)

# pylint: disable=too-many-arguments, too-few-public-methods

class LinkedInBot(BaseManager):
    database_manager = DatabaseManager()

    def __init__(self, bot_id):
        super().__init__(WebDriverManager(bot_id=bot_id), LinkedInBot.database_manager)

        self.bot_id = bot_id
        self.sign_in_manager = LinkedInSignInManager(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager,
            bot_id=self.bot_id
        )
        self.profile_interactor = UserProfileInteractor(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager,
            bot_id=self.bot_id
        )
        self.main_page_scraper = MainUserPageScraper(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager,
            bot_id=self.bot_id
        )
        self.experience_manager = ExperienceManager(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager,
        )
        self.skills_manager = SkillsManager(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager,
        )

    @classmethod
    def get_total_number_of_bot_ids(cls) -> List[int]:
        """
        Get the total number of bot IDs from the database.
    
        Returns:
            list: A list of usable bot IDs.
        """
        # Generate query
        query = (
            "SELECT bot_id FROM bots WHERE bot_email IS NOT NULL "
            "ORDER BY bot_id;"
        )
        bot_id_query_result = cls.database_manager.execute_query(
            query=query,
            fetch="ALL"
        )

        usable_bot_id_list = [result[0] for result in bot_id_query_result]

        return usable_bot_id_list

    @classmethod
    def get_user_id(cls, profile_url: str) -> int:
        """Retrieves the user_id for a given profile_url"""
        # Set query arguments
        query = (
            "SELECT user_id FROM users WHERE profile_url = %s"
        )
        params = (profile_url,)
        fetch = "ONE"

        # Execute query
        user_id = cls.database_manager.execute_query(
            query=query,
            params=params,
            fetch=fetch
        )

        if user_id:
            return user_id[0]

        raise RuntimeError("NoneType user_id is invalid")

    def scrape_linkedin_page(self):
        """Master wrapper for the linkedin scraping processes."""
        # Handle login
        self.sign_in_manager.sign_in_wrapper(bot_id=self.bot_id)

        # Get the user profiles from the database
        profile_urls: List[str] = self.profile_interactor.get_profile_urls()

        # Loop through profile urls
        for profile_url in profile_urls:
            # Visit the user's profile
            self.profile_interactor.visit_user(profile_url=profile_url)
            
            # Run the main page wrapper
            self.main_page_scraper.main_user_page_scraper_wrapper(profile_url=profile_url)
            
            # Run the experiences wrapper
            self.experience_manager.experiences_wrapper(self.get_user_id(profile_url=profile_url))

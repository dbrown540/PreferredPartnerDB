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

Usage:
    Despite the length of this module, the execution is rather simple as I have decided to 
    use wrappers to contain the code logic. 

    >>> from src.bots.scipts.linkedinbot import LinkedInBot

    >>> usable_bot_id_list = LinkedInBot.get_total_number_of_bot_ids()

    >>> for bot_id in usable_bot_id_list:
    >>>     bot_instance = LinkedInBot(bot_id=bot_id)
    >>>     bot_instance.scrape_linkedin_page()


Author:
    Danny Brown

Date:
    May 6, 2024

Version:
    0.1-dev
"""
# pylint: disable=too-many-lines

import logging
import random
import time
from typing import Union, Tuple, Optional, Set, List
import re
from datetime import datetime

import psycopg2
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, WebDriverException,
    StaleElementReferenceException, ElementNotInteractableException)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from src.database.scripts.database_manager import DatabaseManager
from ..webdriver.webdriver_manager import WebDriverManager

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

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
        self.webdriver_manager = webdriver_manager

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
            self.webdriver_manager.humanized_send_keys(email_input, email)

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
            self.webdriver_manager.humanized_send_keys(password_input, password)

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
    Manages the extraction and processing of work experience information from LinkedIn profiles.

    This class provides methods to locate and extract job experience details, 
    including company names, job positions, position descriptions, and dates worked. 
    It also offers functionality to handle different types of LinkedIn pages and 
    print the extracted information.

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
        _locate_show_all_experiences_button():
            Locates and returns the href attribute of the 'Show all experiences' button on the page.
        _locate_list_element_wrappers(page: str):
            Locates and returns WebElements that serve as wrappers for each job experience.
        _has_multiple_experiences_at_one_company(list_element: List[WebElement], page: str):
            Checks if there are multiple work experiences at one company for a given list element.
        _create_company_name_list(list_elements: List[WebElement], page: str):
            Creates a list of company names extracted from the provided list of elements.
        _create_positions_list(list_elements: List[WebElement], page: str):
            Creates a list of job positions extracted from the provided list of elements.
        _create_positions_descriptions_list(list_elements: List[WebElement], page: str):
            Creates a list of position descriptions extracted from the given list of web elements.
        _create_dates_worked_list(list_elements: List[WebElement], page: str):
            Creates a list of dates worked for each position.
        remove_emojis_and_blank_lines(text: str):
            Removes emojis, bullet points, and blank lines from the given text.
        parse_date_range(date_range_text: str):
            Parses the date range text into a list containing start and end dates.
        _zip_all_experience_information(company_names_list: List[str], job_positions_list: List[str],
                                        position_descriptions, dates_worked_list):
            Zips together all the lists that were created while scraping the experiences.
        experience_wrapper():
            Wrapper for all experiences logic.
        _handle_original_page():
            Handles the original page for the current instance.
        _handle_new_page():
            Handles the new page for the current instance.
        _print_results(company_names_list, job_positions_list,
                        position_descriptions, dates_worked_list):
            Prints the zipped list.
    """
    def _locate_show_all_experiences_button(self) -> Optional[str]:
        """
        Locate and return the href attribute of the 'Show all experiences' button on the page.
        
        Returns:
            str: The href attribute of the button if found, None otherwise.
        """
        try:
            # Wait for the presence of at least one matching element
            experience_button = self.wait.until(
                EC.presence_of_element_located((By.ID, "navigation-index-see-all-experiences"))
            )

            return experience_button.get_attribute("href")

        except NoSuchElementException:
            info_message = "The button could not be found"
            logging.info(info_message)

        except TimeoutException:
            info_message = "The button could not be found due to timeout"
            logging.info(info_message)

        return False

    def _locate_list_element_wrappers(self, page) -> List[WebElement]:
        """
        Locates and returns WebElements that serve as wrappers for each job experience.

        Args:
            page (str): 
                Indicates the type of page where the elements are located.
                Possible values: 
                    "New" for a new page, or any other value for an existing page.

        Returns:
            List[WebElement]:
                A list of WebElements located on the page that serve as 
                wrappers for each job experience.

        Raises:
            NoSuchElementException: 
                If unable to locate the list elements on the page.
            TimeoutException: 
                If timed out while waiting for list elements to appear.
            StaleElementReferenceException: 
                If encountered a stale element reference while locating elements.
            WebDriverException: 
                If WebDriver encounters an exception during element location.
        """
        try:
            if page == "Original":

                # locate the experience div wrapper
                # The div wrapper encapsulates all the work experience information

                div_wrapper = self.wait.until(
                    EC.presence_of_element_located((By.ID, "experience"))
                )
                # Access the 2nd sibling div from the div_wrapper
                sibling_div_tag = div_wrapper.find_element(
                    By.XPATH, "./following-sibling::div[2]"
                )

                # Locate the list elements from the sibling div tag
                # The list tag will encapsulate only one job experience

                return sibling_div_tag.find_elements(
                    By.XPATH, "ul/li"
                )

            # The list element encapsulates one single work experience
            return self.wait.until(
                EC.presence_of_all_elements_located((
                    By.CLASS_NAME, "pvs-list__paged-list-item.artdeco-list__item" 
                                   ".pvs-list__item--line-separated.pvs-list__item--one-column"
                ))

            )

        except NoSuchElementException:
            logging.warning(
                "Could not locate the list elements."
            )

        except TimeoutException:
            logging.warning(
                "Timeout occurred while looking for list elements"
            )

        except StaleElementReferenceException:
            logging.warning(
                "Stale element error while looking for list elements"
            )

        return None

    def _has_multiple_experiences_at_one_company(
            self, list_element: List[WebElement], page: str) -> Tuple[bool, Optional[WebElement]]:
        """
        Check if there are multiple work experiences at one company for a given list element.

        Args:
        list_element (List[WebElement]):
            The web element representing the list containing work experiences.
        page (str):
            The type of LinkedIn page, either "Original" or "New".

        Returns:
        tuple:
            A tuple containing a boolean value indicating whether there are multiple
            experiences at one company and the anchor tag associated with it if found.
        """
        if page=="Original":
            try:
                anchor_tag = list_element.find_element(
                    By.XPATH, "div/div/div/a"
                )

                if anchor_tag:
                    return True, anchor_tag

            except NoSuchElementException:
                return False, None

        else:
            try:
                div_tag_containing_anchor = list_element.find_element(
                    By.CLASS_NAME, "display-flex.flex-row.justify-space-between"
                )

                anchor_tag = div_tag_containing_anchor.find_element(
                    By.TAG_NAME, "a"
                )

                return True, anchor_tag

            except NoSuchElementException:
                return False, None


        return False, None

    def _create_company_name_list(self, list_elements: List[WebElement], page: str):
        """
        Creates a list of company names extracted from the provided list of elements.

        Args:
            list_elements (list): A list of elements containing company information.
            page (str): The type of page being processed. Must be either "Original" or another value.

        Returns:
            list: A list of company names extracted from the provided elements.

        Raises:
            NoSuchElementException: If the required elements cannot be found.
        """
        company_names = []
        if page == "Original":
            for list_element in list_elements:
                has_multiple_experiences, anchor_tag = self._has_multiple_experiences_at_one_company(
                    list_element=list_element, page=page
                )

                if has_multiple_experiences:
                    # Handle case for multiple experiences at one company
                    span_tag_with_company_name = anchor_tag.find_element(
                        By.XPATH, "div/div/div/div/span[@aria-hidden='true']"
                    )
                    company_name = span_tag_with_company_name.text
                    company_name = self._clean_up_company_name(company_name)
                    company_names.append(company_name)

                else:                
                    span_tag_with_company_name = list_element.find_element(
                        By.XPATH, ".//span[contains(@class, 't-14 t-normal')]/span[@aria-hidden='true']"
                    )
                    company_name = span_tag_with_company_name.text
                    company_name = self._clean_up_company_name(company_name)
                    company_names.append(company_name)

        else:
            for list_element in list_elements:
                has_multiple_experiences, anchor_tag = self._has_multiple_experiences_at_one_company(
                    list_element=list_element, page=page
                ) # pylint disable=pointless-string-statement
                if has_multiple_experiences:
                    # Handle multiple work experience
                    span_element_with_company_name = anchor_tag.find_element(
                        By.CSS_SELECTOR, "span[aria-hidden='true']"
                    )
                    company_name = span_element_with_company_name.text
                    company_name = self._clean_up_company_name(company_name)
                    company_names.append(company_name)
                else:
                    # Handle single work experiences
                    parent_span_element = list_element.find_element(
                        By.CLASS_NAME, 't-14.t-normal'
                    )
                    span_element_with_company_name = parent_span_element.find_element(
                        By.CSS_SELECTOR, "span[aria-hidden='true']"
                    )

                    company_name_unparsed = (
                        span_element_with_company_name.text
                    )  # Ex. RELI Group, Inc. · Full-time

                    company_name = company_name_unparsed.split(" · ")[0]  # Ex. Reli Group, Inc.

                    company_name = self._clean_up_company_name(company_name)

                    company_names.append(company_name)

        return company_names

    def _create_positions_list(self, list_elements: List[WebElement], page: str, user_id: int) -> List[str]:
        """
        Creates a list of job positions extracted from the provided list of elements.

        Args:
            list_elements (list): A list of elements containing job position information.
            page (str): The type of page being processed. Must be either "Original" or another value.

        Returns:
            list: A list of job positions extracted from the provided elements.

        Raises:
            NoSuchElementException: If the required elements cannot be found.
        """
        positions_list = []
        if page == "Original":
            for list_element in list_elements:
                overflow_at_one_company = self._handle_overflow_at_one_company(list_element=list_element)
                if not overflow_at_one_company:
                    has_multiple_experiences, anchor_tag = self._has_multiple_experiences_at_one_company(
                        list_element=list_element,
                        page=page
                    )

                    if has_multiple_experiences:
                        positions_list_at_one_company = []
                        # Write conditions for multiple work experiences at one company
                        parent_div = anchor_tag.find_element(
                            By.XPATH, "./.."
                        )

                        sibling_div = parent_div.find_element(
                            By.XPATH, "following-sibling::*"
                        )

                        list_elements_containing_individual_job_titles = sibling_div.find_elements(
                            By.XPATH, "ul/li"
                        )

                        for element in list_elements_containing_individual_job_titles:
                            span_tag = element.find_element(
                                By.CSS_SELECTOR, "span[aria-hidden='true']"
                            )
                            position_title = span_tag.text
                            positions_list_at_one_company.append(position_title)

                        positions_list.append(positions_list_at_one_company)

                    else:
                        # Write conditions for single work experiences at one company
                        span_tag = list_element.find_element(
                            By.TAG_NAME, "span"
                        )
                        job_position_text = span_tag.text
                        positions_list.append(job_position_text)

                else:
                    # Handle overflow
                    self.driver.get(overflow_at_one_company)
                    self._handle_new_page(user_id=user_id)
                    return None

        else:
            print(page)
            for list_element in list_elements:
                has_multiple_experiences, anchor_tag = self._has_multiple_experiences_at_one_company(
                        list_element=list_element,
                        page=page
                )
                if has_multiple_experiences:
                    # Write conditions for multiple work experiences at one company
                    positions_list_at_one_company = []
                    # Access the parent of the anchor tag in order to access the correct DOM
                    parent_div = anchor_tag.find_element(
                        By.XPATH, "./.."
                    )

                    # Use the parent tag to access the sibling div tag that serves as a wrapper
                    # for the job titles
                    sibling_div = parent_div.find_element(
                        By.XPATH, "following-sibling::*"
                    )

                    # Access the list elements that sit inside the sibling_div element.
                    # These list elements contain the span tags that hold the position titles
                    multiple_experiences_list_elements = sibling_div.find_elements(
                        By.CLASS_NAME, "pvs-list__paged-list-item.pvs-list__item--one-column"
                    )

                    for list_element in multiple_experiences_list_elements:
                        span_tags = list_element.find_elements(
                            By.CSS_SELECTOR, "span[aria-hidden='true']"
                        )
                        position_title = span_tags[0].text
                        positions_list_at_one_company.append(position_title)
                    
                    positions_list.append(positions_list_at_one_company)


                else:
                    # Write conditions for single work experiences at one company
                    span_tag = list_element.find_element(
                        By.TAG_NAME, "span"
                    )
                    job_position_text = span_tag.text
                    positions_list.append(job_position_text)

        return positions_list

    def _create_positions_descriptions_list(
            self, list_elements: List[WebElement], page: str) -> List[str]:
        """
        Create a list of position descriptions extracted from the given list of web elements.

        Args:
        list_elements (List[WebElement]): A list of web elements containing position descriptions.
        page (str): The type of LinkedIn page, either "Original" or "New".

        Returns:
        List[str]: A list of position descriptions extracted from the web elements.
        """
        position_descriptions_list = []
        if page == "Original":
            for list_element in list_elements:
                has_multiple_experiences, _ = self._has_multiple_experiences_at_one_company(
                    list_element=list_element,
                    page=page
                )
                if has_multiple_experiences:
                        
                    # Write conditions for multiple work experiences at one company
                    position_descriptions_for_one_company = []
                    # Locate the li elmeents within the parent li element.
                    li_element_containers = list_element.find_elements(
                        By.XPATH, "div/div/div/ul/li"
                    )  # Represents each work experience at the company
                    for li_container in li_element_containers:
                        try:
                            span_tag_containing_description = li_container.find_element(
                                By.XPATH, ".//div[contains(@class, 'inline-show-more-text--is-collapsed')]/span[@aria-hidden='true']"
                            )
                            text = span_tag_containing_description.text
                            parsed_description = self.remove_emojis_and_blank_lines(text)
                            position_descriptions_for_one_company.append(parsed_description)
                        except NoSuchElementException:
                            position_descriptions_for_one_company.append(None)

                    position_descriptions_list.append(position_descriptions_for_one_company)
                else:
                    try:
                        # Locate the new ul/li that is embedded in the current list element
                        list_element_containing_description = list_element.find_element(
                            By.TAG_NAME, "li"
                        )
                        
                        # Locate the span tag containing the description under the new list element
                        span_tags_containing_description = list_element_containing_description.find_elements(
                            By.CSS_SELECTOR, "span[aria-hidden='true']"
                        )
                        for span_tag in span_tags_containing_description:
                            text = span_tag.text
                            parsed_description = self.remove_emojis_and_blank_lines(text)
                            position_descriptions_list.append(parsed_description)
                    except NoSuchElementException:
                        position_descriptions_list.append(None)
        else:  # New page
            for list_element in list_elements:
                has_multiple_experiences, _ = self._has_multiple_experiences_at_one_company(
                    list_element=list_element,
                    page=page
                )
                if has_multiple_experiences:
                    position_descriptions_for_one_company = []
                    list_element_containing_description = list_element.find_elements(
                        By.XPATH, ".//li[contains(@id, 'profilePagedListComponent')]"
                    )

                    for new_list_element in list_element_containing_description:
                        try:
                            span_tag_containing_description = new_list_element.find_element(
                                By.XPATH, ".//li/div/div/div/span[@aria-hidden='true']"
                            )
                            text = span_tag_containing_description.text
                            parsed_description = self.remove_emojis_and_blank_lines(text)
                            position_descriptions_for_one_company.append(parsed_description)
                        except NoSuchElementException:
                            position_descriptions_for_one_company.append(None)

                    position_descriptions_list.append(position_descriptions_for_one_company)

                else:
                    try:
                        div_container = list_element.find_element(
                            By.CLASS_NAME, "display-flex.align-items-center.t-14.t-normal.t-black"
                        )
                        span_tag = div_container.find_element(
                            By.TAG_NAME, "span"
                        )
                        text = span_tag.text
                        parsed_description = self.remove_emojis_and_blank_lines(text)
                        position_descriptions_list.append(parsed_description)
                    except NoSuchElementException:
                        position_descriptions_list.append(None)
        return position_descriptions_list

    def _create_dates_worked_list(
            self, list_elements: List[WebElement],
            page: str) -> List[List[Union[str, List[str]]]]:
        """
        Create a list of dates worked for each position.

        Args:
            list_elements (List[WebElement]):
                The list of web elements containing position information.
            page (str):
                The type of page being processed, either "Original" or "New".

        Returns:
            List[List[Union[str, List[str]]]]: 
                A list of dates worked for each position.
                Each sublist contains either a single date range string or a list of date ranges.
        """
        dates_worked_list = []
        if page == "Original":
            for list_element in list_elements:
                has_multiple_experiences, _ = self._has_multiple_experiences_at_one_company(
                    list_element=list_element,
                    page=page
                )

                if has_multiple_experiences:
                    dates_worked_at_multiple_experiences = []
                    span_containing_dates_worked = list_element.find_elements(
                        By.XPATH, ".//a/span/span[@class='pvs-entity__caption-wrapper']"
                    )
                    for date_range in span_containing_dates_worked:
                        date_range_text = date_range.text
                        parsed_dates = self.parse_date_range(date_range_text)
                        if parsed_dates:
                            dates_worked_at_multiple_experiences.append(parsed_dates)

                    dates_worked_list.append(dates_worked_at_multiple_experiences)

                else:
                    span_containing_dates_worked = list_element.find_element(
                        By.CLASS_NAME, "pvs-entity__caption-wrapper"
                    )
                    date_range_text = span_containing_dates_worked.text
                    parsed_dates = self.parse_date_range(date_range_text)
                    dates_worked_list.append(parsed_dates)



        else:
            for list_element in list_elements:
                has_multiple_experiences, _ = self._has_multiple_experiences_at_one_company(
                    list_element=list_element,
                    page=page
                )
                if has_multiple_experiences:
                    dates_worked_at_multiple_experiences = []
                    # Get to the li tag wrapper that contains the single position
                    list_elements_containing_single_experience = list_element.find_elements(
                        By.XPATH, ".//li[contains(@class, 'pvs-list__paged-list-item') "
                        "and contains(@class, 'pvs-list__item--one-column')]"
                    )
                    
                    for wrapper_list_element in list_elements_containing_single_experience:
                        span_containing_dates_worked = wrapper_list_element.find_element(
                            By.CLASS_NAME, "pvs-entity__caption-wrapper"
                        )
                        date_range_text = span_containing_dates_worked.text
                        parsed_dates = self.parse_date_range(date_range_text)
                        dates_worked_at_multiple_experiences.append(parsed_dates)

                    dates_worked_list.append(dates_worked_at_multiple_experiences)

                else:
                    span_containing_dates_worked = list_element.find_element(
                        By.CLASS_NAME, "pvs-entity__caption-wrapper"
                    )
                    date_range_text = span_containing_dates_worked.text
                    parsed_dates = self.parse_date_range(date_range_text)
                    dates_worked_list.append(parsed_dates)

        return dates_worked_list

    def _handle_overflow_at_one_company(self, list_element: WebElement):
        
        try: 
            overflow_a_tag = list_element.find_element(
                By.ID, 'navigation-index-see-all-positions-aggregated'
            )
            
            return overflow_a_tag.get_attribute("href")

        except NoSuchElementException:
            return False
        
        except StaleElementReferenceException:
            print("Stale element. I don't know why this is happening")

    @staticmethod
    def remove_emojis_and_blank_lines(text):
        """
        Remove emojis, bullet points, and blank lines from the given text.

        Args:
        text (str): The input text containing emojis, bullet points, and blank lines.

        Returns:
        str: The text with emojis, bullet points, and blank lines removed.
        """
        # Remove emojis
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F700-\U0001F77F"  # alchemical symbols
                            u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                            u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                            u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                            u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                            u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                            u"\U00002702-\U000027B0"  # Dingbats
                            u"\U000024C2-\U0001F251"
                            u"" 
                            "]+", flags=re.UNICODE)
        text_without_emojis = emoji_pattern.sub(r'', text)
        
        # Remove bullet points
        text_without_bullets = text_without_emojis.replace("•", "").strip()

        # Remove special characters
        text_without_special_characters = text_without_bullets.replace("�", "").strip()
        
        # Remove blank lines
        lines = text_without_special_characters.split('\n')
        clean_lines = (line.strip() for line in lines if line.strip())
        return ' '.join(clean_lines)
    
    @staticmethod 
    def _clean_up_company_name(text: str):
        return text.split(" · ")[0]


    @staticmethod
    def parse_date_range(date_range_text: str) -> List[str]:
        """
        Parse the date range text into a list containing start and end dates.

        Args:
            date_range_text (str): The text containing the date range.

        Returns:
            list: A list containing the start and end dates in the format YYYY-MM-DD.
        """
        # Extract the start and end dates using regex
        pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b|Present'
        dates = re.findall(pattern, date_range_text)

        # Convert dates to YYYY-MM-DD format
        formatted_dates = []
        for date_str in dates:
            if date_str == "Present":
                current_date = datetime.now().strftime("%Y-%m-%d")
                formatted_dates.append(current_date)
            else:
                # Check if the date string contains a month and a year
                date_parts = date_str.split()
                if len(date_parts) >= 2:
                    month_str, year_str = date_parts
                    month_num = {
                        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
                        'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
                        'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
                    }[month_str]
                    formatted_date = f"{year_str}-{month_num:02d}-01"
                    formatted_dates.append(formatted_date)

        # If there are two dates, assume the first is the start date and the second is the end date
        if len(formatted_dates) == 2:
            start_date = formatted_dates[0]
            end_date = formatted_dates[1]
            formatted_dates = [start_date, end_date]

        return formatted_dates
    
    @staticmethod
    def _zip_all_experience_information(company_names_list: List[str], job_positions_list: List[str], position_descriptions, dates_worked_list):
        """Zips together all the lists that were created while scraping the experiences."""
        return zip(company_names_list, job_positions_list, position_descriptions, dates_worked_list)

    def experience_wrapper(self, user_id):
        """Wrapper for all experiences logic"""
        button_href = self._locate_show_all_experiences_button()
        if not button_href:
            print(False)
            self._handle_original_page(user_id=user_id)
        else:
            print(True)
            self.driver.get(button_href)
            self._handle_new_page(user_id=user_id)

    def _handle_original_page(self, user_id):
        """Handles the original page for the current instance"""
        page = "Original"
        list_elements = self._locate_list_element_wrappers(page=page)
        company_name_list = self._create_company_name_list(list_elements=list_elements, page=page)
        job_positions_list = self._create_positions_list(list_elements=list_elements, page=page, user_id=user_id)
        if job_positions_list is None:
            print("Handling new page")
        else:
            position_descriptions = self._create_positions_descriptions_list(list_elements=list_elements, page=page)
            dates_worked_list = self._create_dates_worked_list(list_elements=list_elements, page=page)
            zipped_experiences_list = list(self._zip_all_experience_information(
                company_names_list=company_name_list,
                job_positions_list=job_positions_list,
                position_descriptions=position_descriptions,
                dates_worked_list=dates_worked_list,
            ))
            self.database_manager.update_experiences_in_database(user_id=user_id, zipped_list=zipped_experiences_list)

    def _handle_new_page(self, user_id):
        """Handles the new page for the current instance"""
        page = "New"
        list_elements = self._locate_list_element_wrappers(page=page)
        company_name_list = self._create_company_name_list(list_elements=list_elements, page=page)
        job_positions_list = self._create_positions_list(list_elements=list_elements, page=page, user_id=user_id)
        position_descriptions = self._create_positions_descriptions_list(list_elements=list_elements, page=page)
        dates_worked_list = self._create_dates_worked_list(list_elements=list_elements, page=page)
        zipped_list = self._zip_all_experience_information(
            company_names_list=company_name_list,
            job_positions_list=job_positions_list,
            position_descriptions=position_descriptions,
            dates_worked_list=dates_worked_list,
        )
        self.database_manager.update_experiences_in_database(zipped_list=zipped_list, user_id=user_id)

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
        try:
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

        except TimeoutException:
            print("Could not find any skills for this user")

        return skills_set

    def scrape_skills(self, profile_url):
        """Scrapes skills from user profile.
        
        Returns:
            set: A set of skills scraped from the webpage.
        """
        button_href = self.locate_skills_button()
        if button_href:
            self.driver.get(button_href)
            skills_set = self.scrape_skills_on_new_page()
            # Get back to the original page
            self.driver.get(profile_url)
        else:
            skills_set = self.scrape_skills_on_original_page()

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
        if not skills_set:
            self.database_manager.execute_query(
                "INSERT INTO skills (skill_name, user_id) VALUES (NULL, %s)", (user_id,)
            )
            logging.info("No skills added for User ID: %s into database", user_id)
            return

        for skill in skills_set:
            self.database_manager.execute_query(
                "INSERT INTO skills (skill_name, user_id) VALUES (%s, %s)", (skill, user_id)
            )
            logging.info("Added Skill: %s for User ID: %s into database", skill, user_id)

    def skills_wrapper(self, user_id, profile_url):
        """
        Generates skill set from user profile then updates the database
        """
        skills_set = self.scrape_skills(profile_url)
        self.update_skills_database(skills_set, user_id)

class LinkedInBot(BaseManager):  # pylint: disable=too-many-arguments, too-few-public-methods
    """
    A class representing a LinkedIn bot for automating interactions on the LinkedIn platform.

    This class inherits from the BaseManager class and provides functionality to manage 
    WebDriver and database interactions, handle LinkedIn sign-in, scrape user profiles, 
    and perform various automation tasks on LinkedIn.

    Attributes:
        database_manager (DatabaseManager): 
            An instance of DatabaseManager for database interactions.
        bot_id (int): 
            The unique identifier for the LinkedIn bot.
        sign_in_manager (LinkedInSignInManager): 
            An instance of LinkedInSignInManager for handling sign-in operations.
        profile_interactor (UserProfileInteractor): 
            An instance of UserProfileInteractor for interacting with user profiles.
        main_page_scraper (MainUserPageScraper): 
            An instance of MainUserPageScraper for scraping data from main user pages.
        experience_manager (ExperienceManager): 
            An instance of ExperienceManager for managing user experiences.
        skills_manager (SkillsManager): 
            An instance of SkillsManager for managing user skills.

    Methods:
        get_total_number_of_bot_ids() -> List[int]: 
            Get the total number of bot IDs from the database.
        get_user_id(profile_url: str) -> int: 
            Retrieve the user ID for a given profile URL.
        scrape_linkedin_page(): 
            Master wrapper for the LinkedIn scraping processes.
            Handles login, retrieves user profiles, and performs scraping tasks.
    """
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
            "SELECT bot_id FROM bots WHERE bot_id IS NOT NULL "
            "ORDER BY bot_id;"  # Change bot_id to bot_email
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
            
            # Get the user id
            user_id = self.get_user_id(profile_url=profile_url)

            print("USER ID: ", user_id)

            # Visit the user's profile
            self.profile_interactor.visit_user(profile_url=profile_url)

            # Run the main page wrapper
            self.main_page_scraper.main_user_page_scraper_wrapper(profile_url=profile_url)

            # Run the skills wrapper
            self.skills_manager.skills_wrapper(self.get_user_id(profile_url=profile_url), profile_url=profile_url)

            # Run the experience wrapper
            self.experience_manager.experience_wrapper(user_id=user_id)

            # Wait a little to go to the next profile
            time.sleep(10)
        
    def test(self, user_id, profile_url):
        # Test the Experiences methods
        self.driver.get(profile_url)
        user_id = 1
        self.experience_manager.experience_wrapper(user_id=user_id)
        # self.database_manager.export_to_xslx()

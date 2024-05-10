"""
This module provides classes for interacting with the Google search engine,
extracting LinkedIn profile links from webpages, and scrolling webpages to load
more search results.

Classes:
- GoogleSearcher:
    Provides functionality to interact with the Google search engine,
    including navigating to the homepage, locating the search box,
    and performing search queries for LinkedIn profiles.
- LinkExtractor:
    Extracts LinkedIn profile links from webpages using WebDriverManager
    and DatabaseManager instances to locate and parse the links.
- Scroller:
    Scrolls down webpages to load additional search results, extending
    the functionality of the BaseManager class.
- Scout class:
    Coordinates the search process, link extraction, and database updates,
    utilizing instances of GoogleSearcher, LinkExtractor, and Scroller
    classes to achieve its functionality.

Attributes:
    Inherits attributes and methods from BaseManager class where applicable.

Each class provides detailed docstrings describing its purpose, attributes, and methods.

Example Usage:
    The usage is rather simple as I have decided to wrap the logic into a single method 
    within the Scout class

    >>> from src.bots.scripts.scout import Scout

    >>> scout = Scout()
    >>> scout.execute(run=True, user_count=20)

Author:
    Danny Brown

Date:
    May 1, 2024

Version:
    0.1-dev
"""
import logging
import random
import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementNotInteractableException,
    ElementClickInterceptedException
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from .linkedinbot import BaseManager  #pylint: disable=relative-beyond-top-level
from ..webdriver_manager import WebDriverManager
from ...database.scripts.database_manager import DatabaseManager  #pylint: disable=relative-beyond-top-level

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

class GoogleSearcher(BaseManager):
    """
    GoogleSearcher provides functionality to interact with the Google search engine.

    This class encapsulates methods for navigating to the Google homepage,
    locating the search box on the webpage, and performing a Google search query
    for LinkedIn profiles containing specific phrases.

    Attributes:
        Inherits attributes and methods from BaseManager class.

    Methods:
        navigate_to_google():
            Navigates to the Google homepage.
        locate_google_search_box() -> WebElement:
            Locates the Google search box on the webpage.
        search_google_query(search_box: WebElement):
            Searches a Google query using the provided search box element.
    """
    def __init__(self, webdriver_manager: WebDriverManager, database_manager: DatabaseManager) -> None:
        super().__init__(webdriver_manager, database_manager)
        self.webdriver_manager = webdriver_manager

    def navigate_to_google(self) -> None:
        """Navigates to the Google homepage."""
        self.driver.get("https://www.google.com")

    def locate_google_search_box(self) -> WebElement:
        """
        Locates the Google search box on the webpage.
    
        Returns:
            WebElement: The located Google search box element.
    
        Raises:
            NoSuchElementException: If the Google search box could not be found.
            TimeoutException: If a timeout occurred while looking for the Google search box.
        """
        try:
            search_box = self.wait.until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
            return search_box

        except NoSuchElementException:
            logging.critical(
                "Google Search box could not be found.", exc_info=True
            )

        except TimeoutException:
            logging.critical(
                "A timeout occurred while looking for the Google search box.", exc_info=True
            )

        return None

    def search_google_query(self, search_box: WebElement) -> None:
        """
        Searches a Google query using the provided search box element.
    
        Args:
            search_box (WebElement): The search box element to type the query into.
    
        Returns:
            None
        """
        try:
            # Search query
            search_query = (
                '("Centers for Medicare & Medicaid Services") AND ("Office of the Administrator") '
                'site:linkedin.com/in'
            )

            self.webdriver_manager.humanized_send_keys(search_box, search_query)

            # Press enter to search
            search_box.send_keys(Keys.ENTER)

        except ElementNotInteractableException:
            logging.critical(
                "Search box is not interactable.", exc_info=True
            )

class LinkExtractor(BaseManager):  #pylint: disable=too-few-public-methods
    """
    A class for extracting LinkedIn profile links from a webpage.

    This class extends the functionality of the BaseManager class to 
    locate and parse LinkedIn profile links from a webpage.

    Attributes:
        webdriver_manager (WebDriverManager):
            An instance of the WebDriverManager class responsible for managing the WebDriver.
        database_manager (DatabaseManager):
            An instance of the DatabaseManager class responsible for managing the database.
        last_known_links_index (int):
            Index indicating the last known number of links processed.

    Methods:
        __init__(webdriver_manager, database_manager): 
            Initializes a LinkExtractor instance with the provided 
            WebDriverManager and DatabaseManager.
        link_extractor_wrapper():
            Finds and returns a list of LinkedIn profile links from the webpage.
        _collect_links():
            Waits for links to load on the webpage and returns a list of web elements
            representing the links.
        _parse_links(links):
            Parses a list of web elements representing links and 
            filters out LinkedIn profile links.
        _update_last_known_index(length):
            Updates the last known index to indicate the number of links processed.
    """
    def __init__(
            self, webdriver_manager: WebDriverManager,
            database_manager: DatabaseManager) -> None:
        super().__init__(webdriver_manager, database_manager)
        self.last_known_links_index = 0
        self.scroll_object = Scroller(webdriver_manager, database_manager)

    def _collect_links(self) -> List[WebElement]:
        """Waits for the links to load."""
        try:
            links = self.wait.until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
            )

            return links

        except NoSuchElementException:
            logging.critical("Link elements were not found in the Google search.")
            raise

        except TimeoutException:
            logging.critical("Timeout occurred while attempting to locate the links.")
            raise


    def _parse_links(self, links: List[WebElement]) -> List[str]:
        """Parses LinkedIn profile links."""
        return [
            link.get_attribute('href')
            for link in links
            if link.get_attribute('href') is not None
            and 'www.linkedin.com/in' in link.get_attribute('href')
        ]
    
    def link_extractor_wrapper(self, user_count):
        parsed_links = set()
        unchanged_count = 0  # Counter to track consecutive loops with no change in set length
        max_unchanged_loops = 5  # Maximum consecutive loops with no change allowed

        while len(parsed_links) < user_count:
            unfiltered_links = self._collect_links()
            newly_parsed_links = self._parse_links(unfiltered_links)
            self.scroll_object.scroll()

            prev_length = len(parsed_links)
            for new_link in newly_parsed_links:
                parsed_links.add(new_link)
            print(len(parsed_links))

            if len(parsed_links) == prev_length:
                unchanged_count += 1
                print("UNCHANGED COUNT: ", unchanged_count)
                if unchanged_count >= max_unchanged_loops:
                    break
            else:
                unchanged_count = 0

        # Finally, convert the set to a list
        parsed_links = list(parsed_links)
        return parsed_links


class Scroller(BaseManager):  #pylint: disable=too-few-public-methods
    """
    Scroller provides functionality to scroll down a webpage and load more search results.

    This class extends the functionality of the BaseManager class to scroll down a webpage,
    reaching the bottom to load additional search results if available.

    Attributes:
        Inherits attributes and methods from BaseManager class.

    Methods:
        scroll():
            Scrolls down to load more search results by invoking _scroll_to_bottom() 
            and _click_more_results_button() methods.
        _scroll_to_bottom():
            Scrolls the webpage to the bottom using JavaScript execution.
        _click_more_results_button():
            Clicks the 'More Results' button if found on the webpage.
    """
    def scroll(self):
        """Scrolls down to load more search results"""
        time.sleep(random.uniform(1, 3))
        self._scroll_to_bottom()
        self._click_more_results_button()

    def _scroll_to_bottom(self):
        """Scrolls the webpage to the bottom."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("SCROLLED TO BOTTOM")

    def _click_more_results_button(self):
        """Clicks the 'More Results' button if found."""
        try:
            time.sleep(1)
            more_results_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//a[@aria-label="More results"]')
                )
            )
            more_results_button.click()
            print('"More Results" button found and clicked')
        except TimeoutException:
            logging.warning('Timeout waiting for "More Results" button.')
        except NoSuchElementException as e:
            logging.error('Error clicking "More Results" button: %s', e)
        except ElementClickInterceptedException:
            logging.warning("More Results button click was intercepted")

class Scout(BaseManager):  #pylint: disable=too-few-public-methods
    """
    Scout class provides functionality to search Google, extract links,
    and update profile URLs in the database.

    This class extends the functionality of the BaseManager class to coordinate
    the search process, link extraction, and database updates.

    Attributes:
        Inherits attributes and methods from BaseManager class.
        google_searcher (GoogleSearcher): Instance of GoogleSearcher class
            for searching Google.
        link_extractor (LinkExtractor): Instance of LinkExtractor class
            for extracting links from search results.
        scroller (Scroller): Instance of Scroller class for scrolling the webpage.

    Methods:
        __init__():
            Initializes a Scout instance with WebDriverManager and DatabaseManager.
        execute(user_count=20):
            Executes the search process, link extraction, and database updates.
            If the link count exceeds the user_count, trims the list to match.
    """
    def __init__(self) -> None:
        super().__init__(WebDriverManager(), DatabaseManager())

        self.google_searcher = GoogleSearcher(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager
        )
        self.link_extractor = LinkExtractor(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager
        )
        self.scroller = Scroller(
            webdriver_manager=self.webdriver_manager,
            database_manager=self.database_manager
        )

    def execute(self, run: bool, user_count):
        """
        Optional wrapper. If the code doesn't become complex, 
        then I will move this to main
        """

        if run:

            # Navigate to Google
            self.google_searcher.navigate_to_google()

            # Locate the search box
            google_search_box_element = self.google_searcher.locate_google_search_box()

            # Type search into the search box element
            self.google_searcher.search_google_query(google_search_box_element)

            parsed_links = self.link_extractor.link_extractor_wrapper(user_count=user_count)

            self.database_manager.update_profile_urls_from_scout(parsed_links)

        else:
            print("Skipping Scout. If you want to run Scout, change the value of run to True")

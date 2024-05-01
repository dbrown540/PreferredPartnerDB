import logging
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementNotInteractableException
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from ..bots.scripts.linkedinbot import BaseManager  #pylint: disable=relative-beyond-top-level

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
                'site:linkedin.com/in "Centers for Medicare and Medicaid Services" "Data Analyst"'
            )

            # Type search query into the search box
            search_box.send_keys(search_query)

            # Press enter to search
            search_box.send_keys(Keys.ENTER)

        except ElementNotInteractableException:
            logging.critical(
                "Search box is not interactable.", exc_info=True
            )

class LinkExtractor(BaseManager):
    def locate_links(self, attempt=1) -> list:
        """Finds the LinkedIn profile links and returns a list"""
        parsed_links = []
        logging.info('self.last_known_index (links)= %d', self.last_known_links_index)

        # Wait for the search results to load
        self.wait_for_links_to_load()
        
        # Collect all possible links
        links = self.collect_links()

        # Parse the links making sure they are all profile links
        parsed_links = self.parse_links(links)

        # Get the last known index
        self.update_last_known_index(len(links))

        return parsed_links

    def wait_for_links_to_load(self):
        """Waits for the links to load."""
        self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))

    def collect_links(self) -> list:
        """Collects all links."""
        return self.driver.find_elements(By.TAG_NAME, 'a')

    def parse_links(self, links: list) -> list:
        """Parses LinkedIn profile links."""
        return [
            link.get_attribute('href') 
            for link in links 
            if link.get_attribute('href') is not None 
            and 'www.linkedin.com/in' in link.get_attribute('href')
        ]

    def update_last_known_index(self, length: int) -> None:
        """Updates the last known index."""
        self.last_known_links_index = length

class Scroller(BaseManager):
    def scroll(self):
        """Scrolls down to load more search results"""
        time.sleep(random.uniform(3, 5))
        self._scroll_to_bottom()
        self._click_more_results_button()

    def _scroll_to_bottom(self):
        """Scrolls the webpage to the bottom."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def _click_more_results_button(self):
        """Clicks the 'More Results' button if found."""
        try:
            more_results_button = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="botstuff"]/div/div[3]/div[4]/a[1]/h3/div/span[2]')
                )
            )
            more_results_button.click()
            print('"More Results" button found and clicked')
        except TimeoutException:
            logging.warning('Timeout waiting for "More Results" button.')
        except NoSuchElementException as e:
            logging.error('Error clicking "More Results" button: %s', e)


    def scroll_and_fetch_data(self, final_user_count: int):
        """Scrolls down to load more search results and fetches links and names"""
        parsed_links = []
        try:
            while len(parsed_links) < final_user_count:
                # Scroll down
                self.scroll()
                time.sleep(2)

                # Fetch links
                new_links = self.locate_links()
                parsed_links.extend(new_links)

                logging.info("Total links fetched: %d", len(parsed_links))

        except Exception as e:
            logging.error("An error occurred while scrolling and fetching data: %s", e)

        return parsed_links
    
    def count_users_table_rows(self):
        # Find out how many rows are in the database
        number_of_rows_in_users_table = self.database_manager.execute_query(query='SELECT COUNT(*) FROM users;', fetch='ONE')[0]
        
        return number_of_rows_in_users_table
    

    def update_database(self, parsed_links):
        for url in parsed_links:
            try:
            
                count = self.database_manager.execute_query(query='SELECT COUNT(*) FROM users WHERE profile_url = %s', params=(url,), fetch='ONE')[0]
                
                # If the user doesn't exist, insert into the database
                if count == 0:
                    self.database_manager.execute_query(query='INSERT INTO users (profile_url) VALUES (%s)', params=(url,))
                    print(f"Data for {url} inserted into database successfully.")
                
                # If the user already exists, skip insertion
                else:
                    print(f"Data for {url} already exists in the database. Skipping insertion.")
            
            except Exception as e:
                print(f"Failed to insert data into database: {e}")




    def execute(self, final_user_count: int):

        # Navigate to Google and search for linkedin profiles

        self.search_linkedin_profiles()
        
        # Count the number of rows in the existing database

        parsed_links = self.scroll_and_fetch_data(final_user_count)

        # Update the database

        self.update_database(parsed_links)
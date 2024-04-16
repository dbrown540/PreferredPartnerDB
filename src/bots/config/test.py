import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def locate_names(self, attempt=1) -> list:
        """Finds the links and names and returns a list"""
        parsed_names_list = []
        logging.info('self.last_known_index = %d', self.last_known_names_index)

        try: 
            names_wait = WebDriverWait(self.driver, 10)
            names_wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'LC20lb.MBeuO.DKV0Md')))
            names = self.driver.find_elements(By.CLASS_NAME, 'LC20lb.MBeuO.DKV0Md')
            
            # Start scraping from the last known index
            new_elements = names[self.last_known_names_index:]

            logging.info("Length of names: %d", len(names))
            logging.info("Last known index: %d", self.last_known_names_index)
            logging.info("Length of new elements: %d", len(new_elements))

            # Parse the names and add to list
            parsed_names_list = [name.text.split(' -')[0] for name in new_elements]

            # Update the last known index
            self.last_known_names_index += len(new_elements)

        except Exception as e:
            if attempt <= self.max_retries:
                logging.warning('Name elements not found. Retrying in %d seconds. (Attempt %d/%d)', self.retry_delay_seconds, attempt, self.max_retries)
                return self.locate_names(attempt + 1)
            else:
                logging.critical("Maximum retries. Check class name or try again later.\nError log:\n%s", e)

        return parsed_names_list

def refactored_find_names(self):
    names_wait = WebDriverWait(self.driver, 10)
    names_wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'LC20lb.MBeuO.DKV0Md')))
    names = self.driver.find_elements(By.CLASS_NAME, 'LC20lb.MBeuO.DKV0Md')

    
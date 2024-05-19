"""
WebDriverManager module provides functionality for managing a WebDriver instance
for automated browser testing.

This module encapsulates methods for initializing a WebDriver instance, handling
proxy rotation, and managing bot-specific configurations.

Classes:
    WebDriverManager: 
        Manages WebDriver instance and bot-specific configurations.

Attributes:
    None

Methods:
    __init__(self, bot_id): 
        Initializes a WebDriverManager instance with the given bot_id.
    initialize_webdriver(self): 
        Initializes a WebDriver instance with specified options.
    rotate_proxies(self): 
        Handles proxy rotation for the WebDriver instance.

Usage:
    Example usage of the WebDriverManager class:

    >>> manager = WebDriverManager(bot_id)
    >>> manager.initialize_webdriver()
    >>> manager.rotate_proxies()

Author:
    Danny Brown

Date:
    April 30, 2024

Version:
    0.1-dev
"""

import logging
import random
import time
import math
from typing import Tuple, List

import pyautogui  # pylint: disable=import-error
import numpy as np
import mouse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, ElementNotVisibleException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from ...database.scripts.database_manager import DatabaseManager

class WebDriverManager:
    """
    WebDriverManager provides functionality for managing a 
    WebDriver instance for automated browser testing.

    This class encapsulates methods for initializing and 
    closing a WebDriver instance, with options for
    specifying WebDriver options and service. 
    It integrates with the Selenium library to interact with web browsers.

    Attributes:
        driver_path (str): 
            The path to the WebDriver executable.
        driver (WebDriver): 
            The WebDriver instance initialized by the class.
        wait (WebDriverWait): 
            A WebDriverWait instance associated with the WebDriver instance.
        bot_id (int):
            Unique Bot ID

    Methods:
        __init__(): 
            Initializes a WebDriverManager instance 
            and sets up a WebDriver instance with specified options.
        initialize_webdriver(): 
            Initializes a WebDriver instance with specified options and service.
        close_webdriver(): 
            Closes the WebDriver instance associated with the object.
        rotate_proxies():
            Handles proxy rotation logic unique to each bot_id
        scroll_down():
            Uses JavaScript execute to scroll down the page
    """

    def __init__(self, bot_id: int = None):
        self.bot_id = bot_id
        self.driver_path = 'chromedriver-win64/chromedriver.exe'
        self.driver = self.initialize_webdriver()
        self.wait = WebDriverWait(self.driver, 10)
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
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-extensions')
            options.add_argument("--start-maximized")
            # Add capability to disable infobars
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            service = Service(self.driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            # Manage proxy options
            if self.bot_id:
                pass

            # Log the webdriver information
            info_message = (
                f"Service path: {self.driver_path}\nOptions: {options}"
            )
            logging.info(info_message)

            return driver

        except WebDriverException:
            logging.critical('Failed to initialize WebDriver: ', exc_info=True)
            raise

        except Exception:
            # For other exceptions, log the error and provide a generic error message
            error_message = (
                'An unexpected error occurred while initializing WebDriver: '
            )
            logging.critical(error_message, exc_info=True)
            raise

    def close_webdriver(self) -> None:
        """
        Closes the webdriver.

        This method attempts to close the webdriver instance associated with the object. 
        If a webdriver instance exists, it will be closed. 
        If no webdriver instance is found, it prints a message indicating 
        the absence of any instance to close.

        Raises:
            Exception: If an error occurs while attempting to 
                close the webdriver, an exception is raised. This could
                include errors such as WebDriverException or any other 
                exceptions related to webdriver operations.
                The specific error message can be retrieved from the exception object.
        """
        if self.driver:
            self.driver.close()
            logging.info("Webdriver closed successfully.")
        else:
            logging.info("No webdriver instance found to close.")

    def rotate_proxies(self):
        """Method that handles proxy rotation, provides unique proxy pool for each bot id"""

    def scroll_down(self, scroll_distance: float = random.randint(750, 1250)) -> None:
        """Scroll down the webpage by a random distance.
        
            Args:
                scroll_distance (int): 
                    The distance to scroll down the webpage.
                    Defaults to a random value between 750 and 1250.
        
            Returns:
                None
        """
        # Execute JavaScript to scroll down
        js_script = f"window.scrollBy(0, {scroll_distance});"
        self.driver.execute_script(js_script)

    def humanized_send_keys(self, element: WebElement, text: str, characters_per_minute: int = 7500) -> None:
        """
        Simulates human typing speed while sending keys to a web element.
        
        Args:
            element (WebElement): The web element to send keys to.
            text (str): The text to be sent to the web element.
            characters_per_minute (int): The typing speed in characters per minute.
        
        Returns:
            None
        """
        characters_per_second = characters_per_minute / 60
        start_time = time.time()

        for character in text:
            element.send_keys(character)
            error = random.uniform((1 / (3.5 * characters_per_second)), (3.5 / characters_per_second))  # Factors are arbitrary
            sleep = 1 / (characters_per_second) + error
            time.sleep(sleep)

        end_time = time.time()

        print("Total time: ", end_time - start_time)

    def humanized_scroll(self, element):
        """
        Scrolls the page to make the specified element visible in the viewport and returns the coordinates of the element relative to the viewport.
        
        Args:
            element: The element to be scrolled into view.
        
        Returns:
            tuple: A tuple containing the X and Y coordinates of the element relative to the viewport.
        """
        # Get the window height
        window_height = self.driver.execute_script("return window.innerHeight;")
        print("Window height: ", window_height)

        # Get the location and height of the element
        element_y = element.location["y"] - window_height
        print("ELEMENT Y: ", element_y)

        # Calculate the bottom position of the element
        bottom_of_viewport = window_height
        print("BVP: ", bottom_of_viewport)
        scroll_position = 0

        while element_y > bottom_of_viewport:
            # Determine the scroll position
            scroll_position = self.driver.execute_script("return window.pageYOffset;")
            print("SCROLL POS: ", scroll_position)
            
            # Calculate the bottom of the viewport
            bottom_of_viewport = scroll_position + window_height
            print("BVP: ", bottom_of_viewport)
            
            body_tag = self.driver.find_element(By.TAG_NAME, "body")
            body_tag.send_keys(Keys.PAGE_DOWN)
            
            time.sleep(1)

        # Calculate the coordinates of the element relative to the viewport
        element_x = element.location["x"]  # X-coordinate of the element
        scroll_position_x = self.driver.execute_script("return window.pageXOffset;")  # Horizontal scroll position
        result_x = element_x - scroll_position_x  # Horizontal position relative to the viewport

        result_y = bottom_of_viewport + element_y  # Vertical position relative to the viewport

        print("ELEMENT X: ", element_x)
        print("SCROLL POS X: ", scroll_position_x)
        print(result_x, result_y)

        target = (result_x, result_y)

        print("Found the element")
        # Additional sleep for debugging purposes
        return target
    
    def humanized_mouse_movement(self, mouse_path: Tuple[List[int], List[int]]):
        """Move the mouse cursor along a humanized path."""
        # Adjust path for navbar thickness
        adjusted_path = [(x, y) for x, y in zip(mouse_path[0], mouse_path[1])]

        print("Moving mouse to the center")
        for x, y in adjusted_path:
            mouse.move(x, y, duration=0.0001)

        print("At the target")
        print(adjusted_path[-1][0], adjusted_path[-1][1])

        time.sleep(3)

    def calculate_mouse_path(self, start: Tuple[int, int], target: Tuple[int, int], navbar_thickness=95):
        """Calculate the mouse path between start and target."""
        num_steps = round(abs(target[0] - start[0]))

        # Generate linearly spaced x and y coordinates
        x_path = np.linspace(start=start[0], stop=target[0], num=num_steps)
        y_path = np.linspace(start=start[1], stop=target[1], num=num_steps)

        # Adjust y_path based off the thickness of the navbar
        adjusted_y_path = [y + navbar_thickness for y in y_path]

        # Generate oscillation values
        osc = np.log(np.linspace(1, 10, num=num_steps))
        osc[-1] = 0
        print(osc)

        # Calculate rounded x and y coordinates
        rounded_xpath = [round(value) for value in x_path]
        rounded_ypath = [round(value + 15 * osc_val) for value, osc_val in zip(adjusted_y_path, osc)]

        mouse_path = (rounded_xpath, rounded_ypath)

        return mouse_path
    
    def humanize_click(self, element):
        # Get current mouse position
        startingx, startingy = pyautogui.position()

        # Get starting and target coords as tuples
        starting_coords = (startingx, startingy)
        target_coords = self.humanized_scroll(element)

        # Calculate the mouse path
        mouse_path = self.calculate_mouse_path(start=starting_coords, target=target_coords)

        # Move the cursor to the element
        self.humanized_mouse_movement(mouse_path)

    def save_cookies(self, bot_id, website):
        # Check if cookies exist
        query = (
            "SELECT COUNT(*) FROM cookies "
            "WHERE bot_id = %s AND website = %s;"
        )
        params=(bot_id, website)
        fetch = "ONE"

        self.database_manager.execute_query(
            query=query,
            params=params,
            fetch=fetch
        )


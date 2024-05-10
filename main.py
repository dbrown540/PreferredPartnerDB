"""
Script for executing web scraping tasks using Scout and LinkedInBot.

This script initiates instances of Scout, BotCredentialsManager,
and LinkedInBot classes to perform web scraping tasks.
It first utilizes the Scout class to search Google, extract links, 
and update profile URLs in the database.
Then, it utilizes the LinkedInBot class to scrape LinkedIn pages for data.

Usage:
    Ensure that the required modules are installed and configured properly.
    Run this script using Python to execute the web scraping tasks.

Example:
    $ python main.py

Author:
    Danny Brown

Date:
    May 1, 2024

"""
import time
import random
from src.bots.scripts.scout import Scout
from src.bots.bot_credentials_manager import BotCredentialsManager
from src.bots.scripts.linkedinbot import LinkedInBot
from src.database.scripts.database_manager import DatabaseManager
from testing.scratch import Wrapper
from src.bots.webdriver_manager import WebDriverManager

def main():
    """
    Execute main function to run Scout and LinkedIn Bot.
    
    This function initializes a Scout instance and executes it with a user count of 20.
    It also retrieves a list of usable bot IDs from LinkedInBot and iterates 
    through each ID to create a LinkedInBot instance and scrape a LinkedIn page.
    """
    """# Scout
    scout = Scout()
    scout.execute(run=True, user_count=1000)

    # Bot Credential Manager
    bot_credentials_manager = BotCredentialsManager()
    bot_credentials_manager.bot_credentials_wrapper()

    # LinkedIn Bot
    usable_bot_id_list = LinkedInBot.get_total_number_of_bot_ids()

    for bot_id in usable_bot_id_list:
        bot_instance = LinkedInBot(bot_id=bot_id)
        bot_instance.scrape_linkedin_page()
        time.sleep(random.uniform(7, 12))"""

    phone_number_scraper_object = Wrapper()
    phone_number_scraper_object.execute()

if __name__ == '__main__':
    main()

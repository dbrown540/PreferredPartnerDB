from src.scout.scout import Scout
from src.bots.scripts.bot_credentials_manager import BotCredentialsManager
from src.bots.scripts.linkedinbot import *
from src.database.scripts.database_manager import DatabaseManager
import time

def main():

    
    
    usable_bot_id_list = LinkedInBot.get_total_number_of_bot_ids()
    
    for bot_id in usable_bot_id_list:
        bot_instance = LinkedInBot(bot_id=bot_id)
        bot_instance.scrape_linkedin_page()

    

if __name__ == '__main__':
    main()

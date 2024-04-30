from src.scout.scout import Scout
from src.bots.scripts.bot_credentials_manager import BotCredentialsManager
from src.bots.scripts.linkedinbot import *
from src.database.scripts.database_manager import DatabaseManager
import time

def main():
    
    usable_bot_id_list = LinkedInBot.get_total_number_of_bot_ids()
    print(usable_bot_id_list)
    

if __name__ == '__main__':
    main()

from src.scout.scout import Scout
from src.database.scripts.insert import Insert
from src.bots.config.bot_credentials_manager import BotCredentialsManager
from src.bots.config.proton import Proton

'''def main():
    # Check Scout data already exists
    insert_object = Insert()
    scout_data_exists = insert_object.check_if_exists()

    if not scout_data_exists:
        # Create Scout object
        scout = Scout()

        # Navigate to google and use the boolean search
        scout.navigate_to_google()
        parsed_names_list, parsed_links = scout.scroll_and_fetch_data()
        scout.export_to_csv(parsed_names_list, parsed_links)

        # Insert Scout's data into the database
        
        insert_object.insert_scout()

    # Check to see if there are existing credentials in the bots table:
    bot_manager = BotCredentialsManager(filepath="src/bots/config/names.txt")

    # Check if bot has an existing email
'''

def main():
    
    # Create Scout object
    scout = Scout()
    scout.execute(final_user_count=61)

    '''# Create BotCredentialsManager object
    bot_manager = BotCredentialsManager(filepath="src/bots/config/names.txt")
    bot_manager.execute()'''

if __name__ == '__main__':
    main()
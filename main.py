from src.scout.scout import Scout
from src.database.scripts.insert import Insert
from src.bots.config.create_email_login import BotCredentialsManager

def main():
    # Create Scout object
    scout = Scout()
    scout.navigate_to_google()
    parsed_names_list, parsed_links = scout.scroll_and_fetch_data()
    scout.export_to_csv(parsed_names_list, parsed_links)

    # Insert Scout's data into the database
    insert_object = Insert()
    insert_object.insert_scout()

    # Check to see if there are existing credentials in the bots table:
    bot_manager = BotCredentialsManager(filepath="src/bots/config/names.txt")
    # Generate fake email addresses
    email_list = bot_manager.create_email()

    # Generate strong passwords
    password_list = bot_manager.generate_strong_password()

    # Create lists for first and last names for the bots
    first_names_list, last_names_list = bot_manager.create_names_lists()

    # Export email and password lists to a CSV file
    bot_manager.export_to_csv(first_names_list, last_names_list, email_list, password_list)

    # Check if credentials exist in the database and insert them if necessary
    bot_manager.check_if_credentials_exist_in_db()


if __name__ == '__main__':
    main()
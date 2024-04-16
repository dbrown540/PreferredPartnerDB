from src.scout.scout import Scout
from src.database.scripts.insert import Insert
from src.bots.config.bot_credentials_manager import BotCredentialsManager
from src.bots.config.proton_mail_manager import Proton

def main():
    
    '''# Create Scout object
    scout = Scout()
    scout.execute(final_user_count=20)'''

    # Create BotCredentialsManager object
    '''bot_manager = BotCredentialsManager(filepath="src/bots/config/names.txt")
    bot_manager.execute()'''

    proton_manager = Proton()
    proton_manager.execute_account_creation()

if __name__ == '__main__':
    main()
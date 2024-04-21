from src.scout.scout import Scout
from src.bots.scripts.bot_credentials_manager import BotCredentialsManager
from src.bots.scripts.proton_mail_manager import Proton
from src.bots.scripts.sms_to_me import SMSToMe
from src.bots.scripts.get_test_proxies import ProxyManager
from src.bots.scripts.linkedinbot import LinkedInBot

def main():
    
    '''# Create Scout object
    scout = Scout()
    scout.execute(final_user_count=20)

    # Create BotCredentialsManager object
    bot_manager = BotCredentialsManager(filepath="src/bots/config/names.txt")
    bot_manager.execute()

    proton_manager = Proton()
    proton_manager.execute_account_creation()

    # Create a smstome object
    sms_to_me_object = SMSToMe()
    sms_to_me_object.refresh_phone_number_list()

    # Create proxy manager object
    proxy_manager = ProxyManager()
    proxy_manager.execute()'''

    linkedin_bot = LinkedInBot()
    linkedin_bot.execute()

if __name__ == '__main__':
    main()
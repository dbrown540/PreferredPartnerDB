from src.scout.scout import Scout
from src.bots.scripts.bot_credentials_manager import BotCredentialsManager
from src.bots.scripts.proton_mail_manager import Proton
from src.bots.scripts.sms_to_me import SMSToMe
from src.bots.scripts.get_test_proxies import ProxyManager
from src.bots.scripts.linkedinbot import LinkedInBot
#from bottest import LinkedInBot

def main():
    
    # Create Scout object
    scout = Scout()
    scout.execute(final_user_count=25)

    # Create BotCredentialsManager object
    bot_manager = BotCredentialsManager(filepath="src/bots/config/names.txt")
    bot_manager.execute()

    linkedin_bot = LinkedInBot()
    linkedin_bot.execute()

if __name__ == '__main__':
    main()
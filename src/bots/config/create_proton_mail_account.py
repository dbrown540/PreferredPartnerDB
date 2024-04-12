from ...scout.scout import Scout
import time

class Proton(Scout):
    def access_proton_mail(self):
        self.driver.get("https://proton.me/mail")
        time.sleep(3)
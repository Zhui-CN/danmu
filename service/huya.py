from service.base import BaseClass
from utils.log import logger


class HuYa(BaseClass):
    name = "huya"

    def is_login(self):
        ele = self.chrome.get_element('//div[contains(@class, "success-login")]')
        if ele and not ele.get_attribute("style"):
            return False
        super().is_login()
        return True

    def run(self, text):
        super().run(text)
        self.chrome.get_web(self.url, second=4)

        if not self.is_login():
            return

        self.chrome.send_text(xpath="//textarea[contains(@id, 'pub_msg_input')]", text=text, second=2)
        self.chrome.click(xpath="//*[contains(@id, 'msg_send_bt')]", second=1)
        logger.info("平台:{}->房间:{}->弹幕:{}".format(self.name, self.url, text))

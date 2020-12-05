from service.base import BaseClass
from utils.log import logger


class JiuXiu(BaseClass):
    name = "jiuxiu"

    def is_login(self):
        ele = self.chrome.get_element('//div[@class="userInfo loginLayout"]')
        if ele and ele.get_attribute("style"):
            return False
        super().is_login()
        return True

    def run(self, text):
        super().run(text)
        self.chrome.get_web(self.url, second=4)
        if not self.is_login():
            return
        self.chrome.send_text(xpath="//input[@id='txtchatcontent']", text=text, second=2)
        self.chrome.click(xpath='//*[contains(@class, "e_publish_btn")]', second=1)
        logger.info("平台:{}->房间:{}->弹幕:{}".format(self.name, self.url, text))

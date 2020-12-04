from utils.redis import RedisSession
from utils.error import NotUrlError, NotCookieError


class BaseClass:
    name = ""

    def __init__(self, chrome):
        self.chrome = chrome
        self.cookie = None
        self.cookie_set = False
        self.url = None

    def run(self, text):
        self.url = RedisSession.get_url(self.name + "_room_ls")
        if not self.url: raise NotUrlError(self.name)
        self.cookie = RedisSession.get_cookie(self.name + "_cookie_ls")
        if not self.cookie: raise NotCookieError(self.name)
        self.chrome.set_cookie(self.url, self.cookie)

    def is_login(self):
        RedisSession.set_cookie(self.name + "_cookie_ls", self.cookie)
        self.cookie_set = True

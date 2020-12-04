import logging
from selenium.webdriver.remote.remote_connection import LOGGER as selenium_logger
from urllib3.connectionpool import log as urllib_logger

logger = logging.getLogger()
fmt = logging.Formatter('---------%(message)s---------')
sh = logging.StreamHandler()
sh.setFormatter(fmt)
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)
urllib_logger.setLevel(logging.WARNING)
selenium_logger.setLevel(logging.WARNING)

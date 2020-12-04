import sys
from os.path import dirname, join, abspath
from utils.error import NotMenuError, BreakProgram, NotDigitError


def is_windows():
    return sys.platform in ('win32', 'cygwin')


def is_linux():
    return sys.platform.startswith('linux')


def is_mac():
    return sys.platform == 'darwin'


def get_canonical_os_name():
    if is_windows():
        return 'windows'
    elif is_mac():
        return 'mac'
    elif is_linux():
        return 'linux'


def locate_web_driver():
    driver_name = "chromedriver"
    if is_windows():
        driver_name = 'chromedriver.exe'
    return join(dirname(dirname(abspath(__file__))), "chrome", get_canonical_os_name(), driver_name)


def is_menu(menu):
    if isinstance(menu, str):
        menu = menu.strip()
        if menu == "0":
            raise BreakProgram
        elif not menu.isdigit():
            raise NotDigitError
        return menu
    elif menu is None:
        raise NotMenuError
    return menu

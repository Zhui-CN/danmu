# -*- encoding=utf8 -*-

import multiprocessing
from utils.utils import is_menu
from utils.log import logger
from utils.error import NotMenuError, BreakProgram, NotDigitError
from script.download_driver import download_driver_run
from script.add_urls import add_urls_run
from script.add_cookies import add_cookies_run
from script.danmu import danmu_run

menu_map = {
    "0": "0",
    "1": download_driver_run,
    "2": add_urls_run,
    "3": add_cookies_run,
    "4": danmu_run
}


def run():
    while True:
        print("------------请选择功能-------------")
        print(" 1: 检测脚本驱动")
        print(" 2: 批量添加url")
        print(" 3: 批量添加cookie")
        print(" 4: 运行danmu脚本")
        print(" 0: 退出")
        print("---------------------------------")
        try:
            is_menu(menu_map.get(input("请输入功能序号:")))()
        except (NotMenuError, NotDigitError) as e:
            logger.error(e)
            continue
        except BreakProgram:
            break


if __name__ == '__main__':
    multiprocessing.freeze_support()
    run()

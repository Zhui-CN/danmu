import time
import traceback
import multiprocessing
from service.huya import HuYa
from os import cpu_count
from random import choice
from service.douyu import DouYu
from chrome.driver import ChromeDriver
from service.jiuxiu import JiuXiu
from utils.log import logger
from utils.error import NotUrlError, NotCookieError, NotDigitError, NotMenuError, BreakProgram
from utils.redis import RedisSession
from utils.utils import is_menu

platform_map = {
    "0": "0",
    "1": {
        "name": "九秀",
        "class": JiuXiu
    },
    "2": {
        "name": "虎牙",
        "class": HuYa
    },
    "3": {
        "name": "斗鱼",
        "class": DouYu
    }
}

platform_map[str(len(platform_map))] = [platform for platform in platform_map.values() if platform != "0"]


class InitChrome:
    _instance = None
    _chrome = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object().__new__(cls)
            cls._chrome = ChromeDriver(args[0])
        return cls._instance

    @property
    def chrome(self):
        return self._chrome

    @classmethod
    def close(cls):
        if cls._chrome: cls._chrome.close()
        cls._chrome = None
        cls._instance = None


def init(text_ls, is_headless, platform, sleep_time):
    while True:
        chrome_obj = InitChrome(is_headless)
        platform_item = choice(platform) if isinstance(platform, list) else platform
        platform_obj = platform_item.get("class")(chrome_obj.chrome)
        try:
            platform_obj.run(choice(text_ls))
        except (NotUrlError, NotCookieError) as e:
            logger.error("ERROR: {}".format(e))
            time.sleep(8)
        except Exception as e:
            traceback.print_exc()
            logger.error("ERROR: {}".format(e))
            if not platform_obj.cookie_set: RedisSession.set_cookie(
                platform_obj.name + "_cookie_ls", platform_obj.cookie
            )
            chrome_obj.close()
            time.sleep(5)
        else:
            time.sleep(int(sleep_time))


def danmu_run():
    while True:
        try:
            print("------------请选择平台-------------")
            for idx, value in platform_map.items():
                if idx != "0" and idx != str(len(platform_map) - 1):
                    print(" {}: 启动{}弹幕".format(idx, value["name"]))
            print(" {}: 全平台随机发送".format(len(platform_map) - 1))
            print(" 0: 退出")
            print("---------------------------------")
            platform = is_menu(platform_map.get(input("请输入功能序号:")))
            print("------请选择是否使用无窗口模式-------")
            print(" 1: 启用")
            print(" 2: 不启用")
            print(" 0: 退出")
            print("---------------------------------")
            is_headless = int(is_menu(input("请输入功能序号:")))
            sleep_time = int(is_menu(input("弹幕间隔时间(>1,<9000的整数):")))
            cpu_num = cpu_count()
            logger.info("当前PC有{}个核数".format(cpu_num))
            input_count = int(is_menu(input('请输入浏览器个数:')))
            cpu_num = input_count if input_count <= cpu_num else cpu_num
            logger.info("RUNING CPU NUMBER IS {}".format(cpu_num))
            process_list = []
            with open('words.txt', 'r', encoding='utf-8') as f:
                text_ls = f.read().split('\n')
            for _ in range(cpu_num):
                process = multiprocessing.Process(
                    target=init, args=(text_ls, is_headless, platform, sleep_time)
                )
                process.start()
                process_list.append(process)
            for p in process_list:
                p.join()
            logger.info("运行完成")
        except (NotMenuError, NotDigitError) as e:
            logger.info(e)
            continue
        except BreakProgram:
            break


if __name__ == '__main__':
    danmu_run()

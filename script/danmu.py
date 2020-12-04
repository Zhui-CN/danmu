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
    # "douyu": DouYu,
    "huya": HuYa,
    "九秀": JiuXiu
}

platform_ls = [key for key in platform_map.keys()]


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


def init(text_ls, is_headless, choice_platform, sleep_time):
    while True:
        chrome_obj = InitChrome(is_headless)
        # name = choice(platform_ls)
        name = choice_platform
        platform_obj = platform_map.get(name)(chrome_obj.chrome)
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
            for idx, key in enumerate(platform_map.keys()):
                print(" {}: 启动{}弹幕".format(idx + 1, key))
            print(" 0: 取消添加")
            print("---------------------------------")
            choice_platform = int(is_menu(input("请输入功能序号:")))
            print("------请选择是否使用无窗口模式-------")
            print(" 1: 启用")
            print(" 2: 不启用")
            print(" 0: 退出")
            print("---------------------------------")
            is_headless = int(is_menu(input("请输入功能序号:")))
            print("------请选择是否使用无窗口模式-------")
            sleep_time = int(is_menu(input("弹幕间隔时间(>1,<9000的整数):")))
            print("---------------------------------")
            cpu_num = cpu_count()
            logger.info("当前PC有{}个核数".format(cpu_num))
            input_count = int(is_menu(input('请输入浏览器个数:')))
            cpu_num = input_count if input_count <= cpu_num else cpu_num
            logger.info("RUNING CPU NUMBER IS {}".format(cpu_num))
            process_list = []
            with open('words.txt', 'r', encoding='utf-8') as f:
                text_ls = f.read().split('\n')
            for _ in range(cpu_num):
                process = multiprocessing.Process(target=init,
                                                  args=(text_ls, is_headless, platform_ls[choice_platform - 1],sleep_time))
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

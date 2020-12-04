import os
from utils.log import logger
from utils.utils import is_menu
from utils.redis import RedisSession
from utils.error import NotMenuError, BreakProgram, NotDigitError

cookies_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cookies")


def add_cookies_run():
    while True:
        try:
            if not os.path.exists(cookies_dir):
                os.makedirs(cookies_dir)
            file_ls = os.listdir(cookies_dir)
            if not file_ls: return logger.info("请在目录: {} 里添加cookies文件".format(cookies_dir))
            file_item = {"0": "0"}
            all_file_ls = []
            print("------------请选择文件-------------")
            for index, file_name in enumerate(file_ls, 1):
                file_info = {"name": file_name, "dir": os.path.join(cookies_dir, file_name)}
                file_item[str(index)] = [file_info]
                all_file_ls.append(file_info)
                print(" {}: {}".format(index, file_name))
            file_item[str(len(file_ls) + 1)] = all_file_ls
            print(" {}: 添加全部文件".format(len(file_ls) + 1))
            print(" 0: 取消添加")
            print("---------------------------------")
            select_file_ls = is_menu(file_item.get(input("请输入功能序号:")))
            for file_dict in select_file_ls:
                file_title = file_dict["name"].split(".")[0]
                file_dir = file_dict["dir"]
                with open(file_dir, "r", encoding="utf-8") as f:
                    cookie_ls = [cookie.strip().strip(";") for cookie in f.read().split('\n') if cookie.strip()]
                cookie_ls += RedisSession.lrange('{}_cookie_ls'.format(file_title), 0, -1)
                cookie_ls = list(set(cookie_ls))
                RedisSession.delete('{}_cookie_ls'.format(file_title))
                for idx, cookie in enumerate(cookie_ls, 1):
                    RedisSession.set_cookie('{}_cookie_ls'.format(file_title), cookie.strip())
                    logger.info("SET {} {}_cookie".format(idx, file_title))
            logger.info("添加完成")
        except (NotMenuError, NotDigitError) as e:
            logger.error(e)
            continue
        except BreakProgram:
            break


if __name__ == '__main__':
    add_cookies_run()

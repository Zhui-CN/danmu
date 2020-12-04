import math
import time

import requests
from utils.redis import RedisSession
from utils.utils import is_menu
from utils.log import logger
from utils.error import NotMenuError, BreakProgram, NotDigitError


def get_douyu_url_ls(input_url_num):
    room_ls = []
    for i in range(1, math.ceil(input_url_num / 120) + 1):
        info = requests.get('https://www.douyu.com/gapi/rkc/directory/mixList/0_0/{}'.format(i)).json()
        room_ids = [room['rid'] for room in info['data']['rl']]
        for room_id in room_ids:
            room_ls.append('https://www.douyu.com/{}'.format(room_id))
    return room_ls


def get_huya_url_ls(input_url_num):
    params = {
        "m": 'LiveList',
        "do": 'getLiveListByPage',
        # "gameId": 2135,
        "tagAll": 0,
        "page": '1',
    }
    room_ls = []
    for i in range(1, math.ceil(input_url_num / 120) + 1):
        params['page'] = i
        info = requests.get('https://www.huya.com/cache.php', params=params).json()
        room_ids = [room['profileRoom'] for room in info['data']['datas']]
        for room_id in room_ids:
            room_ls.append('https://www.huya.com/{}'.format(room_id))
    return room_ls


def get_jiuxiu_url_ls(input_url_num):
    params = {
        "tag": "hot",
        "page": "1",
        "pagesize": "28",
        "v": int(time.time() * 1000)
    }
    room_ls = []
    for i in range(1, math.ceil(input_url_num / 28) + 1):
        params['page'] = i
        info = requests.get('https://www.9xiu.com/ajax/index/getroomsbytag', params=params).json()
        room_ids = [room['rid'] for room in info['data']]
        for room_id in room_ids:
            room_ls.append('https://www.9xiu.com/{}'.format(room_id))
    return room_ls


menu_map = {
    "0": "0",
    "1": {"key": "douyu", "name": "斗鱼", "func": get_douyu_url_ls},
    "2": {"key": "huya", "name": "虎牙", "func": get_huya_url_ls},
    "3": {"key": "jiuxiu", "name": "九秀", "func": get_jiuxiu_url_ls},
}


def add_urls_run():
    while True:
        print("------------请选择平台-------------")
        for key, value in menu_map.items():
            if key != "0":
                print(" {}: 添加{}url".format(key, value["name"]))
        print(" 0: 取消添加")
        print("---------------------------------")
        try:
            menu_dict = is_menu(menu_map.get(input("请输入功能序号:")))
            key = menu_dict["key"]
            name = menu_dict["name"]
            func = menu_dict["func"]
            input_url_num = is_menu(input("请输入要添加{}的url数量(0则取消):".format(name)))
            RedisSession.delete('{}_room_ls'.format(key))
            result_ls = func(int(input_url_num))
            for result in result_ls:
                logger.info(result)
                RedisSession.set_url('{}_room_ls'.format(key), result)
            logger.info("添加完成")
        except (NotMenuError, NotDigitError) as e:
            logger.error(e)
            continue
        except BreakProgram:
            break


if __name__ == '__main__':
    add_urls_run()

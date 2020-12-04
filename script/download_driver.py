import os
import re
import zipfile
import requests
from utils.utils import get_canonical_os_name, locate_web_driver
from utils.log import logger

platform_map = {"windows": "win32", "mac": "mac64", "linux": "linux64"}
download_url = "https://npm.taobao.org/mirrors/chromedriver/{}/chromedriver_{}.zip"

driver_dir = locate_web_driver()
platform_dir = os.path.dirname(driver_dir)


def get_version_url(version):
    resp = requests.get("https://npm.taobao.org/mirrors/chromedriver")
    resp_text = resp.content.decode("utf-8")
    if re.search(r"chromedriver/{}/".format(version), resp_text):
        return version
    else:
        version_ls = re.findall(r"chromedriver/({}.*?)/".format(version.split(".")[0]), resp_text)
        if version_ls:
            return version_ls[-1]
        return None


def download(version):
    logger.info("正在查询版本号")
    new_version = get_version_url(version)
    if new_version:
        logger.info("正在下载")
        if not os.path.exists(platform_dir):
            os.makedirs(platform_dir)
        platform = platform_map[get_canonical_os_name()]
        resp = requests.get(download_url.format(new_version, platform), stream=True)
        download_dir = os.path.join(platform_dir, "chromedriver_{}.zip".format(platform))
        with open(download_dir, "wb") as f:
            for data in resp.iter_content(chunk_size=1024):
                f.write(data)
        zip_file = zipfile.ZipFile(download_dir)
        zip_list = zip_file.namelist()
        for f in zip_list:
            zip_file.extract(f, platform_dir)
        zip_file.close()
        os.remove(download_dir)
        logger.info("下载完成")
    else:
        logger.info("未找到对应版本号,请检查重新下载")


def download_driver_run():
    if os.path.exists(driver_dir):
        logger.info("驱动存在")
    else:
        logger.info("未找到驱动,请下载")
        version = input("请输入你的chrome版本号:").strip()
        download(version)


if __name__ == '__main__':
    download_driver_run()

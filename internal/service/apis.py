import random

import requests

from internal.utils.log import LOGGER


def random_2th_img_resp():
    rd = random.randint(0, 1)
    res = ""
    if rd == 0:
        LOGGER.info("xjh")
        resp = requests.get("https://img.xjh.me/random_img.php?return=json")
        res = resp.json()["img"]
        return "[CQ:image,file=https:{}]".format(res)
    elif rd == 1:
        LOGGER.info("sakura")
        resp = requests.get("https://www.dmoe.cc/random.php?return=json")
        print(resp.json())
        res = resp.json()["imgurl"].replace("https://", "")
        return "[CQ:image,file=https://{}]".format(res)

def random_cos_img_resp():
    r_cos = str(requests.get("http://api.rosysun.cn/cos").text)
    return "[CQ:image,file={image}]".format(image=r_cos)
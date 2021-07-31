import random

import requests
import time

from internal.utils.json_reader import json_reader
from internal.utils.log import LOGGER

bot_resp = json_reader("static/bot_response/bot_resp.json")  # object array


def random_vtb_id():
    all_vtb = query_vtb_all()
    online_ones = []
    for item in all_vtb:
        if item["online"] != 0:
            online_ones.append(item)
    _len = len(online_ones)
    rd = random.randint(0, _len - 1)
    return online_ones[rd]


def random_vtb_info():
    r_vtb = random_vtb_id()
    LOGGER.info("vtb info{}".format(str(r_vtb)))
    resp = "VTB:{title}\n[CQ:image,file={image}]\n直播间标题：{content}\n直播间链接：https://live.bilibili.com/{roomid}\n".format(
        title=r_vtb["uname"], image=r_vtb["face"], content=r_vtb["title"], roomid=r_vtb['roomid'])
    return resp


def random_response():
    rd = random.randint(0, len(bot_resp) - 1)
    resp = bot_resp[rd]["content"]
    if resp == "随机vtb":
        resp = random_vtb_info()
        LOGGER.info(resp)
    return resp


def query_vtb_all():
    full_info = requests.get("https://api.vtbs.moe/v1/fullInfo")
    return full_info.json()


def query_vtb(request_json):
    all_vtb = query_vtb_all()
    _message_replace_at = str(
        request_json["message"].replace("[CQ:at,qq=1728158137]", "").replace("[CQ:at,qq=1728158137] ",
                                                                             "").replace(" ", ""))
    _name = _message_replace_at.split("查询vtb@")
    _name = _name[len(_name) - 1]
    result = []
    for item in all_vtb:
        # print(item)
        if _name.upper() in item["uname"].upper():
            LOGGER.info("匹配到内容:{}".format(str(item["uname"])))
            status = "在播" if item["online"] != 0 else "没播"
            if status == "在播":
                lt_pre = item['time']
            else:
                lt_pre = item['lastLive']["time"] if item['lastLive'] else 0
            if lt_pre != 0:
                lt = time.localtime(int(str(lt_pre)[:10]))
                last_time = time.strftime("%Y-%m-%d/%H:%M:%S", lt)
            else:
                last_time = "时间消失在石头门里面了..."
            result.append(
                "VTB:{}\n[CQ:image,file={}]\n直播间标题：{}\n直播状态：{}\n最近开播时间：{}\n直播间链接：https://live.bilibili.com/{}\n".format(
                    item["uname"], item["face"],
                    item["title"], status,
                    last_time, item['roomid']))
    res_str = ""
    if len(result) != 0:
        for item in result:
            res_str += item + "---------\n"
        return res_str
    else:
        return "空空如也捏"

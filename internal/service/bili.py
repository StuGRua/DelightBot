import random

import requests
import time

from internal.utils.json_reader import json_reader
from internal.utils.log import LOGGER


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

def query_vtb_all():
    full_info = requests.get("https://api.vtbs.moe/v1/fullInfo")
    return full_info.json()


def query_vtb(_name: str):
    all_vtb = query_vtb_all()

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


def query_player_status_str(_name: str):
    resp_room = requests.get("https://api.live.bilibili.com/room/v1/Room/room_init", params={"id": int(_name), }).json()

    if resp_room["code"] != 0:
        return "直播间不存在哦"
    else:
        room_data = resp_room["data"]
        status = "在播" if room_data["live_status"] == 1 else "没播"
        if room_data["live_time"] < 0:
            room_data["live_time"] = 0
        LOGGER.info(str(room_data))
        lt = time.localtime(room_data["live_time"])
        last_time = time.strftime("%Y-%m-%d/%H:%M:%S", lt)
        user_resp = requests.get("http://api.live.bilibili.com/live_user/v1/Master/info",
                                 params={"uid": room_data["uid"], }).json()
        user_data = user_resp["data"]["info"]
        if room_data["live_time"] == 0:
            fin_resp = "主播：{}\n直播状态：{}\n".format(user_data["uname"], status)
        else:
            fin_resp = "主播：{}\n直播状态：{}\n开播时间：{}\n".format(user_data["uname"], status, last_time)
        return fin_resp


def query_player_from_rid(rid:int):
    resp_room = requests.get("https://api.live.bilibili.com/room/v1/Room/room_init", params={"id": rid}).json()
    return resp_room

# def get_info_from_rid(rid: int) -> dict:
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
#     }
#     resp = requests.get("https://api.live.bilibili.com/room/v1/Room/room_init?id="+str(rid), headers=headers).json()
#     return resp


# def get_status_from_rid(rid: int):
#     """
#
#     :param rid: 房间id
#     :return: 播放状态 0：未开播 1：直播中
#     """
#     mid_dict = get_info_from_rid(rid)
#     print(mid_dict)
#     status = mid_dict["data"]["live_status"]
#     return status

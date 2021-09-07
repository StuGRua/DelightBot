import json

import requests

from internal.dao.redis_client import get_conn
from internal.utils.log import LOGGER
from internal.service.bili import query_player_from_rid
from internal.service.robot_send_message import robot_send_group_message


def check_single_room(gid: int, rid: int):
    """

    """
    info = query_player_from_rid(rid)
    stat = str(info["data"]["live_status"])
    query_rid = "bili_player_status:{}".format(str(rid))
    with get_conn() as r:
        redis_stat = r.get(query_rid)  # 读当前通知状态
        print(type(redis_stat), redis_stat)
        # 在播
        if stat == "1":
            # 在线心跳
            if redis_stat == "1":
                r.set(query_rid, 1, ex=120)
                # LOGGER.info("doki doki")
                return

            # 检测到开播 redis_stat= 0/2 -> redis_stat = 1
            else:
                user_resp = requests.get("http://api.live.bilibili.com/live_user/v1/Master/info",
                                         params={"uid": info["data"]["uid"], }).json()
                user_data = user_resp["data"]["info"]
                # LOGGER.info("[DD]开播辣")
                r.set(query_rid, 1, ex=120)
                message_sent = "[凯撒喵喵-开播广播]\n主播：{}\n传送门：{}".format(user_data["uname"],
                                                                   "https://live.bilibili.com/" + str(
                                                                       rid))
                print(message_sent)
                robot_send_group_message(gid, message_sent)
        # 离线或轮播 0或2
        else:
            # LOGGER.info("[DD]主播没有在播捏")
            r.set(query_rid, stat, ex=120)


def check_all_players():
    with get_conn() as r:
        dd_rooms_raw = r.get("DDRooms")
    dd_rooms = json.loads(dd_rooms_raw)
    assert type(dd_rooms) == dict
    if dd_rooms:
        dd_rooms = dd_rooms
    else:
        dd_rooms = dict()
    for k, v in dd_rooms.items():
        assert type(v) == list
        for item in v:
            check_single_room(int(k), item)


if __name__ == "__main__":
    check_all_players()

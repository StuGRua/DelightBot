import json

import requests

from internal.dao.redis_client import get_conn
from internal.utils.log import LOGGER
from internal.service.bili import query_player_from_rid
from internal.service.robot_send_message import robot_send_group_message


def check_single_room(rid: int):
    """
    检查房间
    :param rid: 房间号
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
                LOGGER.info("doki doki")
                return

            # 检测到开播 redis_stat= 0/2 -> redis_stat = 1
            else:
                user_resp = requests.get("http://api.live.bilibili.com/live_user/v1/Master/info",
                                         params={"uid": info["data"]["uid"], }).json()
                user_data = user_resp["data"]["info"]
                LOGGER.info("[DD]开播辣")
                r.set(query_rid, 1)
                message_sent = "[凯撒喵喵-开播广播]\n主播：{}\n传送门：{}".format(user_data["uname"],
                                                                   "https://live.bilibili.com/" + str(
                                                                       rid))
                print(message_sent)
                groups = json.loads(r.get("dd_groups"))
                LOGGER.info()
                assert type(groups) == list
                for gp in groups:
                    LOGGER.info(gp)
                    robot_send_group_message(gp, message_sent)
        # 离线或轮播 0或2
        else:
            LOGGER.info("[DD]主播没有在播捏")
            r.set(query_rid, stat)


def check_all_players():
    with get_conn() as r:
        DD_rooms_str = r.get("DD_rooms")
    DD_rooms = json.loads(DD_rooms_str)
    assert type(DD_rooms) == list
    if DD_rooms:
        dd_rooms = DD_rooms
    else:
        dd_rooms = []
    for item in dd_rooms:
        check_single_room(item)


if __name__ == "__main__":
    check_all_players()

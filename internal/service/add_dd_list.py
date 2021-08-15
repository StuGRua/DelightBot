import json

from internal.dao.redis_client import get_conn
from internal.utils.log import LOGGER
from internal.service.bili import query_player_from_rid


def add_dd(dd_room: int):
    with get_conn() as r:
        if not r.exists("DD_rooms"):
            LOGGER.info("[DD ADD]DD_rooms in redis not exist..")
            return False
        # DD_rooms序列已初始化
        else:
            now_dds = json.loads(r.get("DD_rooms"))
            LOGGER.info("[DD ADD]DD_rooms now:{}".format(str(now_dds)))
            assert type(now_dds) == list
            # 不存在redis的list中
            if dd_room not in now_dds and dd_room > 0:
                #  查询房间是否存在
                query_result = query_player_from_rid(dd_room)["code"]
                # 不存在
                if query_result == 60004:
                    LOGGER.info("[DD ADD]room not existed")
                    return "房间不存在"
                now_dds.append(dd_room)
                # 去重
                now_dds = list(set(now_dds))
                assert type(now_dds) == list
                result = r.set("DD_rooms", json.dumps(now_dds))
                if result in [1, "1"]:
                    LOGGER.info("[DD ADD]success")
                else:
                    LOGGER.info("[DD ADD]failed")
                return "DD添加成功，rid={}".format(str(dd_room))
            elif dd_room*(-1) in now_dds and dd_room < 0:
                now_dds.remove(dd_room*(-1))
                result = r.set("DD_rooms", json.dumps(now_dds))
                return "DD删除成功，rid={}".format(str(dd_room))
            else:
                return "DD不太对劲..."

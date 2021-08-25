import json

import config
from internal.dao.redis_client import get_conn
from internal.dao.redis_group_welcome import set_greeting_msg


def init_all_config_to_redis():
    init_groups()
    init_dds()
    init_welcome()


def init_groups():
    set_kv_redis("dd_groups", json.dumps(config.DD_groups))


def init_dds():
    gp_values = list(config.DD_players.values())
    set_kv_redis("DD_rooms", json.dumps(gp_values))


# 初始化启用迎宾的群
def init_welcome():
    set_greeting_msg(514394960, '{"1":"|･ω･｀)","2":"欢迎新朋友~||--来自罗伯特喵喵的自动问候~"}')
    set_greeting_msg(1061794747, '{"1":"|･ω･｀)","2":"欢迎新朋友~||--来自罗伯特喵喵的自动问候~"}')
    # print("初始化老哥群欢迎语")


def set_kv_redis(k: str, v: str):
    with get_conn() as r:
        if r.exists(k):
            return
        r.set(k, v)


if __name__ == "__main__":
    init_all_config_to_redis()

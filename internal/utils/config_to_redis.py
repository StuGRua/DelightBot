import json

import config
from internal.dao.redis_client import get_conn


def init_all_config_to_redis():
    init_groups()
    init_dds()


def init_groups():
    set_kv_redis("dd_groups",json.dumps(config.DD_groups))


def init_dds():
    gp_values = list(config.DD_players.values())
    set_kv_redis("DD_rooms", json.dumps(gp_values))


def set_kv_redis(k: str, v: str):
    with get_conn() as r:
        if r.exists(k):
            return
        r.set(k, v)

if __name__ =="__main__":
    init_all_config_to_redis()

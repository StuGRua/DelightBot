from internal.dao.redis_client import get_conn


def update_cos_pics(pics: list):
    with get_conn() as r:
        r.sadd("cos_pics", *pics)


def get_cos_pics_all() -> list:
    with get_conn() as r:
        return list(r.smembers("cos_pics"))


def get_random_cos_pic() -> str:
    with get_conn() as r:
        return r.srandmember("cos_pics")

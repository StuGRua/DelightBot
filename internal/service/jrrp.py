import datetime
from internal.dao.redis_client import get_conn
from internal.utils.log import LOGGER


def jrrp(userid: int):
    uid = str(userid)
    with get_conn() as r:
        res = r.get(name="jrrp:{}".format(uid))
        if res is not None:
            LOGGER.info("jrrp已存在，直接读取：{}".format(res))
            rp = res
        else:
            time_today = datetime.datetime.now().strftime("%Y-%m-%d")
            rp_str = str(hash(uid + time_today))
            rp = rp_str[len(rp_str) - 2:]
            LOGGER.info("jrrp不存在，重新生成：{}".format(rp))
            r.set(name="jrrp:{}".format(uid), value=rp, ex=60*60*24)
    resp_level = ""
    if int(rp) <= 20:
        resp_level = "哇呜，你今天有点惨"
    elif 20 < int(rp) <= 60:
        resp_level = "看来还得加把劲啊"
    elif 60 < int(rp) <= 80:
        resp_level = "好像运气还可以诶"
    elif 80 < int(rp) <= 98:
        resp_level = "今日海豹"
    elif int(rp) == 99:
        resp_level = "欧皇！"

    return rp, resp_level

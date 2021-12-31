import datetime
from typing import List

from internal.dao.redis_client import get_conn
from internal.interface.cq_client import get_group_members
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
            # sp:12.25/12.26
            # rp = 99
            LOGGER.info("jrrp不存在，重新生成：{}".format(rp))
            r.set(name="jrrp:{}".format(uid), value=rp, ex=get_exp_time_4am())
        ttl = r.ttl(name="jrrp:{}".format(uid)) / 3600
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
    resp_level += "\n下次可刷新：{:.2f}小时后".format(ttl)
    return rp, resp_level


def jrrp_cal(group_id: int) -> str:
    mem = get_group_members(group_id)
    mem_dic = dict()
    print(mem)
    for item in mem:
        print(item)
        mem_dic[item["user_id"]] = item
    with get_conn() as r:
        res = r.keys("jrrp:*")
        print(res)
        tmp = []
        for item in res:
            score = int(r.get(item))
            ttl = r.ttl(item) / 3600
            tmp.append({"uid": item.replace("jrrp:", ""), "score": score, "ttl": ttl,
                        "nickname": mem_dic[int(item.replace("jrrp:", ""))]["nickname"]})
    sd = sorted(tmp, key=lambda x: x["score"], reverse=True)
    rk99mem = []
    rk80mem = []
    rk60mem = []
    rk20mem = []
    rk0mem = []
    for item in sd:
        if item["score"] == 99:
            rk99mem.append(item)
        if item["score"] in range(80, 98):
            rk80mem.append(item)
        if item["score"] in range(60, 79):
            rk60mem.append(item)
        if item["score"] in range(20, 60):
            rk20mem.append(item)
        if item["score"] in range(0, 20):
            rk0mem.append(item)
    rk1 = rp_str("罗马", rk99mem)
    rk2 = rp_str("上等马", rk80mem)
    rk3 = rp_str("中等马", rk60mem)
    rk4 = rp_str("下等马", rk20mem)
    rk5 = rp_str("纯纯牛马", rk0mem)
    res_str = "每日🐂🐴统计：\n{}\n{}\n{}\n{}\n{}".format(rk1, rk2, rk3, rk4, rk5)
    print(res_str)
    return res_str


def rp_str(level_name: str, items: List[dict]) -> str:
    if len(items) == 0:
        return ""
    ss = "{}:\n".format(level_name)
    for item in items:
        ss += "{} : {}\n".format(item["nickname"], item["score"])
    return ss


def get_exp_time_4am() -> int:
    ex = datetime.datetime.now().timetuple()
    if ex.tm_hour < 4:
        # 0-4点
        ex_time = datetime.datetime(ex.tm_year, ex.tm_mon, ex.tm_mday) + datetime.timedelta(hours=4)
    else:
        ex_time = datetime.datetime(ex.tm_year, ex.tm_mon, ex.tm_mday) + datetime.timedelta(days=1, hours=4)
    exp_range_time = int(ex_time.timestamp() - datetime.datetime.now().timestamp())
    return exp_range_time

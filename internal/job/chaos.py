from datetime import datetime
from functools import wraps
import requests
import random
from config import bot_host
from internal.service.cos.random_cos import random_cos
from internal.job.lolicon_pic import random_lolicon
from internal.service.srv_list import srv_list
from internal.dao.redis_chaos import add_chaos_time
# 初始化调度器
from internal.utils.json_reader import json_reader, json_writer

__group = 514394960


# TODO:罗伯特今天吃什么
# TODO:推送开关
def bot_reply_header(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        pre_resp = f(*args, **kwargs)
        resp = {"reply": pre_resp}
        return resp

    return decorated


def chaos_func():
    if 3 <= datetime.now().hour <= 8:
        print("night ver.")
        return
    t = add_chaos_time()
    srv_list.extend([random_cos])
    rf = random.randint(0, len(srv_list) - 1)
    resp = srv_list[rf]()
    body = {
        "group_id": __group,
        "message": "凯撒罗伯特喵喵电台：\n总次数：{}\n".format(str(t)) + resp,
    }
    try:
        resp = requests.post(url="{}/send_group_msg".format(bot_host["main"]), json=body)
    except Exception as e:
        pass
    print(body)


if __name__ == "__main__":
    chaos_func()

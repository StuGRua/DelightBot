from functools import wraps

import requests
import random
from internal.flask_core.core import app
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from config import bot_host
from internal.service.srv_list import srv_list
# 初始化调度器
from internal.utils.json_reader import json_reader, json_writer

scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))

__group = 514394960

def bot_reply_header(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        pre_resp = f(*args, **kwargs)
        resp = {"reply": pre_resp}
        return resp

    return decorated


@scheduler.task('interval', id='chaos_func', seconds=1000, misfire_grace_time=900)
def chaos_func():
    t = json_reader("static/times.json")
    t["chaos_times"] += 1
    json_writer("static/times.json", t)
    rf = random.randint(0,len(srv_list)-1)
    resp = srv_list[rf]()
    body = {
        "group_id": __group,
        "message": "凯撒罗伯特喵喵电台：\n总次数：{}\n".format(str(t))+resp,
    }
    resp = requests.post(url="{}/send_group_msg".format(bot_host["main"]), json=body)
    print(resp)

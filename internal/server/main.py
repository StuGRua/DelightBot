import json
import time
from functools import wraps
import requests
from flask import request, Flask, g
from internal.dao.redis_bili_cos_pics import get_cos_pics_all
from internal.dao.redis_request_limiter import limiter_user_func
from internal.service.aliyun_oss import random_audio_zjw
from internal.service.apis import random_2th_img_resp
from internal.service.random_response import random_response
from internal.service.bili import random_vtb_id, query_vtb, query_player_status_str
from internal.service.cos.random_cos import random_cos
from internal.service.jrrp import jrrp
from internal.service.mc import get_mc_mods_from_gitee, get_ms_status
from internal.utils.log import LOGGER
from internal.service.what_we_eat import query_food
from internal.service.add_dd_list import add_dd
from internal.service.event.group_welcome import group_welcome_handler
from config import BotAccount

app = Flask("RBT")
__at_account = "[CQ:at,qq={}]".format(BotAccount.srv_account)


def quick_reply(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        is_limit = limiter_user_func(g.rj["sender"]["user_id"], f.__name__)
        if is_limit != 0:
            return {"reply": "我真的怀疑有的人的闲的程度啊[CD:{}s]".format(is_limit), "at_sender": True}
        get_item = []
        for item in args:
            get_item.append(item)
        pre_resp = f(*args, **kwargs)
        resp = {"reply": pre_resp, "at_sender": True}
        return resp

    return decorated


@quick_reply
def tts_message_test():
    return "[CQ:tts,text=不要停下来啊]"


@quick_reply
def srv_jrrp():
    request_json = g.rj
    uid = request_json["sender"]["user_id"]
    rp, resp_level = jrrp(uid)
    return "今日人品：{}\n{}".format(rp, resp_level)


@quick_reply
def resp_your_question_mark():
    """

    :return:
    """
    return "[CQ:image,file=https://raw.githubusercontent.com/StuGRua/DelightBot/main/static/bot_image/question_lol.jpg]"


@quick_reply
def random_2th_img():
    """
    :return:
    """
    return random_2th_img_resp()


@quick_reply
def query_510_status():
    """
    :return:
    """
    return query_vtb("阿梓")


@quick_reply
def query_specific_vtb():
    request_json = g.rj
    _name = request_json["message"].split("查询vtb@")
    _name = _name[len(_name) - 1]
    return query_vtb(_name)


@quick_reply
def query_room_and_player():
    request_json = g.rj
    _name = request_json["message"].split("查询主播-")
    _name = _name[len(_name) - 1]
    return query_player_status_str(_name)


@quick_reply
def illegal_request():
    return random_response()


@quick_reply
def query_minecraft_server():
    return get_ms_status()


@quick_reply
def help_me():
    pre_str = "帮助info：\n[CQ:image,file=https://raw.githubusercontent.com/StuGRua/DelightBot/main/static/bot_image/helpme.png]"
    return pre_str


@quick_reply
def get_mc_mods():
    return get_mc_mods_from_gitee()


@quick_reply
def random_vtb_as_query():
    r_vtb = random_vtb_id()
    resp = "VTB:{title}\n[CQ:image,file={image}]\n直播间标题：{content}\n直播间链接：https://live.bilibili.com/{roomid}\n".format(
        title=r_vtb["uname"], image=r_vtb["face"], content=r_vtb["title"], roomid=r_vtb['roomid'])
    return resp


@quick_reply
def random_cos_pic():
    return random_cos()


@quick_reply
def weibo_hot_now():
    wh = json.loads(requests.get("http://api.rosysun.cn/weibo/").content)
    wh = wh["data"]
    resp_str = ""
    for item in wh:
        resp_str += "{}\n{}\n".format(item["title"], item["url"])
    return resp_str


@quick_reply
def add_dd_interface():
    request_json = g.rj
    rid = request_json["message"].split("添加DD=")
    rid = rid[len(rid) - 1]
    res = add_dd(int(rid))
    pre_str = ""
    if res:
        pre_str += res
    else:
        pre_str += res
    return pre_str


@quick_reply
def eat_what():
    return query_food()


def at_bot_message_fixer(rj: dict) -> bool:
    if "message" not in rj:
        LOGGER.info("no message in req json")
        return False
    rj["message"] = rj["message"].replace(__at_account, "").replace(" ", "")
    return True


@app.route('/', methods=['POST'])
def receive():
    rj = request.json
    g.rj = rj
    at_bot_message_fixer(rj)
    _message_replace_at = rj["message"]
    if "!jrrp" in _message_replace_at or "！jrrp" in _message_replace_at:
        return srv_jrrp()
    elif _message_replace_at == "？" or _message_replace_at == "?":
        return resp_your_question_mark()
    elif "来点二次元" in _message_replace_at or "老婆" in _message_replace_at:
        return random_2th_img()
    elif "开门" == _message_replace_at:
        return query_510_status()
    elif "查询vtb@" in _message_replace_at:
        return query_specific_vtb()
    elif "查询主播-" in _message_replace_at:
        return query_room_and_player()
    elif "MC" == _message_replace_at.upper():
        return query_minecraft_server()
    elif "MCMOD" == _message_replace_at.upper():
        return get_mc_mods()
    elif "随机vtb" == _message_replace_at:
        return random_vtb_as_query()
    elif "害怕" == _message_replace_at or "我兄弟" in _message_replace_at:
        return random_audio_zjw()
    elif "随机cos" == _message_replace_at:
        return random_cos_pic()
    elif "微博" in _message_replace_at:
        return weibo_hot_now()
    elif "吃什么" in _message_replace_at:
        return eat_what()
    elif "添加DD=" in _message_replace_at:
        return add_dd_interface()
    elif "帮帮我" == _message_replace_at or "help" == _message_replace_at:
        return help_me()
    elif "团长你在干什么啊" == _message_replace_at:
        return tts_message_test()
    else:
        LOGGER.warning("未知命令")
        return illegal_request()


@app.route('/event', methods=['POST'])
def event_handler():
    rj = request.json
    group_welcome_handler(rj)
    return ""


@app.route('/all_pics', methods=['GET'])
def all_pics():
    return json.dumps(get_cos_pics_all())

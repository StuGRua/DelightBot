import json
import time
from functools import wraps

import requests
from flask import request, Flask
from internal.service.aliyun_oss import random_audio_zjw
from internal.service.apis import random_2th_img_resp, random_cos_img_resp
from internal.service.bili import random_vtb_id, random_response, query_vtb, query_vtb_all, query_player
from internal.service.jrrp import jrrp
from internal.service.mc import get_mc_mods_from_gitee, get_ms_status
from internal.utils.log import LOGGER

app = Flask("RBT")


def quick_reply(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        get_item = []
        for item in args:
            get_item.append(item)
        _uid = get_item[0]["sender"]["user_id"]
        pre_resp = f(*args, **kwargs)
        resp = {"reply": "[CQ:at,qq={}] \n".format(str(_uid)) + pre_resp}
        LOGGER.info(str(resp))
        return resp

    return decorated


@quick_reply
def srv_jrrp(request_json):
    uid = request_json["sender"]["user_id"]
    rp, resp_level = jrrp(uid)
    return "今日人品：{}\n{}".format(rp, resp_level)


@quick_reply
def resp_your_question_mark(request_json):
    """

    :return:
    """
    return "[CQ:image,file=https://raw.githubusercontent.com/StuGRua/DelightBot/main/static/bot_image/question_lol.jpg]"


@quick_reply
def random_2th_img(request_json):
    """

    :param request_json:
    :return:
    """
    return random_2th_img_resp()


@quick_reply
def query_510_status(request_json):
    """
    :return:
    """
    return query_vtb("阿梓")


@quick_reply
def query_specific_vtb(request_json):
    _message_replace_at = str(
        request_json["message"].replace("[CQ:at,qq=1728158137]", "").replace("[CQ:at,qq=1728158137] ",
                                                                             "").replace(" ", ""))
    _name = _message_replace_at.split("查询vtb@")
    _name = _name[len(_name) - 1]
    return query_vtb(_name)


@quick_reply
def query_room_and_player(request_json):
    _message_replace_at = str(
        request_json["message"].replace("[CQ:at,qq=1728158137]", "").replace("[CQ:at,qq=1728158137] ",
                                                                             "").replace(" ", ""))
    _name = _message_replace_at.split("查询主播-")
    _name = _name[len(_name) - 1]
    return query_player(_name)


@quick_reply
def illegal_request(request_json):
    return random_response()


@quick_reply
def query_minecraft_server(request_json):
    return get_ms_status()


@quick_reply
def help_me(request_json):
    pre_str = "帮助info：\n[CQ:image,file=https://raw.githubusercontent.com/StuGRua/DelightBot/main/static/bot_image/helpme.png]"
    return pre_str


@quick_reply
def get_mc_mods(request_json):
    return get_mc_mods_from_gitee()


@quick_reply
def random_vtb_as_query(request_json):
    r_vtb = random_vtb_id()
    resp = "VTB:{title}\n[CQ:image,file={image}]\n直播间标题：{content}\n直播间链接：https://live.bilibili.com/{roomid}\n".format(
        title=r_vtb["uname"], image=r_vtb["face"], content=r_vtb["title"], roomid=r_vtb['roomid'])
    return resp


@quick_reply
def random_cos_pic(request_json):
    return random_cos_img_resp()


@quick_reply
def weibo_hot_now(request_json):
    wh = json.loads(requests.get("http://api.rosysun.cn/weibo/").content)
    wh = wh["data"]
    resp_str = ""
    for item in wh:
        resp_str += "{}\n{}\n".format(item["title"], item["url"])
    return resp_str


@app.route('/', methods=['POST'])
def receive():
    rj = request.json
    LOGGER.info(str(rj))
    _message_replace_at = rj["message"].replace("[CQ:at,qq=1728158137]", "").replace("[CQ:at,qq=1728158137] ",
                                                                                     "").replace(" ", "")
    LOGGER.info(_message_replace_at)
    if "!jrrp" in _message_replace_at:
        return srv_jrrp(rj)
    elif _message_replace_at == "？" or _message_replace_at == "?":
        return resp_your_question_mark(rj)
    elif "来点二次元" in _message_replace_at or "老婆" in _message_replace_at:
        return random_2th_img(rj)
    elif "开门" == _message_replace_at:
        return query_510_status(rj)
    elif "查询vtb@" in _message_replace_at:
        return query_specific_vtb(rj)
    elif "查询主播-" in _message_replace_at:
        return query_room_and_player(rj)
    elif "MC" == _message_replace_at.upper():
        return query_minecraft_server(rj)
    elif "MCMOD" == _message_replace_at.upper():
        return get_mc_mods(rj)
    elif "随机vtb" == _message_replace_at:
        return random_vtb_as_query(rj)
    elif "害怕" == _message_replace_at or "我兄弟" in _message_replace_at:
        return random_audio_zjw(rj)
    elif "随机cos" == _message_replace_at:
        return random_cos_pic(rj)
    elif "微博" in _message_replace_at:
        return weibo_hot_now(rj)
    elif "帮帮我" == _message_replace_at or "help" == _message_replace_at:
        return help_me(rj)
    else:
        LOGGER.warning("未知命令")
        return illegal_request(rj)

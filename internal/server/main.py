import datetime
import hmac
import time
import requests
from functools import wraps
from flask import Flask, request, jsonify
import re

app = Flask(__name__)


def quick_reply(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        get_item = []
        for item in args:
            get_item.append(item)
        print(get_item)
        _uid = get_item[0]["sender"]["user_id"]
        print(_uid)
        pre_resp = f(*args, **kwargs)
        resp = {"reply": "[CQ:at,qq={}] \n".format(str(_uid)) + pre_resp}
        return resp

    return decorated


@quick_reply
def jrrp(request_json):
    uid = str(request_json["sender"]["user_id"])
    time_today = datetime.datetime.now().strftime("%Y-%m-%d")
    rp_str = str(hash(uid + time_today))
    rp = rp_str[len(rp_str) - 2:]
    print(rp)
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
    # print(request.json)
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
    resp = requests.get("https://img.xjh.me/random_img.php?return=json")
    res = resp.json()["img"]
    print(res)
    return "[CQ:image,file=https:{}]".format(res)


@quick_reply
def query_510_status(request_json):
    """

    :return:
    """
    all_vtb = query_vtb_all()
    for item in all_vtb:
        print(item)
        if item["uname"] == "阿梓从小就很可爱":
            status = "在播" if item["online"] == 1 else "没播"
            return "VTB:{}\n直播间标题：{}\n直播状态：{}".format(item["uname"], item["title"], status)


@quick_reply
def query_specific_vtb(request_json):
    all_vtb = query_vtb_all()
    _message_replace_at = str(
        request_json["message"].replace("[CQ:at,qq=1728158137]", "").replace("[CQ:at,qq=1728158137] ",
                                                                             "").replace(" ", ""))
    _name = _message_replace_at.split("查询vtb@")
    _name = _name[len(_name) - 1]
    result = []
    for item in all_vtb:
        # print(item)
        if _name.upper() in item["uname"].upper():
            print("匹配ing")
            print(item)
            status = "在播" if item["online"] != 0 else "没播"
            lt = time.localtime(int(str(item['lastLive']["time"])[:10]))
            last_time = time.strftime("%Y-%m-%d %H:%M:%S", lt)
            result.append(
                "VTB:{}\n直播间标题：{}\n直播状态：{}\n最近开播时间：{}\n".format(item["uname"], item["title"], status, last_time))
    res_str = ""
    print(result)
    if len(result) != 0:
        for item in result:
            res_str += item + "---------\n"
        return res_str
    else:
        return "空空如也捏"


def query_vtb_all():
    full_info = requests.get("https://api.vtbs.moe/v1/fullInfo")
    return full_info.json()


func_entry = {
    "jrrp": jrrp,

}


@app.route('/', methods=['POST'])
def receive():
    rj = request.json
    print(rj)
    _message_replace_at = rj["message"].replace("[CQ:at,qq=1728158137]", "").replace("[CQ:at,qq=1728158137] ",
                                                                                     "").replace(" ", "")
    print(_message_replace_at)
    if "!jrrp" in _message_replace_at:
        return jsonify(jrrp(rj))
    elif _message_replace_at == "？" or _message_replace_at == "?":
        return resp_your_question_mark(rj)
    elif "来点二次元" in _message_replace_at or "老婆" in _message_replace_at:
        return random_2th_img(rj)
    elif "开门" == _message_replace_at:
        return query_510_status(rj)
    elif "查询vtb@" in _message_replace_at:
        return query_specific_vtb(rj)
    else:
        print("未知命令")
        return jsonify({"reply": "李在赣神魔，我怎么听不懂"})

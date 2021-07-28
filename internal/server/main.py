import datetime
import hmac
import time
from functools import wraps
from flask import Flask, request, jsonify

app = Flask(__name__)


def quick_reply(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        get_item = []
        for item in args:
            get_item.append(item)
        _uid = get_item[0]["sender"]["user_id"]
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
    return "[CQ:image,file=./static/bot_image/question_lol.jpg]"


func_entry = {
    "jrrp": jrrp,

}


@app.route('/', methods=['POST'])
def receive():
    rj = request.json
    print(rj)
    _message_replace_at = rj["message"].replace("[CQ:at,qq=1728158137]", "").replace("[CQ:at,qq=1728158137] ", "")
    if "!jrrp" in _message_replace_at:
        return jsonify(jrrp(rj))
    elif _message_replace_at == "？" or _message_replace_at == "?":
        return resp_your_question_mark(rj)
    else:
        print("未知命令")
        return jsonify({"reply": "李在赣神魔，我怎么听不懂"})

import datetime
import hmac
import time

from flask import Flask, request, jsonify

app = Flask(__name__)


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
    return {"reply": "[CQ:at,qq={}] \n今日人品：{}\n{}".format(uid, rp, resp_level)}


func_entry = {
    "jrrp": jrrp,
}


@app.route('/', methods=['POST'])
def receive():
    rj = request.json
    print(rj)
    if "!jrrp" in rj["message"]:
        return jsonify(jrrp(rj))
    else:
        print("未知命令")
        return jsonify({"reply": "李在赣神魔，我怎么听不懂"})

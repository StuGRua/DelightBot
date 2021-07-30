import datetime
import hmac
import json
import random
import time
import requests
from functools import wraps
from flask import Flask, request, jsonify, redirect
from internal.utils.json_reader import json_reader
from internal.utils.log import LOGGER
from config import server_config, minecrafr_server

bot_resp = json_reader("static/bot_response/bot_resp.json")  # object array

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
    rd = random.randint(0, 1)
    res = ""
    if rd == 0:
        LOGGER.info("xjh")
        resp = requests.get("https://img.xjh.me/random_img.php?return=json")
        res = resp.json()["img"]
        return "[CQ:image,file=https:{}]".format(res)
    elif rd == 1:
        LOGGER.info("sakura")
        resp = requests.get("https://www.dmoe.cc/random.php?return=json")
        print(resp.json())
        res = resp.json()["imgurl"].replace("https://", "")
        return "[CQ:image,file=https://{}]".format(res)


@quick_reply
def query_510_status(request_json):
    """
    :return:
    """
    all_vtb = query_vtb_all()
    for item in all_vtb:
        if item["uname"] == "阿梓从小就很可爱":
            status = "在播" if item["online"] != 0 else "没播"
            if status == "在播":
                lt_pre = item['time']
            else:
                lt_pre = item['lastLive']["time"]
            lt = time.localtime(int(str(lt_pre)[:10]))
            last_time = time.strftime("%Y-%m-%d/%H:%M:%S", lt)
            return "{}\n[CQ:image,file={}]\n直播间标题：{}\n直播状态：{}\n最近开播时间：{}\n直播间链接：https://live.bilibili.com/{}\n".format(
                item["uname"], item["face"],
                item["title"], status,
                last_time, item['roomid'])


@quick_reply
def query_specific_vtb(request_json):
    return query_vtb(request_json)


def query_vtb(request_json):
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
            LOGGER.info("匹配到内容:{}".format(str(item["uname"])))
            status = "在播" if item["online"] != 0 else "没播"
            if status == "在播":
                lt_pre = item['time']
            else:
                lt_pre = item['lastLive']["time"] if item['lastLive'] else 0
            if lt_pre != 0:
                lt = time.localtime(int(str(lt_pre)[:10]))
                last_time = time.strftime("%Y-%m-%d/%H:%M:%S", lt)
            else:
                last_time = "时间消失在石头门里面了..."
            result.append(
                "VTB:{}\n[CQ:image,file={}]\n直播间标题：{}\n直播状态：{}\n最近开播时间：{}\n直播间链接：https://live.bilibili.com/{}\n".format(
                    item["uname"], item["face"],
                    item["title"], status,
                    last_time, item['roomid']))
    res_str = ""
    if len(result) != 0:
        for item in result:
            res_str += item + "---------\n"
        return res_str
    else:
        return "空空如也捏"


def random_vtb():
    all_vtb = query_vtb_all()
    online_ones = []
    for item in all_vtb:
        if item["online"] != 0:
            online_ones.append(item)
    _len = len(online_ones)
    rd = random.randint(0, _len - 1)
    return online_ones[rd]


def query_vtb_all():
    full_info = requests.get("https://api.vtbs.moe/v1/fullInfo")
    return full_info.json()


@quick_reply
def query_room_and_player(request_json):
    _message_replace_at = str(
        request_json["message"].replace("[CQ:at,qq=1728158137]", "").replace("[CQ:at,qq=1728158137] ",
                                                                             "").replace(" ", ""))
    _name = _message_replace_at.split("查询主播-")
    _name = _name[len(_name) - 1]
    resp_room = requests.get("https://api.live.bilibili.com/room/v1/Room/room_init", params={"id": int(_name), }).json()

    if resp_room["code"] != 0:
        return "直播间不存在哦"
    else:
        room_data = resp_room["data"]
        status = "在播" if room_data["live_status"] == 1 else "没播"
        lt = time.localtime(room_data["live_time"])
        last_time = time.strftime("%Y-%m-%d/%H:%M:%S", lt)
        user_resp = requests.get("http://api.live.bilibili.com/live_user/v1/Master/info",
                                 params={"uid": room_data["uid"], }).json()
        user_data = user_resp["data"]["info"]
        fin_resp = "主播：{}\n直播状态：{}\n最近开播时间：{}\n".format(user_data["uname"], status, last_time)
        return fin_resp


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


def get_mc_mods_from_gitee():
    gitee_config = minecrafr_server["gitee_repo"]
    url = "https://gitee.com/api/v5/repos/{owner}/{repo}/git/trees/{sha}?recursive=1".format(
        owner=gitee_config["owner"],
        repo=gitee_config["repo"],
        sha=gitee_config["sha"])
    LOGGER.info(url)
    repo_tree = requests.get(url).json()
    LOGGER.info(repo_tree)
    files = repo_tree["tree"]
    result = ""
    assert type(files) == list
    counter = 0
    for item in files:
        if "mods/" in item["path"]:
            counter += 1
            result += ("【{}】".format(str(counter)) + item["path"].replace("mods/", "").replace(".jar", "") + "\n")
        else:
            pass
    return result


def get_ms_status():
    stat_resp = requests.get(minecrafr_server["panel_host"] + "/api/status/" + minecrafr_server["instance"])
    stat = stat_resp.json()
    online_or_not = "正常运行中" if stat["status"] is True else "关闭"
    if online_or_not == "正常运行中":
        stat_str = "{0}：{1}\n版本：{2}\n状态：{3}\n在线人数：{4}\n服务器地址：{5}".format(stat["id"], stat["motd"], stat["version"],
                                                                         online_or_not,
                                                                         stat["current_players"],
                                                                         minecrafr_server["game_port"])
    else:
        stat_str = "{0}：{1}\n版本：{2}\n状态：{3}||".format(stat["id"], stat["motd"], stat["version"],
                                                      online_or_not)
    return stat_str


def random_response():
    rd = random.randint(0, len(bot_resp) - 1)
    resp = bot_resp[rd]["content"]
    if resp == "随机vtb":
        r_vtb = random_vtb()
        LOGGER.info("vtb info{}".format(str(r_vtb)))
        resp = "VTB:{title}\n[CQ:image,file={image}]\n直播间标题：{content}\n直播间链接：https://live.bilibili.com/{roomid}\n".format(
            title=r_vtb["uname"], image=r_vtb["face"], content=r_vtb["title"], roomid=r_vtb['roomid'])
        LOGGER.info(resp)
    return resp


@quick_reply
def random_vtb_as_query(request_json):
    r_vtb = random_vtb()
    resp = "VTB:{title}\n[CQ:image,file={image}]\n直播间标题：{content}\n直播间链接：https://live.bilibili.com/{roomid}\n".format(
        title=r_vtb["uname"], image=r_vtb["face"], content=r_vtb["title"], roomid=r_vtb['roomid'])
    return resp


func_entry = {
    "jrrp": jrrp,
}


@app.route('/', methods=['POST'])
def receive():
    rj = request.json
    LOGGER.info(str(rj))
    _message_replace_at = rj["message"].replace("[CQ:at,qq=1728158137]", "").replace("[CQ:at,qq=1728158137] ",
                                                                                     "").replace(" ", "")
    LOGGER.info(_message_replace_at)
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
    elif "查询主播-" in _message_replace_at:
        return query_room_and_player(rj)
    elif "MC" == _message_replace_at.upper():
        return query_minecraft_server(rj)
    elif "MCMOD" == _message_replace_at.upper():
        return get_mc_mods(rj)
    elif "随机vtb" == _message_replace_at:
        return random_vtb_as_query(rj)
    elif "帮帮我" == _message_replace_at or "help" == _message_replace_at:
        return help_me(rj)
    else:
        LOGGER.warning("未知命令")
        return illegal_request(rj)

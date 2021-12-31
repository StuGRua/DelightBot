import re
import socket

import requests

from config import minecraft_server
from internal.dao import mcrcon
from internal.utils.log import LOGGER


def get_mc_mods_from_gitee():
    gitee_config = minecraft_server["gitee_repo"]
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
    stat_resp = requests.get(minecraft_server["panel_host"] + "/api/status/" + minecraft_server["instance"])
    stat = stat_resp.json()
    online_or_not = "正常运行中" if stat["status"] is True else "关闭"
    if online_or_not == "正常运行中":
        stat_str = "{0}：{1}\n版本：{2}\n状态：{3}\n在线人数：{4}\n服务器地址：{5}".format(stat["id"], stat["motd"], stat["version"],
                                                                         online_or_not,
                                                                         stat["current_players"],
                                                                         minecraft_server["game_port"])
    else:
        stat_str = "{0}：{1}\n版本：{2}\n状态：{3}||".format(stat["id"], stat["motd"], stat["version"],
                                                      online_or_not)
    return stat_str


def mcrcon_comm(comm: str) -> str:
    args = dict()
    args["host"] = "www.mc-tool-man.top"
    args["port"] = 25575
    args["password"] = "x74rtw05"
    # Connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args["host"], args["port"]))
    try:
        # Log in
        result = mcrcon.login(sock, args["password"])
        if not result:
            print("Incorrect rcon password")
            return "服务器错误"

        # Start looping
        request = comm
        response = mcrcon.command(sock, request)

        # response = response.replace("§")
        pat = re.compile("§[a-zA-Z0-9]")
        resp = re.sub(pat, "", response, 999)
        print(resp)
        return resp
    finally:
        sock.close()


def tps():
    return mcrcon_comm("tps")


def mc_list():
    return mcrcon_comm("list")

import requests

from config import minecraft_server
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

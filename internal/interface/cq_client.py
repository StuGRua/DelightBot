import requests

from config import bot_host


def send_group_message(group_id: int, message: str):
    # print("[sending message] to "+str(group_id)+" "+message)
    resp = requests.post(url="{}/send_group_msg".format(bot_host["main"]),
                         json={"group_id": group_id, "message": message})
    return resp.content


def get_group_members(group_id: int) -> list:
    params = {"group_id": group_id}
    resp = requests.get(url="{}/get_group_member_list".format(bot_host["main"]), params=params).json()
    return resp["data"]

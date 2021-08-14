import requests

from config import bot_host
from internal.utils.log import LOGGER


def robot_send_group_message(group: int, body: str):
    _send ={
        "group_id": group,
        "message": body,
    }
    LOGGER.info("[robot_req]{}".format(str(_send)))
    resp = requests.post(url="{}/send_group_msg".format(bot_host["main"]), json=_send).content
    LOGGER.info("[robot_resp]{}".format(str(resp)))
    return resp

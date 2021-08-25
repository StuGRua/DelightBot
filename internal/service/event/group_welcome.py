from internal.dao.redis_group_welcome import get_greeting, set_greeting_msg
from internal.interface.cq_client import send_group_message
from internal.utils.log import LOGGER


# 处理进群通知
def group_welcome_handler(rj: dict):
    assert rj["group_id"]
    msg_pre_resp = get_greeting(int(rj["group_id"]))
    # LOGGER.info("get msg resp of greeting "+str(msg_pre_resp))
    for k, v in msg_pre_resp.items():
        fix_str = "[CQ:at,qq={}]\n".format(str(rj["user_id"])) + v.replace("||", "\n")
        LOGGER.info("DEBUG " + fix_str)
        resp = send_group_message(rj["group_id"], fix_str)
        LOGGER.info(str(resp))

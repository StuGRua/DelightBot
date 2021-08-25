import json
from typing import List

from internal.dao.redis_client import get_conn
from internal.utils.log import LOGGER


# 查返回的招呼信息 array
def get_greeting(group_id: int) -> dict:
    assert group_id
    # 先过一遍redis表查是不是在迎新启用的群里面
    with get_conn() as r:
        is_exist = r.hexists("greeting_group_list", str(group_id))
        # LOGGER.warning(str(is_exist))
        if is_exist is False:
            return dict()
        # 读出来的是json结构(array)，方便之后改
        welcome_content = r.hget("greeting_group_list", str(group_id))
        print(welcome_content)
        welcome_content = json.loads(welcome_content)
        assert type(welcome_content) == dict
        return welcome_content
        # for message in welcome_content:
        #     send_group_message(message=message, group_id=group_id)


def set_greeting_msg(group_id: int, message: str):
    with get_conn() as r:
        r.hset("greeting_group_list", str(group_id), message)


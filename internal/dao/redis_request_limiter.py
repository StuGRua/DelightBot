from internal.dao.redis_client import get_conn
from internal.utils.log import LOGGER

__user_func_limiter_key = "function_name:userid:{function_name}:{userid}"
__group_func_limiter_key = "function_name:group_id:{function_name}:{group_id}"


def limiter_user_func(userid: int, function_name: str) -> int:
    """
    用户-方法 限速
    :param userid: 用户id
    :param function_name:限速方法
    :return:0 未限速，TTL 限速剩余时间
    """
    with get_conn() as r:
        fill_limiter = __user_func_limiter_key.format(function_name=function_name, userid=str(userid))
        # 触发限速
        if r.exists(fill_limiter):
            LOGGER.info("user func limiter in {}".format(fill_limiter))
            return r.ttl(fill_limiter)
        # 未限速
        else:
            r.set(fill_limiter, "1", ex=30)
            return 0


def limiter_group_func(group_id: int, function_name: str) -> int:
    """
    群组-方法 限速
    :param group_id: 群组id
    :param function_name: 限速方法
    :return:0 未限速，TTL 限速剩余时间
    """
    with get_conn() as r:
        fill_limiter = __group_func_limiter_key.format(function_name=function_name, userid=str(group_id))
        # 触发限速
        if r.exists(fill_limiter):
            LOGGER.info("user func limiter in {}".format(fill_limiter))
            return r.ttl(fill_limiter)
        # 未限速
        else:
            r.set(fill_limiter, "1", ex=30)
            return 0

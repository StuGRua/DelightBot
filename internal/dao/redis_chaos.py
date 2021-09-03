from internal.dao.redis_client import get_conn


def add_chaos_time() -> int:
    with get_conn() as r:
        if r.exists("chaos_times"):
            times = int(r.get("chaos_times"))
            times += 1
        else:
            times = 1
        r.set("chaos_times", times)
    return times

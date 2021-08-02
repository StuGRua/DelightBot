import redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, password="x74rtw05")


def get_conn():
    r = redis.Redis(connection_pool=pool, password="x74rtw05")
    return r

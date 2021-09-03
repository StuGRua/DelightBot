import random

from config import random_resp


def random_response():
    _len = len(random_resp)
    rd = random_resp[random.randint(0, _len - 1)]
    return rd["content"]

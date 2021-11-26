import base64
import hashlib
from io import BytesIO

import httpx
import requests

from internal.dao.redis_bili_cos_pics import get_random_cos_pic
from internal.job.get_bili_pics import update_cos_pics_to_redis


def random_cos():
    r_cos = get_random_cos_pic()
    if r_cos == "" or r_cos is None:
        update_cos_pics_to_redis()
        r_cos = get_random_cos_pic()
    return "[CQ:image,file={img}]".format(img=r_cos)


def random_cos_to_wx() -> bool:
    r_cos = get_random_cos_pic()
    cli = httpx.Client()
    pic = cli.get(r_cos.replace("https", "http"), headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}).content
    base64_pic = base64.b64encode(pic)
    md5_pic = hashlib.md5(pic).hexdigest()
    print(base64_pic)
    print(md5_pic)
    resp = cli.post("https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=845e9e02-1c8a-4aeb-853e-ffcde87beacc", json={
        "msgtype": "image",
        "image": {
            "base64": base64_pic.decode("utf-8"),
            "md5": md5_pic
        }
    }
                    )
    resp_json = resp.json()
    if resp_json['errcode'] != 0:
        return False
    return True


def random_cos_to_wx_with_retry():
    """
    带重试的涩图
    :return:
    """
    re_time = 3
    for i in range(re_time):
        res = random_cos_to_wx()
        if res:
            break
        else:
            continue


if __name__ == "__main__":
    random_cos_to_wx_with_retry()

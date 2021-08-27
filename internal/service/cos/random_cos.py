from internal.dao.redis_bili_cos_pics import get_random_cos_pic
from internal.job.get_bili_pics import update_cos_pics_to_redis


def random_cos():
    r_cos = get_random_cos_pic()
    if r_cos == "" or r_cos is None:
        update_cos_pics_to_redis()
        r_cos = get_random_cos_pic()
    return "[CQ:image,file={img}]".format(img=r_cos)

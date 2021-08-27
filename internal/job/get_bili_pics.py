from internal.utils.bili_article import get_articles, get_bili_article_pictures
from internal.dao.redis_bili_cos_pics import get_random_cos_pic, get_cos_pics_all, update_cos_pics
from config import cos_cls

def get_pics_from_cl(cl: int):
    articles = get_articles(cl)
    pics = []
    for arc in articles:
        pics.extend(get_bili_article_pictures(arc))
    print("pic_len:{}".format(str(len(pics))))
    return pics


def update_cos_pics_to_redis():
    for cls in cos_cls:
        pic_ls = get_pics_from_cl(cls)
        update_cos_pics(pic_ls)


def random_cos():
    r_cos = get_random_cos_pic()
    if r_cos == "" or r_cos is None:
        update_cos_pics_to_redis()
        r_cos = get_random_cos_pic()
    return r_cos


if __name__ == "__main__":
    update_cos_pics_to_redis()

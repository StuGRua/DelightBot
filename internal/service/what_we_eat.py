import random

from internal.utils.json_reader import json_reader


def query_food():
    foods = json_reader("static/boot_food/xiachufang.json")
    assert type(foods) == list
    rd = random.randint(0, len(foods) - 1)
    r_food = foods[rd]
    return "{name}\n[CQ:image,file={img}]\n{link}".format(name=r_food["name"], img=r_food["img"], link=r_food["link"])

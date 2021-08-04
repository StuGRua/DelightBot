import httpx
import requests
from bs4 import BeautifulSoup
from internal.utils.json_reader import json_writer, json_reader
import logging


def __get_foods_single_page(number: int):
    url = "https://www.xiachufang.com/category/40076/?page={}".format(str(number))
    headers = {
        'content-type': 'text/html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        "Host": "www.xiachufang.com"
    }
    res_list = []
    resp = requests.get(url=url, headers=headers)
    # with httpx.Client() as cli:
    #     resp = cli.get(url=url, headers=headers)
    logging.info(resp.status_code)
    page = resp
    content = BeautifulSoup(page.content, 'html.parser', from_encoding="utf-8")
    assert content
    content = content.find_all(class_="recipe")
    assert content
    for item in content:
        rep_dict = {}
        item_content = item.find(class_="name")
        logging.info(str(item_content))
        rep_dict["name"] = item_content.text.replace("\n", "").replace(" ", "")
        rep_dict["link"] = "https://xiachufang.com" + item_content.find('a')['href']
        try:
            img = item.find('img')['data-src']
            rep_dict['img'] = img
        except:
            img = item.find('img')['src']
            rep_dict['img'] = img
        res_list.append(rep_dict)
    return res_list


def get_foods_job():
    """
    只需要保证可用性，所以无所谓TTL
    :return:
    """
    res_list = []
    for i in range(1, 8):
        fs = __get_foods_single_page(i)
        res_list.extend(fs)
    json_writer("static/boot_food/xiachufang.json", res_list)


if __name__ == "__main__":
    get_foods_job()
    res = json_reader("static/boot_food/xiachufang.json")
    print(res)

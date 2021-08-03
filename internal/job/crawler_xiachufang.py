import httpx
from bs4 import BeautifulSoup
from internal.utils.json_reader import json_writer, json_reader

def __get_foods_single_page(number: int):
    url = "https://www.xiachufang.com/category/40076/?page={}".format(str(number))
    headers = {
        'content-type': 'text/html'
    }
    res_list = []
    try:
        with httpx.Client() as cli:
            resp = cli.get(url=url, headers=headers)
        page = resp
        content = BeautifulSoup(page.content, 'html.parser')
        content = content.find_all(class_="recipe")
        for item in content:
            rep_dict = {}
            item_content = item.find(class_="name")
            rep_dict["name"] = item_content.text.replace("\n", "").replace(" ", "")
            rep_dict["link"] = "https://xiachufang.com" + item_content.find('a')['href']
            try:
                img = item.find('img')['data-src']
                rep_dict['img'] = img
            except:
                img = item.find('img')['src']
                rep_dict['img'] = img
            res_list.append(rep_dict)
    except:
        return

    return res_list


def get_foods_job():
    """
    只需要保证可用性，所以无所谓TTL
    :return:
    """
    res_list = []
    for i in range(1, 10):
        fs = __get_foods_single_page(i)
        res_list.extend(fs)
    json_writer("static/boot_food/xiachufang.json", res_list)


if __name__ == "__main__":
    get_foods_job()
    res = json_reader("static/boot_food/xiachufang.json")
    print(res)

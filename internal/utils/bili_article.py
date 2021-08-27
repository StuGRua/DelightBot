import requests
from bs4 import BeautifulSoup


def get_bili_article_pictures(number:int):
    url = "https://www.bilibili.com/read/cv{}".format(str(number))
    headers = {
        'content-type': 'text/html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.102 Safari/537.36',
    }
    res_list = []
    resp = requests.get(url=url, headers=headers)
    content = BeautifulSoup(resp.content, 'html.parser', from_encoding="utf-8")
    urls = content.find_all('img')

    for item in urls:
        pre = item["data-src"]
        print(pre)
        if "url=" not in pre:
            res_list.append("https:" + pre)
        else:
            res_list.append("https:" + pre.split("url=")[1])
            print("hit")
            print(pre.split("url=")[1])
    return res_list


def get_articles(number:int):
    url = "http://api.bilibili.com/x/article/list/web/articles?id={}".format(str(number))
    resp = requests.get(url)
    ids = [x["id"] for x in resp.json()['data']['articles']]
    return ids







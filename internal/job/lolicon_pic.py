import requests


def random_lolicon():
    resp = requests.get("https://api.lolicon.app/setu/v1?size1200=true")
    pic_info = resp.json()["data"][0]
    tags_str = "成分分析:"
    for item in pic_info["tags"]:
        tags_str += "[{}] ".format(item)
    return tags_str + "\n[CQ:image,file={img}]".format(img=pic_info["url"])


if __name__ == "__main__":
    print(random_lolicon())
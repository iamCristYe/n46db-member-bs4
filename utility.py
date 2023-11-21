import requests
import os
import urllib


def download_image(img_src_url: str, img_relative_path=None) -> str:
    response = requests.get(img_src_url)
    if not img_relative_path:
        img_relative_path = f"images/{img_src_url.split('/')[-3]}/{img_src_url.split('/')[-2]}/{img_src_url.split('/')[-1]}"
    os.makedirs(os.path.dirname(img_relative_path), exist_ok=True)
    with open(img_relative_path, "wb") as f:
        f.write(response.content)


def add_host(str: str) -> str:
    return urllib.parse.urljoin("https://www.nogizaka46.com/", str)


def list_deduplication(ls: list) -> list:
    res = []
    for i in ls:
        if i not in res:
            res.append(i)

    return res

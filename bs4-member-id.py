from bs4 import BeautifulSoup
import urllib
import requests
import json
import re
import time
from utility import download_image, add_host


def main():
    with open("members.json", mode="r") as src:
        data = json.load(src)

    list_url = "https://n46db.com/saka/saka-memberlist.php?graduated=yes"
    soup = BeautifulSoup(requests.get(list_url).content, "lxml")
    table = soup.find_all("table")[4]
    tr_list = table.find_all("tr")
    for i in range(1, len(tr_list)):
        tr = tr_list[i]
        link = tr.find_all("a")[0].get("href")
        name = tr.find_all("a")[0].get_text()
        # print(tr.find_all("a"))
        abbr = tr.find_all("td")[-1].get_text()
        for member in data:
            if member["member_name_kanji"] == name:
                member["id"] = link.replace("../profile.php?id=", "").replace(
                    "../profile-saka.php?id=", ""
                )
                member["abbr"] = abbr

    with open("members.json", mode="w", encoding="utf-8") as src:
        json.dump(data, src, ensure_ascii=False, indent=2)


main()

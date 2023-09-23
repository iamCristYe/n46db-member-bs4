from bs4 import BeautifulSoup
import urllib
import requests
import json
import re
from utility import download_image


def add_host(str: str) -> str:
    return urllib.parse.urljoin("https://n46db.com/", str)


def get_profile_url_list() -> list:
    # https://n46db.com/saka/saka-memberlist.php?graduated=yes
    list_url = "https://n46db.com/saka/saka-memberlist.php?graduated=yes"
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    #
    table = soup.find_all("table")[4]  # , class_="blueopta")[0]

    profile_url_list = []

    for tr in table.find_all("tr"):
        for td in tr.find_all("td"):
            for a in td.find_all("a"):
                url = urllib.parse.urljoin(list_url, a.get("href"))
                profile_url_list.append(url)

    print(profile_url_list)


def get_profile(url: str) -> dict:
    result = {}
    # https://n46db.com/profile-saka.php?id=126
    # https://n46db.com/profile-saka.php?id=94

    soup = BeautifulSoup(requests.get(url).content, "lxml")

    name_list = soup.find_all("span", class_="f200")
    result["member_name_romaji"] = name_list[0].get_text().strip()
    result["member_name_kanji"] = name_list[1].get_text().strip()

    td_list = soup.find_all("td")
    for td in td_list:
        text = td.get_text()

        if "血液型:" in text:
            result["blood_type"] = text.replace("血液型:", "").strip().replace("型", "")
        if "出身地:" in text:
            result["hometown"] = text.replace("出身地:", "").strip()

        if "加入期:" in text:
            result["generation"] = text.replace("加入期:", "").strip().replace("期", "")
        if "身長:" in text:
            result["height"] = text.replace("身長:", "").strip().replace("cm", "")
        if "あだ名:" in text:
            result["nickname"] = text.replace("あだ名:", "").strip()
            result["comment"] = td.findNext("td").get_text().strip()
    grad_date = soup.find_all("span", attrs={"style": "color:red"})
    if grad_date:
        result["grad_date"] = grad_date[0].get_text()[-10:]

    img_list = soup.find_all("img")
    for img in img_list:
        src = add_host(img.get("src"))
        if "button" not in src:
            download_image(src)
    if "saka" in url:
        td_list = soup.find_all("td")
        for td in td_list:
            text = td.get_text()
            if "生年月日:" in text:
                birthday = re.sub(
                    r"[年月日\s]|(（\d+ 歳）)", "", text.replace("生年月日:", "").strip()
                )
                result["birthday"] = f"{birthday[0:4]}-{birthday[4:6]}-{birthday[6:8]}"
            if "グループ:" in text:
                if "櫻坂" in text:
                    result["group"] = "kesa"
                if "日向" in text:
                    result["group"] = "hi"

    # https://n46db.com/profile.php?id=78
    else:
        td_list = soup.find_all("td")
        for td in td_list:
            text = td.get_text()
            if "生年月日:" in text:
                match = re.findall(r"\d+", text)
                result[
                    "birthday"
                ] = f"{match[0]}-{match[1].zfill(2)}-{match[2].zfill(2)}"
            if "グループ:" in text:
                if "櫻坂" in text:
                    result["group"] = "kesa"
                if "日向" in text:
                    result["group"] = "hi"
    return result


print(get_profile("https://n46db.com/profile.php?id=8"))


def main():
    result = []
    profile_url_list = get_profile_url_list()
    for url in profile_url_list:
        result.append(get_profile(url))
    with open("members.json", "w") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

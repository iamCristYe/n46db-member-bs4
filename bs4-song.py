from bs4 import BeautifulSoup
import urllib
import requests
import json
import re
import time
from utility import download_image, add_host


def get_song_url_list() -> list:
    list_url = "https://n46db.com/songs/all-songs-list.php"
    soup = BeautifulSoup(requests.get(list_url).content, "lxml")
    #
    table = soup.find_all("table")[2]  # , class_="blueopta")[0]

    song_url_list = []

    for tr in table.find_all("tr"):
        for td in tr.find_all("td"):
            for a in td.find_all("a"):
                url = urllib.parse.urljoin(list_url, a.get("href"))
                if "song.php" in url:
                    song_url_list.append(url)

    return song_url_list


# def download_gallery(url: str):
#     soup = BeautifulSoup(requests.get(url).content, "lxml")
#     img_list = soup.find_all("img")
#     for img in img_list:
#         src = add_host(img.get("src"))
#         if "button" not in src:
#             download_image(src)


def get_song(url: str) -> dict:
    result = {}

    # https://n46db.com/song.php?songcode=s012g

    # soup = BeautifulSoup(requests.get(url).content, "lxml")

    # name_list = soup.find_all("span", class_="f200")
    # result["member_name_romaji"] = name_list[0].get_text().strip()
    # result["member_name_kanji"] = name_list[1].get_text().strip()

    # td_list = soup.find_all("td")
    # for td in td_list:
    #     text = td.get_text()
    #     if "生年月日:" in text:
    #         match = re.findall(r"\d+", text)
    #         result["birthday"] = f"{match[0]}-{match[1].zfill(2)}-{match[2].zfill(2)}"
    #     if "血液型:" in text:
    #         result["blood_type"] = text.replace("血液型:", "").strip().replace("型", "")
    #     if "出身地:" in text:
    #         result["hometown"] = text.replace("出身地:", "").strip()
    #     if "加入期:" in text:
    #         match = re.findall(r"\d+", text)
    #         result["generation"] = f"{match[0]}"
    #     if "身長:" in text:
    #         result["height"] = text.replace("身長:", "").strip().replace("cm", "")
    # grad_date = soup.find_all("span", attrs={"style": "color:red"})
    # if grad_date:
    #     result["grad_date"] = grad_date[0].get_text()[-10:]

    # img_list = soup.find_all("img")
    # for img in img_list:
    #     src = add_host(img.get("src"))
    #     if "button" not in src:
    #         download_image(src)

    # if "saka" in url:
    #     td_list = soup.find_all("td")
    #     for td in td_list:
    #         text = td.get_text()
    #         if "あだ名:" in text:
    #             result["nickname"] = text.replace("あだ名:", "").strip()
    #             result["comment"] = td.findNext("td").get_text().strip()
    #         if "グループ:" in text:
    #             if "櫻坂" in text:
    #                 result["group"] = "kesa"
    #             if "日向" in text:
    #                 result["group"] = "hi"

    # # https://n46db.com/profile.php?id=78
    # else:
    #     td_list = soup.find_all("td")
    #     for td in td_list:
    #         text = td.get_text()
    #         result["group"] = "no"
    #         if "あだ名:" in text:
    #             result["nickname"] = text.replace("あだ名:", "").strip()
    #         if "兄弟:" in text:
    #             family = []
    #             for word in re.split(r"\/|\.", str(td)):
    #                 if "unknown" in word:
    #                     family.append("unknown")
    #                 elif "onlychild" in word:
    #                     family.append("only_child")
    #                 elif "lilbro" in word:
    #                     family.append("younger_brother")
    #                 elif "lilsis" in word:
    #                     family.append("younger_sister")
    #                 elif "bigbro" in word:
    #                     family.append("elder_brother")
    #                 elif "bigsis" in word:
    #                     family.append("elder_sister")
    #             result["family"] = family
    #         if "サイリウム:" in text:
    #             result["color"] = text.replace("サイリウム:", "").strip()
    #     download_gallery(url.replace("profile.php", "members/membergallery.php"))
    # return result


def main():
    result = []
    song_url_list = get_song_url_list()
    # print(song_url_list)
    for url in song_url_list:
        song = get_song(url)
        # print(profile["member_name_kanji"])
        result.append(song)
        time.sleep(3)
        with open("songs.json", "w") as file:
            json.dump(result, file, ensure_ascii=False, indent=2)


main()

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


def download_gallery(url: str):
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    img_list = soup.find_all("img")
    for img in img_list:
        src = add_host(img.get("src"))
        if "button" not in src:
            download_image(src)


def get_song(url: str) -> dict:
    result = {}
    result["url"] = url
    # https://n46db.com/song.php?songcode=s012g
    # https://n46db.com/song.php?songcode=s022a
    # https://n46db.com/song.php?songcode=s028e

    # 5 parts: basic_info, cover, comments, MV_info, members
    soup = BeautifulSoup(requests.get(url).content, "lxml")

    table_list = soup.find_all("table")
    for table in table_list:
        if "刹那少女" in table.get_text():
            continue
        if "メインページ" in table.get_text():
            continue
        if not table.get_text().strip():
            continue
        if "枚目シングル" in table.get_text():
            continue
        if "©" in table.get_text():
            continue

        print(table.get_text())
        if "曲名" in table.get_text():
            tr_list = table.find_all("tr")
            for tr in tr_list:
                text = tr.get_text().strip()
                if "曲名：" in text:
                    result["name"] = text.replace("曲名：", "").strip()
                if "概要：" in text:
                    result["summary"] = text.replace("概要：", "").strip()
                if "センター：" in text:
                    result["center"] = text.replace("センター：", "").strip()
                if "歌手：" in text:
                    result["center"] = text.replace("歌手：", "").strip()
                    result["solo"] = True
                if "作詞：" in text:
                    result["lyricist"] = text.replace("作詞：", "").strip()
                if "作曲：" in text:
                    result["composer"] = text.replace("作曲：", "").strip()
                if "編曲：" in text:
                    result["arranger"] = text.replace("編曲：", "").strip()
                if "発売日：" in text:
                    result["date"] = text.replace("発売日：", "").strip()

        # for table in table_list:
        elif "通常盤" in table.get_text():
            result["version"] = []
            td_list = table.find_all("td")
            for td in td_list:
                text = td.get_text()
                result["version"].append(text)
                img_list = td.find_all("img")
                for img in img_list:
                    src = add_host(img.get("src"))
                    # if "button" not in src:
                    #     download_image(src)

        else:
            # the next part would be commets
            result["comments"] = []
            li_list = table.find_all("li")
            if li_list:
                for li in li_list:
                    result["comments"].append(li.get_text().strip())
            else:
                result["comments"].append(table.get_text().strip())

            break

    if "Music video なし" in soup.get_text():
        result["MV"] = None
    else:
        u_list = soup.find_all("u")
        for u in u_list:
            if "Music Video" in u.get_text():
                a_list = soup.find_all("a")
                for a in a_list:
                    a_link = a.get("href")
                    if "director" in a_link:
                        if "director" not in result:
                            result["director"] = []

                        result["director"].append(
                            a_link.replace(
                                "https://n46db.com/videos/director.php?director=", ""
                            )
                        )
                    if "furi" in a_link:
                        if "choreographer" not in result:
                            result["choreographer"] = []
                        result["choreographer"].append(
                            a_link.replace("https://n46db.com/songs/furi.php?furi=", "")
                        )

    result["formation"] = []
    for table in table_list:
        a_list = table.find_all("a")
        if a_list:
            temp = []
            for a in a_list:
                src = add_host(a.get("href"))
                if "profile.php" in src:
                    temp.append(src)
            result["formation"].append(temp)

    return result


def main():
    result = []
    song_url_list = get_song_url_list()
    # print(song_url_list)
    # song_url_list = [
    #     "https://n46db.com/song.php?songcode=s012g",
    #     "https://n46db.com/song.php?songcode=s022a",
    #     "https://n46db.com/song.php?songcode=s028e",
    # ]
    for i in range(0, 300):
        song = get_song(song_url_list[i])
        result.append(song)
        time.sleep(3)
        with open("songs_crawled.json", "w") as file:
            json.dump(result, file, ensure_ascii=False, indent=2)


main()

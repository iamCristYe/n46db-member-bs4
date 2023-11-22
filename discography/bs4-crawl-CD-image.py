from bs4 import BeautifulSoup
import requests
import time
import random
import json
import os
import urllib.parse

from utility import download_image, add_host

discography = {
    "NS": [
        "ぐるぐるカーテン",
        "おいでシャンプー",
        "走れ！Bicycle",
        "制服のマネキン",
        "君の名は希望",
        "ガールズルール",
        "バレッタ",
        "気づいたら片想い",
        "夏のFree&Easy",
        "何度目の青空か？",
        "命は美しい",
        "太陽ノック",
        "今、話したい誰かがいる",
        "ハルジオンが咲く頃",
        "裸足でSummer",
        "サヨナラの意味",
        "インフルエンサー",
        "逃げ水",
        "いつかできるから今日できる",
        "シンクロニシティ",
        "ジコチューで行こう！",
        "帰り道は遠回りしたくなる",
        "Sing Out！",
        "夜明けまで強がらなくてもいい",
        "しあわせの保護色",
        "僕は僕を好きになる",
        "ごめんねFingers crossed",
        "君に叱られた",
        "Actually...",
        "好きというのはロックだぜ！",
        "ここにはないもの",
        "人は夢を二度見る",
        "おひとりさま天国",
        "Monopoly",
    ],
    "NA": [
        "透明な色",
        "それぞれの椅子",
        "生まれてから初めて見た夢",
        "今が思い出になるまで",
    ],
    "NUA": ["僕だけの君 ~Under Super Best~"],
    "NBA": [
        "Time flies",
    ],
}


def get_image_name(text):
    for type in discography:
        for i in range(len(discography[type])):
            if discography[type][i] in text:
                img_dest = f"./image/{type}{i+1}"

                if "盤A" in text or "Type-A" in text:
                    img_dest += f"A.jpg"
                elif "盤B" in text or "Type-B" in text:
                    img_dest += f"B.jpg"
                elif "盤C" in text or "Type-C" in text:
                    img_dest += f"C.jpg"
                elif "盤D" in text or "Type-D" in text:
                    img_dest += f"D.jpg"
                else:
                    img_dest += f".jpg"
                return img_dest

            else:
                img_dest = f"./image/{text}.jpg"
    return img_dest


def get_CD_list():
    current_page = 0
    current_url = f"https://www.nogizaka46.com/s/n46/search/discography?ima=3158&cd=10001&ct=SINGLE&page={current_page}"
    CD_list = []

    while True:
        soup = BeautifulSoup(requests.get(current_url).content, "lxml")
        # print(soup.prettify())
        img_tile_list = soup.find_all("a", class_="m--jkt__a hv--thumb")
        for img_tile in img_tile_list:
            img_div = img_tile.find_all("div", class_="m--bg js-bg")[0]
            # "background-image: url(&quot;/images/46/71f/0e4f001a6f9ef6984ba166f1749a5/500_320_102400.jpg&quot;);"
            # img_src = (
            #     img_div.get("style")
            #     .replace("background-image: url(&quot;", "")
            #     .replace("&quot;);", "")
            # )
            img_src = img_div.get("data-src")

            text = img_tile.find_all("p", class_="m--jkt__ttl f--head")[0].get_text()
            date = img_tile.find_all("p", class_="m--jkt__time f--head")[0].get_text()

            img_dest = get_image_name(text)
            print(add_host(img_src), img_dest)
            # download_image(add_host(img_src), img_dest)
            CD_list.append([text, date, add_host(img_src)])

        next_li = soup.find_all("li", class_="next")
        if next_li:
            current_page += 1
            current_url = f"https://www.nogizaka46.com/s/n46/search/discography?ima=3158&cd=10001&ct=SINGLE&page={current_page}"
            print(current_url)
            # when testing, uncomment below line to only get page 1
            # break
            time.sleep(random.randint(1, 3))
        else:
            break

    with open("discography.json", "w") as file:
        json.dump(CD_list, file, ensure_ascii=False, indent=2)


get_CD_list()

import requests
import json


def get_list(playlist_url):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    playlist_id = playlist_url.replace("https://www.youtube.com/playlist?list=", "")

    params = {
        "part": "id,snippet,contentDetails,status",
        "playlistId": playlist_id,
        "maxResults": 100,
        "key": "AIzaSyDk3izF_jy-RUwUsN4Rf6oPsPqtahbt4yI",  # Replace with your actual API key
    }

    headers = {
        "authority": "www.googleapis.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh-TW;q=0.5,zh;q=0.4",
        "cache-control": "no-cache",
        "dnt": "1",
        "origin": "https://hi3103.net",
        "pragma": "no-cache",
        "referer": "https://hi3103.net/",
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "x-client-data": "CJO2yQEIorbJAQipncoBCMbeygEIlKHLAQjvmM0BCIWgzQEYp+rNAQ==",
    }

    response = requests.get(url, params=params, headers=headers)

    list = {playlist_id: {}}
    if response.status_code == 200:
        data = response.json()
        video_list = data["items"]
        for video in video_list:
            video_id = video["contentDetails"]["videoId"]
            if "img" not in list[playlist_id]:
                img_url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
                list[playlist_id]["img"] = img_url
            print(video["contentDetails"]["videoId"], video["snippet"]["title"])
            list[playlist_id][video_id] = video["snippet"]["title"]

    else:
        print(f"Error: {response.status_code}, {response.text}")
    return list


playlists = [
    "https://www.youtube.com/playlist?list=OLAK5uy_lKk-rG0LacCpEDhSMqhFIG9YxzPZHMu7o",
    "https://www.youtube.com/playlist?list=OLAK5uy_kOoYXVceZTb1qW7nra9O9oIyT-M-imd_w",
    "https://www.youtube.com/playlist?list=OLAK5uy_lIOrU1W1bBsBInUwZNSOx9ISel1hzLWcM",
    "https://www.youtube.com/playlist?list=OLAK5uy_kayQiJicGQKcImAMFxJb_UibOVsDTWHFg",
    "https://www.youtube.com/playlist?list=OLAK5uy_mQGstpWJ4AIfsrzks0Ztw1yBA_YlptOJw",
    "https://www.youtube.com/playlist?list=OLAK5uy_moR_yY8EmFj5JHAaZKed09W9drEtMgV34",
    "https://www.youtube.com/playlist?list=OLAK5uy_mPn9vJ5tNoGwnMX7rDl3RiNeaK6qhPxNM",
    "https://www.youtube.com/playlist?list=OLAK5uy_nGm-zmthP73rVjn-LszTDTfjgFGGNwrZg",
    "https://www.youtube.com/playlist?list=OLAK5uy_koxG9V0xyx2uQ0LPOE_v5mH2YBfH0zQsc",
    "https://www.youtube.com/playlist?list=OLAK5uy_nlgwOQuYzdZsKL0Jmwn6_mJJKbNT8Z_hA",
    "https://www.youtube.com/playlist?list=OLAK5uy_nytCiGz5ehan6TVg9u0zp1pGL49Z33HrM",
    "https://www.youtube.com/playlist?list=OLAK5uy_mplS33D2bulj9pvzEUddTyl7RtytoF2Qk",
    "https://www.youtube.com/playlist?list=OLAK5uy_kbeqvYTjRTOHmB3DI1Y6E48_v9DlorzBs",
    "https://www.youtube.com/playlist?list=OLAK5uy_mYDTJNIO6mqrDdCcccVrto8rykeHKjrs4",
    "https://www.youtube.com/playlist?list=OLAK5uy_n4dfMTr-ZbyK3b4CQUyZ47s6MdtDZcPAg",
    "https://www.youtube.com/playlist?list=OLAK5uy_kbvxzUDOvg_BnCmncoGDDzpwZWz673zNw",
    "https://www.youtube.com/playlist?list=OLAK5uy_nB8pOZnnBoyay4Vu4BKoD28wUHDceyqcY",
    "https://www.youtube.com/playlist?list=OLAK5uy_nmkynzp1Y0w6j8e8viEEAYlEEbPkoqafU",
    "https://www.youtube.com/playlist?list=OLAK5uy_lLwBJ91XLk0GdvEpAZvTx0V3FvnBWZVEc",
    "https://www.youtube.com/playlist?list=OLAK5uy_nVmMkFhKEKATveuYPv7FO9XtOnWRbWQgI",
    "https://www.youtube.com/playlist?list=OLAK5uy_momw47GSvhbvFVATfOKlK2tVgerMpAuiA",
    "https://www.youtube.com/playlist?list=OLAK5uy_mOtrADLa9MAa0zw1Yb7XV4xt0T3mUF2QA",
    "https://www.youtube.com/playlist?list=OLAK5uy_mzFkHepyt9atJnI1DgO2nCLQVGahm5BGQ",
    "https://www.youtube.com/playlist?list=OLAK5uy_ljQ8C5KJr8zjSkgO1TdoZnolB7axz4HvA",
    "https://www.youtube.com/playlist?list=OLAK5uy_lh1oVtJL6iQ7ELXed_BYdPeAxmLkfFrKU",
    "https://www.youtube.com/playlist?list=OLAK5uy_n8_vX0H5kjdWFEbLqylSumRxB32_gWxx0",
    "https://www.youtube.com/playlist?list=OLAK5uy_nsdhsyrejaWJJbjtbSZzR9CYPBWUFKrSA",
    "https://www.youtube.com/playlist?list=OLAK5uy_nc-iqVAF31ygnt0f6EPOOUpRYO2rt-oVU",
    "https://www.youtube.com/playlist?list=OLAK5uy_m8jMy9dCTicZOOhFKXcbNVvG-eRieLrlU",
    "https://www.youtube.com/playlist?list=OLAK5uy_mAsx6OXSGOdVDlxm9EW_nn6jw83hkbl2E",
    "https://www.youtube.com/playlist?list=OLAK5uy_m5_yO5ts_xRwHX1bf2N4NeW9bFv7blNuM",
    "https://www.youtube.com/playlist?list=OLAK5uy_nFfEZUxh6bpnv-pgKgu1bQT7cxKgrufDw",
    "https://www.youtube.com/playlist?list=OLAK5uy_kiYTsb7MXXK5IAoisWCQwDbmhpphKXkfQ",
    "https://www.youtube.com/playlist?list=OLAK5uy_k-Na5dxShlUFqx-xORTYGmCJC1FmfcUY4",
    "https://www.youtube.com/playlist?list=OLAK5uy_nIXd0tkUnd7cJPDrbX5Oei1JeYubOKOVA",
    "https://www.youtube.com/playlist?list=OLAK5uy_nNdloilvDniuJY0XTRh0laJRI4QsygtTA",
    "https://www.youtube.com/playlist?list=OLAK5uy_mZ0WAeVz_O7FjzJsP5VD0Oi4BsmyiIxig",
    "https://www.youtube.com/playlist?list=OLAK5uy_k_Y7f0OQMJT5T-zb99Iw-Bk2kHcc0spqg",
    "https://www.youtube.com/playlist?list=OLAK5uy_nV1Cpz39rnO8fRukyx35WdUe1K3TwI9-4",
    "https://www.youtube.com/playlist?list=OLAK5uy_nSWlPGM5BedscsjeSNlEriUxfn_HcHqZs",
    "https://www.youtube.com/playlist?list=OLAK5uy_nphBTQ0z9Yo4GX0nZntydtnLiEmTWFrZU",
    "https://www.youtube.com/playlist?list=OLAK5uy_kq7m8YkrW83CnbWlx42_-EzpEXlxVZTJg",
    "https://www.youtube.com/playlist?list=OLAK5uy_kKHsXFyCaWhXF8Tzt-85uoelXrR86AKXE",
    "https://www.youtube.com/playlist?list=OLAK5uy_k-9t1jLREECnt3P7SJxz__IKxbHAIClg0",
    "https://www.youtube.com/playlist?list=OLAK5uy_lEE4POUTJe-BX2ZRBGoyTvcWQDB6YSK58",
    "https://www.youtube.com/playlist?list=OLAK5uy_l_GU_JQTY3jxSsjTqBQ2XpMuuIYB8lNCo",
    "https://www.youtube.com/playlist?list=OLAK5uy_lVFGfI0FlJTZ4Y3qeofMglnWpmm__00tY",
    "https://www.youtube.com/playlist?list=OLAK5uy_lJZ-b3GWuy6db0B4PllSEf5nOhMzNUfyk",
    "https://www.youtube.com/playlist?list=OLAK5uy_kO0-Pe2n-RHP9OHEjZ-jP7_rYh7cJWrjI",
    "https://www.youtube.com/playlist?list=OLAK5uy_ls7yYkwqyW6LnRgS8Xut9K8ELWMuHmF94",
    "https://www.youtube.com/playlist?list=OLAK5uy_lULcvpeFNhjL-9NHNxCPdsbGebw5qIidk",
    "https://www.youtube.com/playlist?list=OLAK5uy_lwneSHxXYsPoiVmszykLojGn0lKRZUt7o",
    "https://www.youtube.com/playlist?list=OLAK5uy_l-Sh2dt5InHGYrZGuwOhUgMcHibPh7C_w",
    "https://www.youtube.com/playlist?list=OLAK5uy_ksHoQmWbA7JInMwxTJV5thDQIK2EdCm84",
    "https://www.youtube.com/playlist?list=OLAK5uy_kqGKwy3TPPV7VzNh9oEaFWx4H5W-pjVPE",
    "https://www.youtube.com/playlist?list=OLAK5uy_mSLlxL36AzRPmzEJOka2schJVlQir3eTY",
    "https://www.youtube.com/playlist?list=OLAK5uy_lDosPMLF9YZuvTLj4QYZ9RF2tjU9SASg0",
    "https://www.youtube.com/playlist?list=OLAK5uy_m9gkYVngH4erNElw5vUFwSzWxiOjbeJ_0",
    "https://www.youtube.com/playlist?list=OLAK5uy_lkVKJe4le7nihvdgiMnOYIMbetPrzAzxo",
    "https://www.youtube.com/playlist?list=OLAK5uy_lv0A7WmOg2HuVWbs881kfKUiFFiyzNviM",
    "https://www.youtube.com/playlist?list=OLAK5uy_md8h1LmuzFl4z3p1GkUIuK_cRPzR3sVV0",
    "https://www.youtube.com/playlist?list=OLAK5uy_kR24XZkHRgz1GIfZrzJHHh6VlCgOcJX70",
    "https://www.youtube.com/playlist?list=OLAK5uy_m3zykRuemALKhW30K5bu5hniOniHsudaI",
    "https://www.youtube.com/playlist?list=OLAK5uy_m27WfKV20t1NZ9rNTQqt9tSn9QOzVwxms",
    "https://www.youtube.com/playlist?list=OLAK5uy_lr7_M-g5k-0TwFDW6R4logFlfOIa-cXYI",
    "https://www.youtube.com/playlist?list=OLAK5uy_k6Y-b4MKN7Uf8hE8qtGyRM8imyTJLDXzI",
    "https://www.youtube.com/playlist?list=OLAK5uy_keNIwGrWqF2t7HzeADBEaU-Vb3f5asdc8",
    "https://www.youtube.com/playlist?list=OLAK5uy_kcybgRXrbT0-gGiHKKTVCki5319w-QO0c",
    "https://www.youtube.com/playlist?list=OLAK5uy_nh_psVozMspc5zJ2hWwM3ldhbFL0Gxt6o",
    "https://www.youtube.com/playlist?list=OLAK5uy_msEcYiCYljwonqAR3UwLG2jTqLZMi-v6M",
    "https://www.youtube.com/playlist?list=OLAK5uy_n7aAEIAeQn_bnyeb7e7LyCpbPX_r9W1EA",
    "https://www.youtube.com/playlist?list=OLAK5uy_ke8HBtvHn4xb-_uF10uuM9AK5m6-t_5M8",
    "https://www.youtube.com/playlist?list=OLAK5uy_nzKG2kvE8-GGJn8DjIrN1SPDmT-hyyx-k",
]


result = []
for playlist in playlists:
    result.append(get_list(playlist))

with open("youtube-id.json", "w") as file:
    json.dump(result, file, ensure_ascii=False, indent=2)

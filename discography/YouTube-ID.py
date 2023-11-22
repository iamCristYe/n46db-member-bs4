import requests
import json


def get_list(playlist_url):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    playlist_id = playlist_url.replace("https://www.youtube.com/playlist?list=", "")

    params = {
        "part": "id,snippet,contentDetails,status",
        "playlistId": playlist_id,
        "maxResults": 1000,
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
    "https://www.youtube.com/playlist?list=PLDUMgL1jIEfMcaJcz082WS8TxcTlexJKz",
]


result = []
for playlist in playlists:
    result.append(get_list(playlist))

with open("youtube-mv.json", "w") as file:
    json.dump(result, file, ensure_ascii=False, indent=2)

import json
from utility import list_deduplication

# Read existing JSON data from the file
with open("songs_crawled.json", mode="r") as src:
    data = json.load(src)
with open("../member/members.json", mode="r") as src:
    members = json.load(src)

id_dict = {}
abbr_dict = {}
for member in members:
    id_dict[member["id"]] = member["member_name_kanji"].replace(" ", "")
    abbr_dict[member["abbr"]] = member["member_name_kanji"].replace(" ", "")


songs = {}
for song in data:
    included_in = song["url"].replace("https://n46db.com/song.php?songcode=", "")[0:-1]
    if included_in not in songs:
        songs[included_in] = {}
    # print(song["summary"])
    song["type"] = song["summary"][song["summary"].index("（") + 1 : -1]
    # if "unit" not in songs[included_in]:
    #     songs[included_in]["unit"] = 0
    # if song["type"] == "ユニット曲":
    #     songs[included_in]["unit"] += 1
    if "title" not in songs[included_in]:
        # print(song["name"])
        songs[included_in]["title"] = song["name"]
    if "date" not in songs[included_in]:
        songs[included_in]["date"] = song["date"]
    del song["date"]
    if "center" in song:
        song["center"] = song["center"].split("・")

    if "composer" in song:
        song["composer"] = song["composer"].split("、")
        song["composer"] = list_deduplication(song["composer"])

    if "arranger" in song:
        song["arranger"] = song["arranger"].split("、")
        song["arranger"] = list_deduplication(song["arranger"])

    if "lyricist" in song:
        song["lyricist"] = song["lyricist"].split("、")
        song["lyricist"] = list_deduplication(song["lyricist"])

    if "director" in song:
        for i in range(len(song["director"])):
            song["director"][i] = song["director"][i].replace(
                "videos/director.php?director=", ""
            )
        song["director"] = list_deduplication(song["director"])

    if "choreographer" in song:
        for i in range(len(song["choreographer"])):
            song["choreographer"][i] = song["choreographer"][i].replace(
                "songs/furi.php?furi=", ""
            )
        song["choreographer"] = list_deduplication(song["choreographer"])

    if "version" in song:
        songs[included_in]["versions"] = song["version"]
        del song["version"]

    processed_comments = []

    for comment in song["comments"]:
        if not ("表題曲" in comment and "アンダー曲" in comment):
            processed_comments.append(comment)

    song["comments"] = processed_comments

    if "formation" in song:
        formation = []
        temp = []

        for row in song["formation"]:
            if len(row) < 1:
                continue
            row_temp = []
            for url in row:
                if "https://n46db.com/profile.php?shortname=" in url:
                    row_temp.append(
                        abbr_dict[
                            url.replace("https://n46db.com/profile.php?shortname=", "")
                        ]
                    )
                else:
                    row_temp.append(
                        id_dict[url.replace("https://n46db.com/profile.php?id=", "")]
                    )

            formation.append(list_deduplication(row_temp))

            formation_remove_first = False
            if len(formation) > 1:
                for member in formation[0]:
                    if member in formation[-1]:
                        formation_remove_first = True
                        break

            if formation_remove_first:
                temp = []
                for i in range(1, len(formation)):
                    temp.append(formation[i])
                formation = temp
        song["formation"] = formation

    if "tracks" not in songs[included_in]:
        songs[included_in]["tracks"] = []
    songs[included_in]["tracks"].append(song)

# for release in songs:
#     #print(release)
#     print(songs[release]["title"],songs[release]["unit"])

with open("discography_CD.json", mode="r") as CD_llc:
    llc_data = json.load(CD_llc)

with open("youtube-id.json", mode="r") as youtube_data_json:
    youtube_data = json.load(youtube_data_json)

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
    "NHS": ["世界中の隣人よ", "Route 246", "１・２・３"],
}

result = {"NS": [], "NA": [], "NUA": [], "NBA": [], "NHS": []}  # 配信限定シングル
for i in range(1, 35):
    result["NS"].append(songs[f"s{str(i).zfill(3)}"])
for i in range(1, 5):
    result["NA"].append(songs[f"a{str(i).zfill(3)}"])
    result["NA"][i - 1]["title"] = discography["NA"][i - 1]
for i in range(1, 2):
    result["NUA"].append(songs[f"u{str(i).zfill(3)}"])
    result["NUA"][i - 1]["title"] = discography["NUA"][i - 1]
for i in range(1, 2):
    result["NBA"].append(songs[f"b{str(i).zfill(3)}"])
    result["NBA"][i - 1]["title"] = discography["NBA"][i - 1]
for i in range(1, 4):
    result["NHS"].append(songs[f"z{str(i).zfill(3)}"])
    result["NHS"][i - 1]["title"] = discography["NHS"][i - 1]

for release_type in result:
    for release in result[release_type]:
        if "versions" in release:
            dict = {}
            for version in release["versions"]:
                dict[version] = {}
            release["versions"] = dict


# for release_type in result:
#     for release in result[release_type]:
#         release["youtube_playlist_id"] = []
#         release["cover_youtube"] = []
#         for song in release["tracks"]:
#             for youtube_playlist in youtube_data:
#                 for playlist_id in youtube_playlist:
#                     playlist_data = youtube_playlist[playlist_id]
#                     if "youtube_id" not in song:
#                         for video_id in playlist_data:
#                             if song["name"] == playlist_data[video_id]:
#                                 song["youtube_id"] = video_id
#                                 if playlist_id not in release["youtube_playlist_id"]:
#                                     release["youtube_playlist_id"].append(playlist_id)
#                                 if playlist_data["img"] not in release["cover_youtube"]:
#                                     release["cover_youtube"].append(
#                                         playlist_data["img"]
#                                     )

# for release_type in result:
#     for release in result[release_type]:
#         if "versions" not in release:
#             release["versions"] = {}
#         print(release["title"], len(release["youtube_playlist_id"]))
#         if len(release["youtube_playlist_id"]) > 1:
#             i = 0
#             for version in release["versions"]:
#                 if version == "アニメ盤":
#                     continue

#                 print(version, i)
#                 release["versions"][version]["youtube_playlist_id"] = release[
#                     "youtube_playlist_id"
#                 ][i]
#                 release["versions"][version]["cover_youtube"] = release[
#                     "cover_youtube"
#                 ][i]
#                 i += 1
#             del release["youtube_playlist_id"]
#             del release["cover_youtube"]
#         else:
#             if release["title"] == "Monopoly":
#                 continue
#             release["versions"]["配信"] = {}
#             release["versions"]["配信"]["youtube_playlist_id"] = release[
#                 "youtube_playlist_id"
#             ][0]
#             release["versions"]["配信"]["cover_youtube"] = release["cover_youtube"][0]
#             del release["youtube_playlist_id"]
#             del release["cover_youtube"]


for single in result["NS"]:
    for version in single["versions"]:
        for llc_release in llc_data:
            if single["title"][:-2] in llc_release[0] and version in llc_release[0]:
                # single["versions"][version]["cover_llc"] = llc_release[2].replace(
                #     "500_320_102400.jpg", "1000_1000_102400.jpg"
                # )
                single["date_llc"] = llc_release[1]
            elif single["title"][:-2] in llc_release[0]:
                # single["versions"]["通常盤"]["cover_llc"] = llc_release[2].replace(
                #     "500_320_102400.jpg", "1000_1000_102400.jpg"
                # )
                single["date_llc"] = llc_release[1]

    print(
        single["title"],
        json.dumps(single["versions"], ensure_ascii=False, indent=2, sort_keys=True),
    )


# Write back the JSON data with increased indentation
with open("discography.json", mode="w", encoding="utf-8") as src:
    json.dump(result, src, ensure_ascii=False, indent=2)

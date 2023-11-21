import json
from utility import list_deduplication

# Read existing JSON data from the file
with open("songs_crawled.json", mode="r") as src:
    data = json.load(src)
with open("members.json", mode="r") as src:
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
        songs[included_in]["version"] = song["version"]
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

# Write back the JSON data with increased indentation
with open("songs.json", mode="w", encoding="utf-8") as src:
    json.dump(songs, src, ensure_ascii=False, indent=2)

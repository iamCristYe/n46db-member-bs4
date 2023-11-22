import json
from utility import list_deduplication

# Read existing JSON data from the file
with open("discography.json", mode="r") as src:
    data = json.load(src)

for release_type in data:
    for release in data[release_type]:
        # if "date_llc" in release:
        #     print(
        #         release["date"].replace("年", "").replace("月", "").replace("日", "")
        #         == release["date_llc"].replace(".", ""),
        #     )
        # else:
        #     print(release["date"])
        if "date_llc" in release:
            release["date"] = release["date_llc"].replace(".", "")
            del release["date_llc"]
        release["date"] = (
            release["date"].replace("年", "").replace("月", "").replace("日", "")
        )

with open("youtube-mv.json", mode="r") as src:
    mv_data = json.load(src)
    for mv in mv_data:
        flag = True
        for release_type in data:
            for release in data[release_type]:
                for track in release["tracks"]:
                    if track["name"] in mv[0]:
                        track["mv_youtube_id"] = mv[1]
                        flag = False
        if flag:
            print(mv)


# Write back the JSON data with increased indentation
with open("discography.json", mode="w", encoding="utf-8") as src:
    json.dump(data, src, ensure_ascii=False, indent=2)

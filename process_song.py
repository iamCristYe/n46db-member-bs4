import json

# Read existing JSON data from the file
with open("songs_1.json", mode="r") as src:
    data = json.load(src)


# Write back the JSON data with increased indentation
with open("songs_1.json", mode="w", encoding="utf-8") as src:
    json.dump(data, src, ensure_ascii=False, indent=2)

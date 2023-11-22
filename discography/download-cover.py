from utility import download_image
import json

with open("discography.json", mode="r") as src:
    data = json.load(src)
    for release_type in data:
        for i in range(len(data[release_type])):
            release = data[release_type][i]
            print(release["versions"])
            for version in release["versions"]:
                type = release["versions"][version]
                if "cover_youtube" in type:
                    download_image(
                        type["cover_youtube"],
                        f"img/{release_type}-{i+1}-{version}-youtube.jpg",
                    )
                if "cover_llc" in type:
                    download_image(
                        type["cover_llc"],
                        f"img/{release_type}-{i+1}-{version}-llc.jpg",
                    )
                

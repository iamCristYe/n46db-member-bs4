import requests
import os


def download_image(img_src_url: str) -> str:
    response = requests.get(img_src_url)
    img_relative_path = f"images/{img_src_url.split('/')[-3]}/{img_src_url.split('/')[-2]}/{img_src_url.split('/')[-1]}"
    os.makedirs(os.path.dirname(img_relative_path), exist_ok=True)
    with open(img_relative_path, "wb") as f:
        f.write(response.content)

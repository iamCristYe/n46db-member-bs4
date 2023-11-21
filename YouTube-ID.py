import yt_dlp

# Create a YouTube downloader instance
ydl = yt_dlp.YoutubeDL({"skip_download": "True"})

# Specify the playlist URL or ID you want to retrieve videos from
playlist_url = (
    "https://www.youtube.com/playlist?list=OLAK5uy_m27WfKV20t1NZ9rNTQqt9tSn9QOzVwxms"
)

# Extract video titles and IDs
with ydl:
    playlist_info = ydl.extract_info(playlist_url, download=False)
    videos = playlist_info["entries"]

    for video in videos:
        video_title = video["title"]
        video_id = video["id"]
        print(f"Video Title: {video_title}, Video ID: {video_id}")

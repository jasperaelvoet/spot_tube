import re
import urllib.request


def search_video(query: str) -> str:
    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v=" + video_ids[0]

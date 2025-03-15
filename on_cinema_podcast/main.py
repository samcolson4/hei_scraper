from bs4 import BeautifulSoup
import json
from datetime import datetime

with open("on_cinema_podcast/podcast_html.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

episodes_json = []

base_url = "https://oncinematimeline.com"

for episode_div in soup.select(".episode.podcast"):
    # Skip if it's a 'bonus' without episode URL (bonus handled separately if needed)
    anchor = episode_div.select_one("a")
    if not anchor or not anchor.get("href"):
        continue

    import requests
    full_episode_url = base_url + anchor["href"]
    episode_title = anchor.text.strip()

    youtube_link = None
    try:
        episode_res = requests.get(full_episode_url)
        if episode_res.ok:
            episode_soup = BeautifulSoup(episode_res.text, "html.parser")
            yt_anchor = episode_soup.find("a", href=lambda href: href and "youtube.com" in href)
            if yt_anchor:
                youtube_link = yt_anchor["href"]
    except Exception as e:
        print(f"Error fetching YouTube link from {full_episode_url}: {e}")

    description_el = episode_div.select_one(".episode_description")
    episode_description = description_el.text.strip() if description_el else ""

    poster_img = episode_div.select_one("img")
    poster_url = base_url + poster_img["src"] if poster_img else None

    date_el = episode_div.select_one(".episode_date")
    if date_el:
        aired_at = datetime.strptime(date_el.text.strip(), "%m/%d/%Y").isoformat()
    else:
        aired_at = None

    is_bonus = "bonus" in episode_div.get("class", [])
    collection = "Bonus Podcast" if is_bonus else "Podcast Archive"
    show = "on_cinema_podcast"

    episode_data = {
        "episode_url": youtube_link or full_episode_url,
        "collection": collection,
        "episode_title": episode_title,
        "poster_url": poster_url,
        "aired_at": aired_at,
        "show": show,
        "media_type": "podcast"
    }

    episodes_json.append(episode_data)

# Output as JSON
with open("on_cinema_podcast/podcasts.json", "w", encoding="utf-8") as out_file:
    json.dump(episodes_json, out_file, indent=2)

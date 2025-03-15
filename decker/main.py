import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
import pdb
import glob

from bs4 import BeautifulSoup
import json

with open("raw_html.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

episodes = []

episode_divs = soup.select("div.episode.decker")

for div in episode_divs:
    title_tag = div.select_one(".episode_title_text h4 a")
    collection = title_tag.text.strip() if title_tag else None
    url = title_tag['href'] if title_tag else None

    description_tag = div.select_one(".episode_description")
    episode_title = description_tag.text.strip() if description_tag else None

    date_tag = div.select_one(".episode_date")
    date_str = date_tag.text.strip() if date_tag else None
    try:
        date = datetime.strptime(date_str, "%m/%d/%Y").isoformat()
    except Exception:
        date = date_str

    image_tag = div.select_one(".episode_thumb img")
    image_url = image_tag['src'] if image_tag else None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    episode_url = "https://oncinematimeline.com" + url
    response = requests.get(episode_url, headers=headers)
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, "html.parser")
      media_links_section = soup.find("div", class_="video-links")

      if media_links_section:
        youtube_link_tag = media_links_section.find("a", string="Youtube")
        episode_link = None
        if youtube_link_tag:
            episode_link = youtube_link_tag.get("href")
        else:
            adultswim_link_tag = media_links_section.find("a", string="Adult Swim")
            if adultswim_link_tag:
                episode_link = adultswim_link_tag.get("href")

        if episode_link:
            episodes.append({
                "collection": collection,
                "episode_title": episode_title,
                "episode_description": "",
                "aired_at": date,
                "episode_url": episode_link,
                "poster_url": image_url,
                "show": "decker",
                "media_type": "episode"
            })

# Output result
with open("parsed_episodes.json", "w", encoding="utf-8") as f:
    json.dump(episodes, f, indent=2)

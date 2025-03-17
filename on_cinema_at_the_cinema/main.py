import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
import pdb
import glob
import re

def get_latest_json_file():
    json_files = glob.glob("episodes_*.json")
    if not json_files:
        return None
    return max(json_files, key=os.path.getctime)


def load_existing_urls():
    latest_file = get_latest_json_file()
    if not latest_file:
        return set()
    try:
        with open(latest_file, "r") as file:
            data = json.load(file)
            return {item.get("episode_url") for item in data if "episode_url" in item}
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def extract_date(air_date_str):
    date_part = air_date_str.split(": ")[1]
    return datetime.strptime(date_part, "%m/%d/%Y")


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return (
            obj.isoformat()
        )  # Converts to ISO 8601 format (e.g., "2015-04-01T00:00:00")
    raise TypeError("Type not serializable")


def normalize_text(text):
    import unicodedata

    normalized = unicodedata.normalize("NFKC", text)
    normalized = (
        normalized.replace("\u2018", "'").replace("\u2019", "'").replace("\u2013", "-")
    )

    return normalized


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def append_to_json(file_name, data):
    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            json.dump([], file)

    try:
        with open(file_name, "r") as file:
            existing_data = json.load(file)
            if not isinstance(existing_data, list):
                existing_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(data)

    with open(file_name, "w") as file:
        json.dump(existing_data, file, default=serialize_datetime, indent=4)


with open("episodes.txt", "r") as file:
    now = datetime.now()
    formatted_time = now.strftime("%d_%m_%y_%H_%M")
    filename = f"episodes_{formatted_time}.json"
    existing_urls = load_existing_urls()
    processed_urls = set()

    for line in file:
        episode_url = "https://" + line.strip()
        if episode_url in existing_urls:
            print(f"Skipping existing episode: {episode_url}")
            continue
        if episode_url in processed_urls:
            print(f"Already processed during this run, skipping: {episode_url}")
            continue

        data = {
            "franchise": "on_cinema",
            "media_type": "episode",
            "season_name": "",
            "season_number": None,
            "title": "",
            "date_published": "",
            "published_by": None,
            "url": episode_url,
            "poster_url": "",
            "is_bonus": False,
            "is_meta": False
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(episode_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            data["season_name"] = normalize_text(
                soup.find(
                    class_="text-yellow m-0 text-lg font-bold uppercase"
                ).text.strip()
            )
            if data["season_name"].lower() == "bonus content":
                data["is_bonus"] = True
            import re
            match = re.search(r"Season\s+(\d+)", data["season_name"], re.IGNORECASE)
            if match:
                data["season_number"] = int(match.group(1))
            else:
                data["season_number"] = None

            data["title"] = normalize_text(
                soup.find(
                    class_="text-yellow semibold col-span-full md:text-5xl m-0 text-3xl"
                ).text.strip()
            )
            data["date_published"] = extract_date(
                normalize_text(soup.find(class_="text-red font-bold").text.strip())
            )
            data["poster_url"] = normalize_text(
                soup.find(
                    "img", class_="attachment-master size-master wp-post-image"
                ).get("src")
            )

            print(data)
            if data["url"] in existing_urls:
                print(f"Duplicate URL detected, skipping append: {data['url']}")
                continue
            append_to_json(filename, data)
            processed_urls.add(episode_url)
        else:
            print(
                f"Failed to retrieve the webpage. Status code: {response.status_code}"
            )

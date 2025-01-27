import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def extract_date(air_date_str):
    date_part = air_date_str.split(": ")[1]
    return datetime.strptime(date_part, "%m/%d/%Y")


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Converts to ISO 8601 format (e.g., "2015-04-01T00:00:00")
    raise TypeError("Type not serializable")


def normalize_text(text):
    import unicodedata

    normalized = unicodedata.normalize("NFKC", text)
    normalized = normalized.replace("\u2018", "'").replace("\u2019", "'")

    return normalized


def append_to_json(file_name, data):
    try:
        with open(file_name, "r") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(data)

    with open(file_name, "w") as file:
        json.dump(existing_data, file, default=serialize_datetime, indent=4)


with open("episodes.txt", "r") as file:
    for line in file:
        episode_url = "https://" + line.strip()
        data = {
            "episode_url": episode_url,
            "collection": "",
            "episode_title": "",
        }

        response = requests.get(episode_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            data["collection"] = normalize_text(
                soup.find(class_="text-yellow m-0 text-lg font-bold uppercase").text.strip()
            )
            data["episode_title"] = normalize_text(
                soup.find(class_="text-yellow semibold col-span-full md:text-5xl m-0 text-3xl").text.strip()
            )
            data["aired_at"] = extract_date(
                normalize_text(soup.find(class_="text-red font-bold").text.strip())
            )

            print(data)
            append_to_json("episode_json.json", data)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

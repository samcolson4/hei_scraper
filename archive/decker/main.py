import csv
import json
from datetime import datetime  # Import only the class


# Define input and output file paths
csv_file_path = "decker_episodes.csv"
json_file_path = "decker_episodes.json"


def normalize_text(text):
    import unicodedata

    normalized = unicodedata.normalize("NFKC", text)
    normalized = (
        normalized.replace("\u2018", "'").replace("\u2019", "'").replace("\u2013", "-")
    )

    return normalized


# Read CSV file and transform data
episodes = []
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        dt = datetime.strptime(row["aired_at"], "%B %d, %Y")

        episode = {
            "episode_url": None,
            "collection": row["season"] if row["season"] else "Specials",
            "episode_title": normalize_text(row["episode_title"]),
            "poster_url": "",
            "aired_at": dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "show": "Decker",
            "media_type": "episode"
        }
        episodes.append(episode)

# Write to JSON file
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(episodes, json_file, indent=4)

print(f"JSON file created: {json_file_path}")

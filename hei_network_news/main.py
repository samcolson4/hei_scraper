from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json

def extract_article_urls(html_file: Path) -> set[str]:
    article_urls = set()
    with html_file.open("r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a['href']
            if "/article" in href:
                article_urls.add(href)
    return article_urls


def extract_article_metadata(article_html: str) -> dict:
    soup = BeautifulSoup(article_html, "html.parser")
    metadata = {"published_at": None, "title": None, "poster_url": None, "published_by": None}

    # Extract publish date
    date_elem = (
        soup.find("time", class_="entry-date published updated")
        or soup.find("time", class_="entry-date published")
        or soup.find("span", class_="posted-on")
    )
    if date_elem:
        datetime_attr = date_elem.get("datetime")
        if datetime_attr:
            try:
                metadata["published_at"] = datetime.fromisoformat(datetime_attr)
            except ValueError:
                pass
        else:
            try:
                metadata["published_at"] = datetime.strptime(date_elem.text.strip(), "%B %d, %Y")
            except ValueError:
                pass

    # Extract article title
    title_elem = soup.find("h1", class_="entry-title bold blue")
    if title_elem:
        metadata["title"] = title_elem.text.strip()

    # Extract poster image
    thumbnail_div = soup.find("div", class_="post-thumbnail")
    if thumbnail_div:
        img = thumbnail_div.find("img")
        if img and img.get("src"):
            metadata["poster_url"] = img.get("src")

    # Extract published_by
    meta_elem = soup.find(class_="entry-meta")
    if meta_elem:
        text = meta_elem.get_text(strip=True)
        if "by " in text:
            published_by = text.split("by ", 1)[-1].strip()
            metadata["published_by"] = published_by
        else:
            metadata["published_by"] = None
    else:
        metadata["published_by"] = None

    return metadata


def main():
    now = datetime.now()
    formatted_time = now.strftime("%d_%m_%y_%H_%M")
    filename = f"articles_{formatted_time}.json"

    article_files = sorted(Path(".").glob("articles_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if article_files:
        with open(article_files[0], "r", encoding="utf-8") as old_f:
            existing_articles = json.load(old_f)
    else:
        existing_articles = []

    existing_urls = {article.get("url") for article in existing_articles}

    articles = existing_articles
    html_file = Path("./news_15_03_25.html")
    article_urls = extract_article_urls(html_file)
    print(f"Found {len(article_urls)} article URLs:")

    for url in sorted(article_urls):
        print(f"Fetching: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            metadata = extract_article_metadata(response.text)
            if url in existing_urls:
                print(f"Skipping existing article: {url}")
                continue
            article_data = {
                "franchise": None,
                "media_type": "article",
                "season_name": None,
                "season_number": None,
                "title": metadata["title"],
                "date_published": metadata["published_at"].isoformat() if metadata["published_at"] else None,
                "published_by": metadata["published_by"],
                "url": url,
                "poster_url": metadata["poster_url"],
                "is_bonus": False,
                "is_meta": False
            }
            articles.append(article_data)

            print(json.dumps(article_data, indent=2, ensure_ascii=False))

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"  → Failed to fetch or parse: {e}")


if __name__ == "__main__":
    main()

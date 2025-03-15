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
    metadata = {"published_at": None, "title": None, "poster_url": None}

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

    return metadata


def main():
    html_file = Path("./hei_network_news/news_15_03_25.html")
    article_urls = extract_article_urls(html_file)
    print(f"Found {len(article_urls)} article URLs:")

    articles = []
    for url in sorted(article_urls):
        print(f"Fetching: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            metadata = extract_article_metadata(response.text)
            article_data = {
                "media_type": "article",
                "collection": "news",
                "article_title": metadata["title"],
                "article_url": url,
                "posted_at": metadata["published_at"].isoformat() if metadata["published_at"] else None,
                "poster_url": metadata["poster_url"],
            }
            articles.append(article_data)
        except Exception as e:
            print(f"  → Failed to fetch or parse: {e}")

    with open("hei_network_news/articles.json", "w", encoding="utf-8") as f:
      json.dump(articles, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

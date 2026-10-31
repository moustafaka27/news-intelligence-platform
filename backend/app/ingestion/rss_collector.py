import json
import calendar
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import requests

from processing.cleaner import clean_text, create_content_hash
from ingestion.sources import NEWS_SOURCES


def collect_from_source(source):
    print(f"Collecting from: {source['name']}")

    try:
        response = requests.get(
            source["url"],
            timeout=20,
            headers={"User-Agent": "NewsIntelligencePlatform/1.0"}
        )

        response.raise_for_status()

        feed = feedparser.parse(response.content)

        articles = []

        for entry in feed.entries:
            title = clean_text(entry.get("title", ""))
            summary = clean_text(entry.get("summary", ""))
            url = entry.get("link", "").strip()

            if not title or not url:
                continue

            published_at = None

            if entry.get("published_parsed"):
                timestamp = calendar.timegm(
                    entry.published_parsed
                )

                published_at = datetime.fromtimestamp(
                    timestamp,
                    tz=timezone.utc
                ).isoformat()

            article = {
                "source": source["name"],
                "language": source["language"],
                "category": source["category"],
                "country": source["country"],
                "title": title,
                "summary": summary,
                "url": url,
                "published_at": published_at,
                "collected_at": datetime.now(
                    timezone.utc
                ).isoformat(),
                "content_hash": create_content_hash(title, url),
            }

            articles.append(article)

        print(f"Collected {len(articles)} articles.")

        return articles

    except requests.RequestException as error:
        print(f"Network error for {source['name']}: {error}")

    except Exception as error:
        print(f"Unexpected error for {source['name']}: {error}")

    return []


def collect_all_news():
    all_articles = []

    for source in NEWS_SOURCES:
        articles = collect_from_source(source)
        all_articles.extend(articles)

    # Remove duplicate URLs
    unique_articles = []
    seen_urls = set()

    for article in all_articles:
        if article["url"] not in seen_urls:
            seen_urls.add(article["url"])
            unique_articles.append(article)

    return unique_articles


def save_news(articles):
    output_path = Path("datasets/raw/news.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            articles,
            file,
            ensure_ascii=False,
            indent=4
        )

    print(f"\nSaved {len(articles)} articles to {output_path}")


if __name__ == "__main__":
    news = collect_all_news()
    save_news(news)
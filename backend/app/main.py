
from ingestion.rss_collector import collect_all_news
from processing.validator import validate_articles
from ingestion.sources import NEWS_SOURCES
from core.repository import save_source, save_article


def main():

    print("=" * 50)
    print("NEWS INTELLIGENCE PLATFORM")
    print("=" * 50)

    # Step 1: Collect news
    articles = collect_all_news()

    # Step 2: Validate articles
    valid_articles, rejected_articles = validate_articles(articles)

    inserted = 0
    skipped = 0

    # Step 3: Prepare source lookup
    sources_lookup = {
        source["name"]: source
        for source in NEWS_SOURCES
    }

    source_ids = {}

    # Step 4: Save articles directly to PostgreSQL
    for article in valid_articles:

        source_name = article["source"]
        source = sources_lookup.get(source_name)

        if source is None:
            rejected_articles.append(article)
            continue

        if source_name not in source_ids:
            source_ids[source_name] = save_source(source)

        source_id = source_ids[source_name]

        result = save_article(article, source_id)

        if result == 1:
            inserted += 1
        else:
            skipped += 1

    # Step 5: Final report
    print("\nPIPELINE REPORT")
    print("-" * 30)

    print(f"Collected articles: {len(articles)}")
    print(f"Valid articles: {len(valid_articles)}")
    print(f"Inserted articles: {inserted}")
    print(f"Skipped duplicates: {skipped}")
    print(f"Rejected articles: {len(rejected_articles)}")

    print("\nPIPELINE COMPLETED")


if __name__ == "__main__":
    main()

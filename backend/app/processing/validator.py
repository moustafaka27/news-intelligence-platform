def validate_articles(articles):
    valid_articles = []
    rejected_articles = []

    for article in articles:

        required_fields = [
            "title",
            "url",
            "source",
            "language",
            "collected_at",
        ]

        missing_fields = [
            field
            for field in required_fields
            if not article.get(field)
        ]

        if missing_fields:
            rejected_articles.append({
                "article": article,
                "missing_fields": missing_fields,
            })
        else:
            valid_articles.append(article)

    print("\nDATA QUALITY REPORT")
    print("-------------------")
    print(f"Total articles: {len(articles)}")
    print(f"Valid articles: {len(valid_articles)}")
    print(f"Rejected articles: {len(rejected_articles)}")

    return valid_articles, rejected_articles
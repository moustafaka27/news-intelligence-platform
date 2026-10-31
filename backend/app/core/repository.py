
from core.database import get_connection


def save_source(source):
    query = """
        INSERT INTO sources (
            name,
            url,
            language,
            category,
            country
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (name)
        DO UPDATE SET
            url = EXCLUDED.url,
            language = EXCLUDED.language,
            category = EXCLUDED.category,
            country = EXCLUDED.country
        RETURNING id;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                query,
                (
                    source["name"],
                    source["url"],
                    source["language"],
                    source.get("category"),
                    source.get("country"),
                ),
            )

            return cursor.fetchone()[0]


def save_article(article, source_id):
    query = """
        INSERT INTO articles (
            source_id,
            title,
            summary,
            url,
            language,
            category,
            country,
            published_at,
            collected_at,
            content_hash
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        ON CONFLICT (url) DO NOTHING;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                query,
                (
                    source_id,
                    article["title"],
                    article.get("summary"),
                    article["url"],
                    article["language"],
                    article.get("category"),
                    article.get("country"),
                    article.get("published_at"),
                    article["collected_at"],
                    article.get("content_hash"),
                ),
            )

            return cursor.rowcount

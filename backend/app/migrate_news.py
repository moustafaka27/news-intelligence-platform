
import json
from pathlib import Path

from core.repository import save_source, save_article
from ingestion.sources import NEWS_SOURCES


# تحديد المسار الرئيسي للمشروع
PROJECT_ROOT = Path(__file__).resolve().parents[2]

NEWS_FILE = PROJECT_ROOT / "datasets" / "raw" / "news.json"


def migrate_news():

    print("=" * 50)
    print("NEWS DATABASE MIGRATION")
    print("=" * 50)

    # التأكد من وجود ملف الأخبار
    if not NEWS_FILE.exists():
        print("ERROR: news.json file not found!")
        return

    # قراءة الأخبار
    with open(NEWS_FILE, "r", encoding="utf-8") as file:
        articles = json.load(file)

    print(f"Loaded articles: {len(articles)}")

    # إنشاء قاموس لمصادر الأخبار
    sources_lookup = {
        source["name"]: source
        for source in NEWS_SOURCES
    }

    source_ids = {}

    inserted = 0
    skipped = 0
    rejected = 0

    # نقل الأخبار إلى قاعدة البيانات
    for article in articles:

        source_name = article.get("source")

        source = sources_lookup.get(source_name)

        # التحقق من وجود المصدر
        if source is None:
            rejected += 1
            print(f"Unknown source: {source_name}")
            continue

        # إضافة المصدر مرة واحدة فقط
        if source_name not in source_ids:
            source_ids[source_name] = save_source(source)

        source_id = source_ids[source_name]

        # إضافة الخبر
        result = save_article(article, source_id)

        if result == 1:
            inserted += 1
        else:
            skipped += 1

    # تقرير النتائج
    print("\nMIGRATION REPORT")
    print("-" * 30)
    print(f"Total articles: {len(articles)}")
    print(f"Inserted articles: {inserted}")
    print(f"Skipped duplicates: {skipped}")
    print(f"Rejected articles: {rejected}")

    print("\nMIGRATION COMPLETED")


if __name__ == "__main__":
    migrate_news()

import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "news_intelligence"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}

if not DB_CONFIG["password"]:
    raise RuntimeError(
        "DB_PASSWORD is missing. Check your .env file."
    )


def get_connection():
    return psycopg.connect(**DB_CONFIG)


def test_connection():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                result = cursor.fetchone()

                print("POSTGRESQL CONNECTION SUCCESS")
                print(result[0])

    except psycopg.Error as error:
        print("DATABASE CONNECTION FAILED")
        print(error)


if __name__ == "__main__":
    test_connection()
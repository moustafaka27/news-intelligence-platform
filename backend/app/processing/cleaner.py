import re
import hashlib
from html import unescape


def clean_text(text):
    if not text:
        return ""

    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def create_content_hash(title, url):
    value = f"{title.strip().lower()}|{url.strip().lower()}"

    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()
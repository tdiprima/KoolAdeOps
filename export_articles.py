#!/usr/bin/env python3
"""Export all articles from research.db to a markdown file."""
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "research.db"
OUTPUT_PATH = Path(__file__).resolve().parent / "articles_export.md"


def fetch_all_articles(conn):
    cursor = conn.execute(
        "SELECT title, url, summary FROM articles ORDER BY fetched_at DESC"
    )
    return cursor.fetchall()


def format_article(title, url, summary):
    lines = []
    lines.append(f"### {title}")
    lines.append(f"<{url}>")
    if summary:
        lines.append(summary)
    else:
        lines.append("*No summary available.*")
    return "\n".join(lines)


def main():
    if not DB_PATH.exists():
        print(f"ERROR: DB not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    try:
        rows = fetch_all_articles(conn)
    finally:
        conn.close()

    if not rows:
        print("No articles found.", file=sys.stderr)
        sys.exit(0)

    blocks = [format_article(title, url, summary) for title, url, summary in rows]
    content = "\n\n\n".join(blocks) + "\n"

    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"Wrote {len(rows)} articles to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

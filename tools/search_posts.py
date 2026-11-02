"""Search your LinkedIn posts (shares) by keyword, date or link.

Usage:
  python3 -I tools/search_posts.py "agentic" [--year 2025] [--links-only] [--limit 20]
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "..", "Posts", "index.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", default="", help="words to match (all must appear, case-insensitive)")
    ap.add_argument("--year", help="only posts from this year")
    ap.add_argument("--links-only", action="store_true", help="only posts that share a public link")
    ap.add_argument("--limit", type=int, default=20)
    a = ap.parse_args()

    posts = json.load(open(INDEX, encoding="utf-8"))
    words = [w.lower() for w in a.query.split()]
    hits = []
    for p in posts:
        if a.year and not p["date"].startswith(a.year):
            continue
        if a.links_only and not p["has_public_link"]:
            continue
        text = " ".join([p["commentary"], p["shared_url"] or ""]).lower()
        if all(w in text for w in words):
            hits.append(p)
    hits.sort(key=lambda p: p["date"], reverse=True)
    print(f"{len(hits)} matching posts")
    for p in hits[: a.limit]:
        snippet = " ".join(p["commentary"].split())[:160]
        print(f"\n{p['date']}  {p['share_link']}")
        print(f"  {snippet}")
        if p["shared_url"]:
            print(f"  link: {p['shared_url']}")


if __name__ == "__main__":
    main()

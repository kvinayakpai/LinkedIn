"""Search the public links harvested from posts and shares.

Usage:
  python3 -I tools/search_links.py "forbes" [--domain youtube.com] [--min-times 2] [--year 2025] [--limit 30]
  python3 -I tools/search_links.py --top-domains 15
"""
import argparse
import collections
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LINKS = os.path.join(HERE, "..", "Links", "data", "unique_links.csv")


def load():
    with open(LINKS, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", default="", help="words that must appear in the URL (case-insensitive)")
    ap.add_argument("--domain", help="only links on this domain, e.g. youtube.com")
    ap.add_argument("--min-times", type=int, default=1, help="only links shared at least this many times")
    ap.add_argument("--year", help="only links last seen in this year")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--top-domains", type=int, metavar="N", help="list the N most common domains and exit")
    a = ap.parse_args()

    rows = load()
    if a.top_domains:
        c = collections.Counter(r["domain"] for r in rows)
        for d, n in c.most_common(a.top_domains):
            print(f"{n:5d}  {d}")
        return

    words = [w.lower() for w in a.query.split()]
    hits = []
    for r in rows:
        if a.domain and r["domain"] != a.domain.lower():
            continue
        if int(r["times_shared"]) < a.min_times:
            continue
        if a.year and not r["last_seen"].startswith(a.year):
            continue
        if all(w in r["url"].lower() for w in words):
            hits.append(r)
    hits.sort(key=lambda r: (-int(r["times_shared"]), r["last_seen"]), reverse=False)
    print(f"{len(hits)} matching links")
    for r in hits[: a.limit]:
        print(f"{r['times_shared']}x  {r['first_seen']} to {r['last_seen']}  {r['url']}")


if __name__ == "__main__":
    main()

"""Check which harvested links still work, and record the result.

Writes Links/data/link_status.csv (one row per distinct URL) and,
with --write-clean, Links/data/unique_links_working.csv without broken links.
Nothing is deleted from the source files; the original lists are kept as they were.

Usage (run on a machine with internet access):
  python3 tools/check_links.py [--workers 16] [--timeout 15] [--write-clean]
  python3 tools/check_links.py --only-domain forbes.com
"""
import argparse
import concurrent.futures as cf
import csv
import os
import socket
import ssl
import urllib.error
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "Links", "data")
SRC = os.path.join(DATA, "unique_links.csv")
STATUS = os.path.join(DATA, "link_status.csv")
CLEAN = os.path.join(DATA, "unique_links_working.csv")
UA = "Mozilla/5.0 (link checker for a personal reference list)"


def check(url, timeout):
    """Return (status, code, final_url). status is ok, redirect, blocked, broken or error."""
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            final = r.geturl()
            code = r.status
            return ("ok" if final == url else "redirect", code, final)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403, 429):
            return ("blocked", e.code, url)
        return ("broken", e.code, url)
    except (urllib.error.URLError, socket.timeout, ssl.SSLError, ConnectionError, OSError) as e:
        return ("error", "", str(getattr(e, "reason", e))[:120])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--only-domain")
    ap.add_argument("--write-clean", action="store_true", help="also write the list of working links")
    a = ap.parse_args()

    rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
    if a.only_domain:
        rows = [r for r in rows if r["domain"] == a.only_domain]
    checked = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        results = list(ex.map(lambda r: check(r["url"], a.timeout), rows))

    with open(STATUS, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["url", "domain", "times_shared", "status", "http_code", "final_url_or_error", "checked_on"])
        for r, (st, code, info) in zip(rows, results):
            w.writerow([r["url"], r["domain"], r["times_shared"], st, code, info, checked])

    if a.write_clean:
        keep = [r for r, (st, _, _) in zip(rows, results) if st in ("ok", "redirect", "blocked")]
        with open(CLEAN, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(keep)
        print(f"working or blocked-but-live: {len(keep)} of {len(rows)}")

    counts = {}
    for st, _, _ in results:
        counts[st] = counts.get(st, 0) + 1
    print(counts)


if __name__ == "__main__":
    main()

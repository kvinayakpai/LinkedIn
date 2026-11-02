# LinkedIn

My LinkedIn content, exported from my LinkedIn data export (2026-11-02).

- `Articles/` – 70 published LinkedIn articles (HTML, each links to its original).
- `Posts/shares.csv` – all 2,544 shared posts from the export, with my commentary and any shared link.
- `Posts/index.json` – the same posts as JSON, with a `has_public_link` flag (580 posts share a link).
- `tools/search_posts.py` – keyword search over the posts, optionally by year or links only.

Search examples:

    python3 -I tools/search_posts.py "agentic" --year 2025
    python3 -I tools/search_posts.py "data" --links-only --limit 50

Posts are marked `MEMBER_NETWORK` in the export, meaning they were visible to LinkedIn members only.

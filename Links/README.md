# LinkedIn shared links

Every public link harvested from my LinkedIn posts and shares (export of 2026-11-02, 2,544 shares).

Links come from two places in each post:
- `shared_url`: the link attached to a share.
- `in_commentary`: any http(s) link written in the commentary.

Files:
- `Links/data/links.csv`: one row per link per post (1,322 rows): date, share link, URL, domain, source.
- `Links/data/unique_links.csv` and `.json`: one row per distinct URL (1,179), with how many times it was shared and first and last seen dates. Sorted by times shared.

Notes:
- 660 links are `lnkd.in` short links, which LinkedIn uses for redirects. They are kept as written, not resolved.
- Some links are shortened or tracking links (`okt.to`, `bit.ly`, `share.google`). They are not resolved or checked.
- Links are as exported. Being listed here does not mean I endorse the page.

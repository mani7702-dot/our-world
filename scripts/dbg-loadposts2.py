#!/usr/bin/env python3
import sys, os
sys.path.insert(0, "/home/ubuntu/our-world")
import build
print("=== FILES in content/news/ matching slug ===")
for fn in sorted(os.listdir(os.path.join(build.CONTENT_DIR, "news"))):
    if "history" in fn or "solar" in fn:
        print("  ", fn)
print("=== load_posts('news') slugs ===")
news = build.load_posts("news")
for p in news:
    print("  slug:", p["slug"], "has fg:", "for-grown-ups" in p, "fgbool:", bool(p.get("for-grown-ups","")))
    if p["slug"] == "history-solar-storm-train-delay-typo":
        print("    >>> MATCH FOUND, fg len:", len(p.get("for-grown-ups","")))
print("total news posts:", len(news))
# Did parse_frontmatter see it? Re-parse manually
fp = os.path.join(build.CONTENT_DIR, "news", "history-solar-storm-train-delay-typo.md")
meta, body = build.parse_frontmatter(build.read(fp))
print("manual parse keys:", sorted(meta.keys()), "fg in meta:", "for-grown-ups" in meta)
print("manual fg len:", len(meta.get("for-grown-ups","")), "bool:", bool(meta.get("for-grown-ups","")))

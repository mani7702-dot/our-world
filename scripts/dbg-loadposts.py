#!/usr/bin/env python3
import sys
sys.path.insert(0, "/home/ubuntu/our-world")
import build
news = build.load_posts("news")
for p in news:
    if p["slug"] == "history-solar-storm-train-delay-typo":
        print("=== POST FOUND ===")
        print("keys:", sorted(p.keys()))
        print("has for-grown-ups?:", "for-grown-ups" in p)
        fg = p.get("for-grown-ups", "")
        print("for-grown-ups repr[:80]:", repr(fg)[:80])
        print("bool:", bool(fg), "len:", len(fg))
        # Run the actual article_page internal logic
        section = p["section"]
        grownups = ""
        if p.get("for-grown-ups"):
            grownups = ('<aside class="grownups" data-reveal>\n'
                        "      <h2>For grown-ups</h2>\n"
                        "      <p>%s</p>\n"
                       "    </aside>") % build.esc(p["for-grown-ups"])
        print("grownups built?:", "grownups" in grownups, "len:", len(grownups))
        break
else:
    print("SLUG NOT FOUND in news posts!")
    print("slugs:", [x["slug"] for x in news[:5]], "...", len(news), "total")

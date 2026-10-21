#!/usr/bin/env python3
import sys
sys.path.insert(0, "/home/ubuntu/our-world")
import build
news = build.load_posts("news")
for p in news:
    if p["slug"] == "history-solar-storm-train-delay-typo":
        try:
            html = build.article_page(p)
            print("article_page returned, len:", len(html))
            print("grownups in output?:", "grownups" in html)
        except Exception as e:
            import traceback
            print("EXCEPTION in article_page:")
            traceback.print_exc()
        break

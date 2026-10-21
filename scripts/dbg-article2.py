#!/usr/bin/env python3
import sys, os
sys.path.insert(0, "/home/ubuntu/our-world")
import build
news = build.load_posts("news")
for p in news:
    if p["slug"] == "history-solar-storm-train-delay-typo":
        print("Calling article_page...")
        try:
            ret = build.article_page(p)
            print("article_page returned:", repr(ret), "len:", len(ret) if ret else "N/A")
        except Exception as e:
            import traceback
            print("EXCEPTION:")
            traceback.print_exc()
        # Read the file it wrote
        outp = os.path.join(build.ROOT, "news", p["slug"] + ".html")
        if os.path.exists(outp):
            content = open(outp, encoding="utf-8").read()
            print("OUTPUT FILE len:", len(content))
            print("grownups in output?:", "grownups" in content)
            # show what's around where aside should be
            idx = content.find("</figure>")
            if idx >= 0:
                print("around first /figure:", content[idx:idx+400])
        else:
            print("OUTPUT FILE MISSING")
        break

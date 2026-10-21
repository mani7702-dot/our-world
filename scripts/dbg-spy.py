#!/usr/bin/env python3
import sys, os
sys.path.insert(0, "/home/ubuntu/our-world")
import build

# Capture what article_page passes to page()/render
orig_render = build.render
captured = {}
def spy_render(name, tokens):
    if name == "article.html":
        captured["GROWNUPS"] = tokens.get("GROWNUPS", "<MISSING>")
        captured["GROWNUPS_len"] = len(tokens.get("GROWNUPS", "") or "")
        captured["all_keys"] = sorted(tokens.keys())
    return orig_render(name, tokens)
build.render = spy_render

news = build.load_posts("news")
p = next(x for x in news if x["slug"]=="history-solar-storm-train-delay-typo")
print("PRE article_page: fg len:", len(p.get("for-grown-ups","")))
try:
    build.article_page(p)
    print("article_page completed without error")
except SystemExit as e:
    print("SystemExit:", e)
print("CAPTURED GROWNUPS_len:", captured.get("GROWNUPS_len"))
g = captured.get("GROWNUPS","")
print("CAPTURED GROWNUPS empty?:", not g, "has 'aside'?:", "aside" in g, "has 'grownups'?:", "grownups" in g)
print("CAPTURED GROWNUPS repr[:100]:", repr(g)[:100])

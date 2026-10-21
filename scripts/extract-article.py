#!/usr/bin/env python3
"""Extract article text from a saved HTML file (robust for ScienceDaily layout)."""
import sys, re, html
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip_depth = 0
        self.text = []
        self.capture = False
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("script", "style", "svg", "noscript"):
            self.skip_depth += 1
        cls = d.get("class", "")
        # ScienceDaily wraps content in div#text-body-content or similar
        if tag == "div" and ("text-body" in cls or "article_body" in cls or "post-body" in cls or "story" in cls):
            self.capture = True
    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg", "noscript"):
            if self.skip_depth > 0:
                self.skip_depth -= 1
        if tag == "div":
            self.capture = False
    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        if self.capture:
            s = html.unescape(data).strip()
            if s:
                self.text.append(s)

if len(sys.argv) < 2:
    print("usage: extract-article.py <saved.html>")
    sys.exit(1)

filepath = sys.argv[1]
html_content = open(filepath, encoding="utf-8", errors="replace").read()

# Title
m = re.search(r"<title[^>]*>(.*?)</title>", html_content, re.S|re.I)
title = m.group(1).strip() if m else "(no title)"
# Meta description
md = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html_content, re.I)
desc = md.group(1).strip() if md else ""

# Find all paragraph text
paras = re.findall(r"<p[^>]*>(.*?)</p>", html_content, re.S|re.I)
clean = []
for p in paras:
    # strip tags
    t = re.sub(r"<[^>]+>", " ", p)
    t = html.unescape(t).strip()
    t = re.sub(r"\s+", " ", t)
    if len(t) > 30:
        clean.append(t)

full = "\n".join(clean)

print("TITLE:", title)
if desc:
    print("META DESC:", desc)
print("=" * 60)
print(full[:5000])
print("=" * 60)
keywords = ["first five minutes", "big bang", "helium", "universe", "cosmic", "galaxies",
            "black hole", "supermassive", "collision", "doomsday", "November 13",
            "monster", "100 years"]
print("\nKEYWORD COUNTS:")
for kw in keywords:
    c = full.lower().count(kw.lower())
    if c:
        print(f"  {kw}: {c}")
print("\nEST WORD COUNT:", len(full.split()))

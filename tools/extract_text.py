#!/usr/bin/env python3
"""Extract article body text from ScienceDaily HTML."""
import re, sys

html = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
text = re.sub(r"<[^>]+>", " ", html)
text = re.sub(r"\s+", " ", text)
# Find the article body - look for the headline and print what follows
start = text.find(sys.argv[2])
if start >= 0:
    print(text[start:start+3000])
else:
    print("NOT FOUND")

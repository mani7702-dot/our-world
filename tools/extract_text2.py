#!/usr/bin/env python3
"""Extract more text from ScienceDaily article."""
import re, sys

html = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
text = re.sub(r"<[^>]+>", " ", html)
text = re.sub(r"\s+", " ", text)
start = text.find("Combining Three Decades")
if start >= 0:
    print(text[start:start+3000])
else:
    print("NOT FOUND")

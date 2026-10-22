#!/usr/bin/env python3
"""dupe-grep the fetch-news candidates against content/blog + content/news"""
import os, re

ROOT = "/home/ubuntu/our-world"
CANDIDATES = os.path.join(ROOT, "_candidates.txt")
CONTENT_DIRS = [os.path.join(ROOT, "content/blog"), os.path.join(ROOT, "content/news")]

with open(CANDIDATES, encoding="utf-8") as f:
    phrases = [ln.strip() for ln in f if ln.strip()]

for p in phrases:
    # extract 3+ stable core tokens to avoid false positives on generic words
    tokens = [t for t in re.split(r'[^A-Za-z0-9]+', p) if len(t) >= 4]
    core = " ".join(tokens[:4]) if len(tokens) >= 4 else p
    found = []
    for d in CONTENT_DIRS:
        if not os.path.isdir(d):
            continue
        for fname in sorted(os.listdir(d)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(d, fname)
            try:
                with open(fpath, encoding="utf-8", errors="replace") as fh:
                    txt = fh.read()
            except Exception:
                continue
            haystack = p.lower()
            if re.search(re.escape(haystack[:28].lower()), txt.lower()) or \
               (tokens and all(t.lower() in txt.lower() for t in tokens[:3] if len(t) >= 5)):
                rel = fpath.replace(ROOT + "/", "")
                found.append(rel)
    status = "DUP" if found else "FRESH"
    print(f"[{status}] {p}")
    for fnd in found:
        print(f"    -> {fnd}")

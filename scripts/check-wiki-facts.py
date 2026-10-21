#!/usr/bin/env python3
"""Extract key facts from Wikipedia lake articles for cross-check. File-based (Tirith-safe)."""
import re, html as H

def extract_text(path):
    h = open(path, encoding="utf-8", errors="ignore").read()
    # First paragraph(s) from body content
    # Remove tags
    t = re.sub(r'<script.*?</script>', '', h, flags=re.S)
    t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = H.unescape(t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

for name, path in [
    ("LAKE NATRON", "/tmp/wiki-natron.html"),
    ("ABRAHAM LAKE", "/tmp/wiki-abraham.html"),
    ("KAINDY LAKE", "/tmp/wiki-kaindy.html"),
    ("JELLYFISH LAKE", "/tmp/wiki-jelly.html"),
]:
    txt = extract_text(path)
    # Find the article lead paragraph (search for characteristic phrases)
    print(f"=== {name} ===")
    # Print first ~800 chars of article text after title marker
    idx = txt.find("Lake")
    if idx > 0:
        print(txt[idx:idx+1200])
    else:
        print(txt[:1200])
    print()

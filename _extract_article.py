#!/usr/bin/env python3
"""Extract full article text from a Universe Today URL using urllib (Tirith-safe)."""
import urllib.request, re, html as htmlmod, gzip, sys

url = sys.argv[1] if len(sys.argv) > 1 else "https://www.universetoday.com/articles/white-dwarfs-are-actuallyyellow-green-pink-and-purple"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip" or raw[:2] == b'\x1f\x8b':
            raw = gzip.decompress(raw)
        text = raw.decode('utf-8', errors='replace')
except Exception as e:
    print(f"FETCH ERROR: {e}")
    sys.exit(1)

# Extract article body — Universe Today uses <article> or .entry-content
article = ""
# Try article tag
m = re.search(r'<article[^>]*>(.*?)</article>', text, re.DOTALL | re.IGNORECASE)
if m:
    article = m.group(1)
# Fallback: .entry-content
if not article:
    m = re.search(r'class="entry-content[^"]*"[^>]*>(.*?)</div>', text, re.DOTALL | re.IGNORECASE)
    if m:
        article = m.group(1)
# Fallback: .post-content
if not article:
    m = re.search(r'class="post-content[^"]*"[^>]*>(.*?)</div>', text, re.DOTALL | re.IGNORECASE)
    if m:
        article = m.group(1)

if not article:
    print("Could not locate article body; dumping page title + length.")
    t = re.search(r'<title>(.*?)</title>', text, re.DOTALL | re.IGNORECASE)
    print(f"Title: {t.group(1) if t else 'N/A'}")
    print(f"Page length: {len(text)} chars")
    sys.exit(2)

# Strip scripts/styles
article = re.sub(r'<script.*?</script>', '', article, flags=re.DOTALL | re.IGNORECASE)
article = re.sub(r'<style.*?</style>', '', article, flags=re.DOTALL | re.IGNORECASE)
# Clean
article = re.sub(r'<[^>]+>', ' ', article)
article = htmlmod.unescape(article)
article = re.sub(r'\s+', ' ', article).strip()
print(f"ARTICLE LENGTH: {len(article)} chars")
print("=" * 60)
print(article[:4000])
print("=" * 60)

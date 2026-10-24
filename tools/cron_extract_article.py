#!/usr/bin/env python3
"""Fetch a single Space.com article body via urllib (Tirith-safe)."""
import urllib.request
import re

URL = "https://www.space.com/space-exploration/artemis/nasa-lays-out-plan-for-artemis-3-moon-lander-test-flight-but-when-will-it-launch"

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
req = urllib.request.Request(URL, headers={"User-Agent": UA})
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    print(f"Fetched {len(html)} bytes")
except Exception as e:
    print(f"FETCH ERROR: {e}")
    raise SystemExit(1)

# Strip scripts/styles
html = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL|re.IGNORECASE)
html = re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=re.DOTALL|re.IGNORECASE)
# Extract <p> content
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, flags=re.DOTALL|re.IGNORECASE)
text_parts = []
for p in paras:
    txt = re.sub(r'<[^>]+>', '', p).strip()
    if txt and len(txt) > 25:
        text_parts.append(txt)
body = "\n".join(text_parts)
print("\n--- ARTICLE BODY (first 6000 chars) ---")
print(body[:6000])

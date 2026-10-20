#!/usr/bin/env python3
"""Submit every URL in the live sitemap to IndexNow (Bing/Yandex/Seznam), free, no account.
Usage: python3 tools/indexnow-submit.py  (or --urls "a,b" for single new posts)
"""
import json, re, sys, urllib.request

KEY = "afd35788d7f52e6d423daf2f10f0a1c1"
KEY_LOC = "https://mani7702-dot.github.io/our-world/afd35788d7f52e6d423daf2f10f0a1c1.txt"
HOST = "mani7702-dot.github.io"
SITE = "https://mani7702-dot.github.io/our-world"

def fetch(url, data=None):
    req = urllib.request.Request(url, data=data,
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "OurWorld-indexing"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", "ignore")

def main():
    urls = []
    if "--urls" in sys.argv:
        urls = [u.strip() for u in sys.argv[sys.argv.index("--urls")+1].split(",")]
    else:
        status, body = fetch(SITE + "/sitemap.xml")
        urls = re.findall(r"<loc>([^<]+)</loc>", body)
    print(f"submitting {len(urls)} urls")
    # IndexNow caps at 10k; chunk to be safe
    for i in range(0, len(urls), 5000):
        chunk = urls[i:i+5000]
        try:
            status, body = fetch("https://api.indexnow.org/indexnow",
                json.dumps({"host": HOST, "key": KEY, "keyLocation": KEY_LOC, "urlList": chunk}).encode())
            print(f"  chunk {i//5000}: HTTP {status} {body[:200]}")
        except Exception as e:
            print(f"  chunk {i//5000}: ERROR {e}")

if __name__ == "__main__":
    main()

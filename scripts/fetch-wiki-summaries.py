#!/usr/bin/env python3
"""Fetch Wikipedia REST API summaries for lake fact-check. File-based (Tirith-safe)."""
import json, urllib.request, html

UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
LAKES = ["Lake_Natron", "Abraham_Lake", "Kaindy_Lake", "Jellyfish_Lake",
         "Lake_Kivu", "Lake_Maracaibo", "Lost_Lake_Oregon", "Lake_Toba"]

for name in LAKES:
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.loads(r.read())
        extract = data.get("extract", "")
        print(f"=== {name} ===")
        print(extract)
        print()
    except Exception as e:
        print(f"=== {name} === ERROR: {e}")
        print()

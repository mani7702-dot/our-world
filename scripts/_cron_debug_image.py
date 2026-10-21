#!/usr/bin/env python3
"""Debug: query Wikimedia Commons for Sherlock Holmes images and inspect licenses."""
import subprocess, urllib.parse, json

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
queries = [
    "Sherlock Holmes bust",
    "Sherlock Holmes 221B",
    "Arthur Conan Doyle",
    "Sherlock Holmes illustration",
    "Sidney Paget Sherlock Holmes",
]

def curl_json(params):
    url = API + "?" + urllib.parse.urlencode(params)
    p = subprocess.run(["curl","-s","--compressed","--max-time","30","-A",UA,url],
                       capture_output=True, text=True)
    try:
        return json.loads(p.stdout)
    except Exception:
        return None

for q in queries:
    print(f"\n=== QUERY: {q} ===")
    data = curl_json({"action":"query","format":"json","generator":"search",
                      "gsrsearch":"file:" + q,"gsrnamespace":"6","gsrlimit":"15",
                      "prop":"imageinfo","iiprop":"url|mime|extmetadata","iiurlwidth":"1200"})
    if not data:
        print("  no data"); continue
    pages = (data.get("query",{}) or {}).get("pages",{}) or {}
    for pid, pg in pages.items():
        ii = (pg.get("imageinfo") or [{}])[0]
        mime = ii.get("mime","")
        url = ii.get("thumburl") or ii.get("url","")
        lic = (ii.get("extmetadata",{}) or {}).get("LicenseShortName",{}).get("value","")
        title = pg.get("title","")
        print(f"  {title[:60]} mime={mime} lic={lic[:30]} url={url[:70]}")

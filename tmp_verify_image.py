#!/usr/bin/env python3
"""Verify the Commons image metadata for our galaxy cluster image."""
import urllib.parse, urllib.request, json

# Verify the exact file metadata
filename = "A colossal cluster PLCK G308.3-20.2.jpg"
api_url = "https://commons.wikimedia.org/w/api.php"
params = {
    "action": "query",
    "format": "json",
    "titles": "File:" + filename,
    "prop": "imageinfo",
    "iiprop": "url|extmetadata|metadata",
    "iiurlwidth": "1200",
}
url = api_url + "?" + urllib.parse.urlencode(params)
req = urllib.request.Request(url, headers={"User-Agent": "HermesBot/1.0 (educational; contact@example.com)"})
raw = urllib.request.urlopen(req, timeout=30).read()
data = json.loads(raw.decode())

pages = data["query"]["pages"]
for pid, page in pages.items():
    if "imageinfo" in page:
        ii = page["imageinfo"][0]
        ext = ii.get("extmetadata", {})
        print(f"File: {page.get('title', '?')}")
        print(f"  License: {ext.get('LicenseShortName', {}).get('value', 'N/A')}")
        print(f"  License (long): {ext.get('LicenseLongName', {}).get('value', 'N/A')}")
        print(f"  Credit: {ext.get('Credit', {}).get('value', 'N/A')}")
        print(f"  Artist: {ext.get('Artist', {}).get('value', 'N/A')}")
        print(f"  ImageDescription: {ext.get('ImageDescription', {}).get('value', 'N/A')}")
        print(f"  Date: {ext.get('Date', {}).get('value', 'N/A')}")
        print(f"  Url: {ii.get('url', 'N/A')}")
        print(f"  Mime: {ii.get('mime', 'N/A')}")
    else:
        print(f"File: {page.get('title', '?')}")
        print(f"  Missing! (pageid={pid})")
        print(f"  Full page data: {json.dumps(page, indent=2)}")

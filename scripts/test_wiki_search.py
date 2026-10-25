#!/usr/bin/env python3
"""Get full image URL for a specific Wikimedia file."""
import urllib.request, urllib.parse, json, re

url = 'https://commons.wikimedia.org/w/api.php'
filename = 'File:Pacific Walrus - Bull (8247646168).jpg'

params = urllib.parse.urlencode({
    'action': 'query',
    'format': 'json',
    'prop': 'imageinfo',
    'iiprop': 'url|extmetadata',
    'titles': filename,
})
req = urllib.request.Request(url + '?' + params, headers={'User-Agent': 'OurWorldSite/1.0'})
resp = urllib.request.urlopen(req, timeout=30)
data = json.loads(resp.read().decode('utf-8'))

pages = data.get('query', {}).get('pages', {})
for page_id, page in pages.items():
    ii = page.get('imageinfo', [{}])[0] if page.get('imageinfo') else {}
    ext_meta = ii.get('extmetadata', {})
    license_short = ext_meta.get('LicenseShortName', {}).get('value', '')
    artist = ext_meta.get('Artist', {}).get('value', '')
    artist_clean = re.sub(r'<[^>]+>', '', artist).strip()
    
    print(f"Title: {filename}")
    print(f"License: {license_short}")
    print(f"Artist: {artist_clean}")
    print(f"Full URL: {ii.get('url', '')}")
    print(f"Thumb URL: {ii.get('thumburl', '')}")
    print(f"Description URL: {ext_meta.get('CommonsName', {}).get('value', '')}")
    print(f"Credit: {ext_meta.get('Credit', {}).get('value', '')}")

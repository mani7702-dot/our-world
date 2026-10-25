import urllib.request, urllib.parse, json, time, re, html

url = 'https://commons.wikimedia.org/w/api.php'

# Search for Clusia images - simple search
params = urllib.parse.urlencode({
    'action': 'query',
    'format': 'json',
    'list': 'search',
    'srsearch': 'Clusia plant leaves',
    'srnamespace': '6',
    'srlimit': '10',
})
req = urllib.request.Request(url + '?' + params, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
resp = urllib.request.urlopen(req, timeout=30)
data = json.loads(resp.read().decode('utf-8'))

search_results = data.get('query', {}).get('search', [])
print(f"Found {len(search_results)} search results")

# Get image info for each
for item in search_results[:8]:
    title = item['title']
    # Get full image info
    info_params = urllib.parse.urlencode({
        'action': 'query',
        'format': 'json',
        'prop': 'imageinfo',
        'iiprop': 'url|mime|extmetadata',
        'titles': title,
    })
    info_req = urllib.request.Request(url + '?' + info_params, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
    time.sleep(1.5)
    info_resp = urllib.request.urlopen(info_req, timeout=30)
    info_data = json.loads(info_resp.read().decode('utf-8'))
    pages = info_data.get('query', {}).get('pages', {})
    for pid, page in pages.items():
        ii = page.get('imageinfo', [{}])[0] if page.get('imageinfo') else {}
        url_full = ii.get('url', '')
        mime = ii.get('mime', '')
        ext_meta = ii.get('extmetadata', {})
        lic = ext_meta.get('LicenseShortName', {}).get('value', '')
        artist = ext_meta.get('Artist', {}).get('value', '')
        artist_clean = re.sub(r'<[^>]+>', '', artist).strip()
        
        # Check license
        lic_ok = "public domain" in lic.lower() or "cc0" in lic.lower() or "cc by" in lic.lower()
        no_restrictions = "no restrictions" in lic.lower()
        
        print(f"\n  Title: {title}")
        print(f"  License: {lic} | OK={lic_ok} | no_restrictions={no_restrictions}")
        print(f"  MIME: {mime}")
        print(f"  Artist: {artist_clean[:100]}")
        print(f"  URL: {url_full}")
        if lic_ok and 'jpeg' in mime:
            print("  *** CANDIDATE FOUND ***")

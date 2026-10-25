import urllib.request, urllib.parse, json, re, time

def search_commons(keywords, limit=8):
    search_term = ' '.join(keywords)
    url = 'https://commons.wikimedia.org/w/api.php'
    params = urllib.parse.urlencode({
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': search_term + ' filetype:bitmap has:thumb',
        'srnamespace': '6',
        'srlimit': limit,
    })
    req = urllib.request.Request(url + '?' + params, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read().decode('utf-8'))
    
    results = []
    for item in data.get('query', {}).get('search', []):
        title = item['title']
        info_params = urllib.parse.urlencode({
            'action': 'query',
            'format': 'json',
            'prop': 'imageinfo',
            'iiprop': 'url|extmetadata',
            'titles': title,
        })
        info_req = urllib.request.Request(url + '?' + info_params, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
        time.sleep(1.5)
        info_resp = urllib.request.urlopen(info_req, timeout=30)
        info_data = json.loads(info_resp.read().decode('utf-8'))
        pages = info_data.get('query', {}).get('pages', {})
        for page_id, page in pages.items():
            ii = page.get('imageinfo', [{}])[0] if page.get('imageinfo') else {}
            thumb_url = ii.get('thumburl', '') or ii.get('url', '')
            if not thumb_url:
                fname = title.replace('File:', '').replace(' ', '_')
                thumb_url = f'https://upload.wikimedia.org/wikipedia/commons/thumb/' + fname[:1] + '/' + fname[:2] + '/' + fname + '/200px-' + fname
            
            ext_meta = ii.get('extmetadata', {})
            license_short = ext_meta.get('LicenseShortName', {}).get('value', '')
            artist = ext_meta.get('Artist', {}).get('value', '')
            artist_clean = re.sub(r'<[^>]+>', '', artist).strip()
            
            # Get the full image URL
            full_url = ii.get('url', '')
            
            mime = ii.get('mime', '')
            
            results.append({
                'title': title,
                'thumb': thumb_url,
                'full_url': full_url,
                'license': license_short,
                'artist': artist_clean,
                'mime': mime,
            })
    return results

queries = [
    ["Clusia", "plant", "tropical", "tree", "leaves"],
    ["Clusia", "plant", "leaves", "Costa Rica"],
    ["Clusia rosea", "plant", "red", "leaves"],
    ["CAM", "photosynthesis", "plant", "leaves"],
    ["tropical plant", "rainforest", "green", "leaves"],
]

for i, q in enumerate(queries):
    print(f"\n=== Query {i+1}: {q} ===")
    try:
        results = search_commons(q, limit=8)
        for j, r in enumerate(results[:5]):
            lic_ok = "public domain" in r['license'].lower() or "cc0" in r['license'].lower() or "cc by" in r['license'].lower()
            print(f"  {j+1}. {r['title']} | License: {r['license']} | OK={lic_ok} | MIME={r['mime']}")
            print(f"     Artist: {r['artist'][:80]}")
            print(f"     Full URL: {r['full_url']}")
            print(f"     Thumb: {r['thumb']}")
    except Exception as e:
        print(f"  ERROR: {e}")
    time.sleep(2)

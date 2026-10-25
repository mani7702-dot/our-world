#!/usr/bin/env python3
"""Manual Wikimedia Commons fallback query helper.
Searches Commons for images matching keywords and returns top results with license info.
"""
import urllib.request, urllib.parse, json, re, sys

def search_commons(keywords, limit=10):
    """Search Wikimedia Commons for files matching keywords."""
    search_term = ' '.join(keywords)
    url = 'https://commons.wikimedia.org/w/api.php'
    params = urllib.parse.urlencode({
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': search_term + ' filetype:bitmap has:thumb',
        'srnamespace': '6',  # File namespace
        'srlimit': limit,
    })
    req = urllib.request.Request(url + '?' + params, headers={'User-Agent': 'OurWorldSite/1.0'})
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read().decode('utf-8'))
    
    results = []
    for item in data.get('query', {}).get('search', []):
        title = item['title']
        # Get image info including license
        info_params = urllib.parse.urlencode({
            'action': 'query',
            'format': 'json',
            'prop': 'imageinfo',
            'iiprop': 'url|extmetadata',
            'titles': title,
        })
        info_req = urllib.request.Request(url + '?' + info_params, headers={'User-Agent': 'OurWorldSite/1.0'})
        info_resp = urllib.request.urlopen(info_req, timeout=30)
        info_data = json.loads(info_resp.read().decode('utf-8'))
        pages = info_data.get('query', {}).get('pages', {})
        for page_id, page in pages.items():
            ii = page.get('imageinfo', [{}])[0] if page.get('imageinfo') else {}
            thumb_url = ii.get('thumburl', '')
            if not thumb_url:
                # try to construct from filename
                fname = title.replace('File:', '').replace(' ', '_')
                thumb_url = f'https://upload.wikimedia.org/wikipedia/commons/thumb/' + fname[:1] + '/' + fname[:2] + '/' + fname + '/200px-' + fname
            
            # Get license info
            ext_meta = ii.get('extmetadata', {})
            license_short = ext_meta.get('LicenseShortName', {}).get('value', '')
            artist = ext_meta.get('Artist', {}).get('value', '')
            # Clean HTML from artist
            artist_clean = re.sub(r'<[^>]+>', '', artist).strip()
            
            results.append({
                'title': title,
                'thumb': thumb_url,
                'license': license_short,
                'artist': artist_clean,
                'license_url': ext_meta.get('LicenseUrl', {}).get('value', ''),
            })
    return results

if __name__ == '__main__':
    keywords = sys.argv[2:] if len(sys.argv) > 2 else ['walrus', 'Pacific', 'calf']
    slug = sys.argv[1] if len(sys.argv) > 1 else 'test'
    results = search_commons(keywords)
    for i, r in enumerate(results):
        print(f"{i+1}. {r['title']}")
        print(f"   License: {r['license']}")
        print(f"   Artist: {r['artist'][:100]}")
        print(f"   Thumb: {r['thumb']}")
        print()

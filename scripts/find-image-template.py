#!/usr/bin/env python3
"""Custom multi-query Wikimedia Commons search with progressive broadening.
- Browser UA for API calls and downloads
- time.sleep between calls to avoid 429
- No filetype:bitmap has:thumb modifier (too restrictive)
- Accepts 'cc by', 'cc by-sa', 'public domain', 'cc0', 'no restrictions'
"""
import urllib.request
import urllib.parse
import json
import re
import time
import sys
import os

BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

def api_get(params):
    """Make a GET request to Commons API with browser UA."""
    url = COMMONS_API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": BROWSER_UA})
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode('utf-8'))

def ok_license(license_short, license_url=""):
    """Check if license is acceptable for educational site."""
    lic = (license_short + " " + license_url).lower()
    # Accept: public domain, cc0, cc by, cc by-sa, no restrictions
    if "no restrictions" in lic:
        return True, "no restrictions"
    if "public domain" in lic:
        return True, "public domain"
    if "cc0" in lic:
        return True, "CC0"
    if "cc by" in lic:
        return True, "CC BY-SA" if "sa" in lic else "CC BY"
    return False, lic

def search_and_download(keywords, slug, max_queries=4):
    """Search Commons with progressive broadening, return best image info."""
    keyword_sets = [
        keywords.split(),
        keywords.split()[:4],
        keywords.split()[:3],
        keywords.split()[:2],
    ]
    
    found = []
    for i, kw in enumerate(keyword_sets[:max_queries]):
        search_term = ' '.join(kw)
        print(f"  Query {i+1}: '{search_term}'", file=sys.stderr)
        
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': search_term,
            'srnamespace': '6',
            'srlimit': 10,
        }
        
        try:
            data = api_get(params)
        except Exception as e:
            print(f"    API error: {e}", file=sys.stderr)
            time.sleep(2)
            continue
        
        time.sleep(1.5)  # avoid 429
        
        results = data.get('query', {}).get('search', [])
        if not results:
            print(f"    No results", file=sys.stderr)
            continue
        
        for item in results[:5]:
            title = item['title']
            info_params = {
                'action': 'query',
                'format': 'json',
                'prop': 'imageinfo',
                'iiprop': 'url|extmetadata',
                'titles': title,
            }
            try:
                info_data = api_get(info_params)
            except Exception as e:
                print(f"    Info error: {e}", file=sys.stderr)
                time.sleep(1.5)
                continue
            
            time.sleep(1.5)
            
            pages = info_data.get('query', {}).get('pages', {})
            for page_id, page in pages.items():
                ii = page.get('imageinfo', [{}])[0] if page.get('imageinfo') else {}
                if not ii:
                    continue
                thumb_url = ii.get('thumburl', '')
                if not thumb_url:
                    thumb_url = ii.get('url', '')
                    if not thumb_url:
                        # construct from title
                        fname = title.replace('File:', '').replace(' ', '_')
                        thumb_url = f'https://upload.wikimedia.org/wikipedia/commons/thumb/' + fname[:1] + '/' + fname[:2] + '/' + fname + '/200px-' + fname
                
                ext_meta = ii.get('extmetadata', {})
                license_short = ext_meta.get('LicenseShortName', {}).get('value', '')
                artist = ext_meta.get('Artist', {}).get('value', '')
                license_url = ext_meta.get('LicenseUrl', {}).get('value', '')
                
                accepted, final_lic = ok_license(license_short, license_url)
                if not accepted:
                    continue
                
                # Clean artist HTML
                artist_clean = re.sub(r'<[^>]+>', '', artist).strip()
                # Extract just a clean name
                artist_clean = re.sub(r'\]\(.*', '', artist_clean).replace('[', '').strip()
                if not artist_clean:
                    artist_clean = "Wikimedia Commons contributor"
                
                # Build caption
                if "public domain" in final_lic or "no restrictions" in final_lic:
                    caption = f"Photo: {artist_clean} / Public domain / Wikimedia Commons"
                elif "cc0" in final_lic:
                    caption = f"Photo: {artist_clean} / CC0 / Wikimedia Commons"
                elif "cc by-sa" in final_lic:
                    caption = f"Photo: {artist_clean} / CC BY-SA / Wikimedia Commons"
                elif "cc by" in final_lic:
                    caption = f"Photo: {artist_clean} / CC BY / Wikimedia Commons"
                else:
                    caption = f"Photo: {artist_clean} / Wikimedia Commons"
                
                found.append({
                    'title': title,
                    'thumb_url': thumb_url,
                    'license': final_lic,
                    'artist': artist_clean,
                    'caption': caption,
                    'url': thumb_url,
                })
                print(f"    Found: {title} ({final_lic})", file=sys.stderr)
        
        if found:
            return found[0], True
    
    return None, False

def download_image(url, dest):
    """Download image to dest with browser UA."""
    req = urllib.request.Request(url, headers={"User-Agent": BROWSER_UA})
    resp = urllib.request.urlopen(req, timeout=30)
    data = resp.read()
    with open(dest, 'wb') as f:
        f.write(data)
    print(f"  Downloaded: {dest} ({len(data)} bytes)", file=sys.stderr)
    return True

if __name__ == '__main__':
    slug = sys.argv[1] if len(sys.argv) > 1 else 'test'
    keywords = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else 'nairobi kenya shop business'
    
    print(f"Searching Commons for: {keywords}", file=sys.stderr)
    
    result, found = search_and_download(keywords, slug)
    
    if found:
        print(f"IMAGE_FOUND")
        print(f"title={result['title']}")
        print(f"url={result['url']}")
        print(f"caption={result['caption']}")
        print(f"license={result['license']}")
    else:
        print("NO_IMAGE_FOUND")

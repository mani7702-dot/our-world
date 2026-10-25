#!/usr/bin/env python3
import urllib.request, re, html, sys

url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.goodnewsnetwork.org/rescuers-ensure-orphaned-baby-walrus-gets-a-second-chance-look/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
try:
    resp = urllib.request.urlopen(req, timeout=30)
    content = resp.read().decode('utf-8', errors='replace')
    # Find td-post-content div and capture until matching closing div
    m = re.search(r'<div[^>]*class="td-post-content"[^>]*>(.*?)</div>\s*</div>\s*</div>', content, re.DOTALL)
    if m:
        body = m.group(1)
    else:
        # fallback: find the entry content div
        m = re.search(r'<div[^>]*class="entry-content[^"]*"[^>]*>(.*?)</div>\s*</div>', content, re.DOTALL)
        if m:
            body = m.group(1)
        else:
            body = content[:5000]  # last resort
    body = re.sub(r'<[^>]+>', ' ', body)
    body = html.unescape(body)
    body = re.sub(r'\s+', ' ', body).strip()
    print(body)
except Exception as e:
    print(f'Error: {e}')

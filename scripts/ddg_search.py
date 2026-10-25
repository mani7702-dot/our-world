#!/usr/bin/env python3
"""Search DuckDuckGo HTML and extract results."""
import urllib.request, re, sys, urllib.parse

query = sys.argv[1] if len(sys.argv) > 1 else 'Annautaq walrus SeaWorld Orlando rescue'
url = f'https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
resp = urllib.request.urlopen(req, timeout=30)
content = resp.read().decode('utf-8', errors='replace')
results = re.findall(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', content, re.DOTALL)
snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', content, re.DOTALL)
for i, (link, title) in enumerate(results[:10]):
    title = re.sub(r'<[^>]+>', '', title).strip()
    snip = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ''
    print(f'{i+1}. {title}')
    print(f'   URL: {link}')
    print(f'   {snip[:200]}')
    print()

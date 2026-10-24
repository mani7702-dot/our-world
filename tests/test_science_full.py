import urllib.request
import re

# Fetch ScienceDaily top articles to find new trending ones
url = 'https://www.sciencedaily.com/rss/top.xml'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = resp.read().decode('utf-8', errors='replace')
    root = __import__('xml.etree.ElementTree', fromlist=['ET']).fromstring(data)
    items = root.findall('.//item')
    print(f'Total items: {len(items)}')
    for it in items[:30]:
        t = it.findtext('title') or ''
        link = it.findtext('link') or ''
        desc = (it.findtext('description') or '')[:300]
        # Parse guid for date
        guid = it.findtext('guid') or ''
        pub = it.findtext('pubDate') or ''
        print(f'TITLE: {t}')
        print(f'URL: {link}')
        print(f'PUB: {pub}')
        print(f'DESC: {desc}')
        print('---')

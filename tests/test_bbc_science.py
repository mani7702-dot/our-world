import urllib.request
import xml.etree.ElementTree as ET

# BBC Science & Environment
url = 'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = resp.read().decode('utf-8', errors='replace')
    root = ET.fromstring(data)
    items = root.findall('.//item')
    print(f'Total items: {len(items)}')
    for it in items[:25]:
        t = it.findtext('title') or ''
        link = it.findtext('link') or ''
        desc = (it.findtext('description') or '')[:250]
        print(f'TITLE: {t}')
        print(f'URL: {link}')
        print(f'DESC: {desc}')
        print('---')

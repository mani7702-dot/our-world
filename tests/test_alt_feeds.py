import urllib.request
import xml.etree.ElementTree as ET

# Try different RSS feed URLs
urls = [
    'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
    'https://www.sciencedaily.com/rss/top.xml',
    'https://science.nasa.gov/rss/api/?mediaAssetPage=true',
    'https://www.universetoday.com/feed/',
    'https://phys.org/rss/earth-sciences/',
    'https://www.eurekalert.org/rss/news',
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode('utf-8', errors='replace')
            print(f'{url}: {len(data)} bytes')
            try:
                root = ET.fromstring(data)
                items = root.findall('.//item')
                print(f'  Items: {len(items)}')
                for it in items[:3]:
                    t = it.findtext('title') or ''
                    print(f'  - {t[:120]}')
            except ET.ParseError:
                print(f'  (not valid RSS/XML)')
            print('---')
    except Exception as e:
        print(f'{url}: ERROR - {e}')
        print('---')

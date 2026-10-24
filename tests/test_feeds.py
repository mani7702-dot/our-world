import urllib.request
import ssl

urls = [
    'https://old.reddit.com/r/todayilearned/top/.rss',
    'https://www.npr.org/rss/rss.jsf?id=1001',
]
for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read().decode('utf-8', errors='replace')
            print(f'{url}: {len(data)} bytes')
            print(data[:500])
            print('---')
    except Exception as e:
        print(f'{url}: ERROR - {e}')

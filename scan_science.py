import urllib.request, re

# Check ScienceDaily top.xml for animal stories
req = urllib.request.Request('https://www.sciencedaily.com/rss/top.xml',
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
try:
    raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8','ignore')
    raw = re.sub(r'<!--.*-->', '', raw, flags=re.S)
    items = re.findall(r'<item>(.*?)</item>', raw, re.S)
    print(f'Total ScienceDaily top.xml items: {len(items)}')
    for i, item in enumerate(items[:60]):
        title = re.search(r'<title>(.*?)</title>', item, re.S)
        link = re.search(r'<link>(.*?)</link>', item, re.S)
        if title and link:
            t = title.group(1).strip()
            l = link.group(1).strip()
            print(f'{i}: {t[:90]} | {l[:90]}')
except Exception as e:
    print(f'Error: {e}')

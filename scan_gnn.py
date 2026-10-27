import urllib.request, re

req = urllib.request.Request('https://www.goodnewsnetwork.org/feed/',
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8','ignore')
items = re.findall(r'<item>(.*?)</item>', raw, re.S)
print(f'Total GNN items: {len(items)}')
for i, item in enumerate(items[:40]):
    title = re.search(r'<title>(.*?)</title>', item, re.S)
    link = re.search(r'<link>(.*?)</link>', item, re.S)
    if title and link:
        t = title.group(1).strip()
        l = link.group(1).strip()
        print(f'{i}: {t[:90]} | {l[:90]}')

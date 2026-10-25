import urllib.request, re, html

ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
req = urllib.request.Request('https://www.goodnewsnetwork.org/feed/', headers={'User-Agent': ua})
raw = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', errors='replace')
items = re.findall(r'<item>(.*?)</item>', raw, re.DOTALL)
print(f'Total items: {len(items)}')
for i, item in enumerate(items[:15]):
    t = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
    l = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
    d = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
    if t:
        title = html.unescape(t.group(1).strip())
        link = html.unescape(l.group(1).strip()) if l else ''
        desc = d.group(1) if d else ''
        desc_clean = re.sub(r'<[^>]+>', '', desc)
        desc_clean = html.unescape(desc_clean).strip()[:220]
        print(f'{i}: {title}')
        print(f'   url: {link}')
        print(f'   desc: {desc_clean}')
        print()

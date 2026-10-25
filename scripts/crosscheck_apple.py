import urllib.request, re, html

ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'

# Cross-check: Lost Apple Project Wikipedia + apple heritage Wikipedia
urls = [
    'https://en.wikipedia.org/wiki/Apple',
    'https://en.wikipedia.org/wiki/Lost_Apple_Project',
]

for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': ua})
    raw = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', errors='replace')
    # Get the main content paragraphs
    content = re.sub(r'<script.*?</script>', '', raw, flags=re.DOTALL)
    content = re.sub(r'<style.*?</style>', '', content, flags=re.DOTALL)
    paras = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    print(f'\n=== {url} ===')
    print(f'Paragraphs found: {len(paras)}')
    for i, p in enumerate(paras[:10]):
        clean = re.sub(r'<[^>]+>', '', p)
        clean = html.unescape(clean).strip()
        if len(clean) > 40:
            print(f'  P{i}: {clean[:300]}')
    print()

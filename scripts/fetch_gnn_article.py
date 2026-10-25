import urllib.request, re, html

ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'

urls = [
    'https://www.goodnewsnetwork.org/major-supermarket-begins-wide-scale-tests-to-bring-heritage-apple-varieties-to-market/',
    'https://www.goodnewsnetwork.org/a-towering-figure-of-tolerance-from-2500-years-ago-has-found-a-new-home-in-atlanta/',
]

for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': ua})
    raw = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', errors='replace')
    # Extract article body from <article> tag
    article_match = re.search(r'<article[^>]*>(.*?)</article>', raw, re.DOTALL)
    body = article_match.group(1) if article_match else raw
    # Pull paragraphs
    paras = re.findall(r'<p[^>]*>(.*?)</p>', body, re.DOTALL)
    print(f'\n=== {url} ===')
    print(f'Paragraphs found: {len(paras)}')
    for i, p in enumerate(paras[:15]):
        clean = re.sub(r'<[^>]+>', '', p)
        clean = html.unescape(clean).strip()
        if len(clean) > 40:
            print(f'  P{i}: {clean[:300]}')
    print()

import urllib.request

urls = [
    'https://news.mongabay.com/short-article/2026/10/rare-bird-finding-strengthens-case-to-protect/',
    'https://news.mongabay.com/2026/10/bangladeshs-hornbills-face-hunting-risk-during/',
]

for url in urls:
    print(f"\n{'='*60}\n{url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        resp = urllib.request.urlopen(req, timeout=25).read().decode('utf-8','ignore')
        # extract article body
        import re
        # try to find article content
        article = re.search(r'<article[^>]*>(.*?)</article>', resp, re.S)
        if article:
            text = article.group(1)
        else:
            text = resp[:5000]
        # strip HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(text[:2000])
    except Exception as e:
        print(f"Error: {e}")

import urllib.request, re

# Try the Congo rainforest bird story with correct URL
urls = [
    'https://news.mongabay.com/2026/10/rare-bird-finding-strengthens-case-to-protect-congo-rainforest-across-borders/',
    'https://news.mongabay.com/short-article/2026/10/can-a-swamp-stop-an-army/',
    'https://news.mongabay.com/2026/10/nearly-all-the-worlds-coral-reefs-are-at-risk-of-collapse-within-50-years-iucn/',
]

for url in urls:
    print(f"\n{'='*60}\n{url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        resp = urllib.request.urlopen(req, timeout=25).read().decode('utf-8','ignore')
        article = re.search(r'<article[^>]*>(.*?)</article>', resp, re.S)
        text = article.group(1) if article else resp[:5000]
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(text[:1500])
    except Exception as e:
        print(f"Error: {e}")

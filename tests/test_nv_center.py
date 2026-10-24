import urllib.request
import re

# Check Wikipedia for nitrogen-vacancy center (spin defect in diamond)
url = 'https://en.wikipedia.org/wiki/Nitrogen-vacancy_center'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        print(f"Wikipedia NV center: {len(text)} chars")
        # Find relevant content
        idx = text.find('Nitrogen-vacancy')
        if idx > 0:
            print(text[idx:idx+2000])
except Exception as e:
    print(f"Error: {e}")

# Also check silicon carbide Wikipedia for context
url2 = 'https://en.wikipedia.org/wiki/Silicon_carbide'
try:
    req = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        print(f"\n\nWikipedia Silicon carbide: {len(text)} chars")
        idx = text.find('Silicon carbide')
        if idx > 0:
            print(text[idx:idx+1500])
except Exception as e:
    print(f"Error: {e}")

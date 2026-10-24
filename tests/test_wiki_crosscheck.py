import urllib.request
import re

# Cross-check with Wikipedia for basic quantum defect concepts
url = 'https://en.wikipedia.org/wiki/Quantum_dots'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        print(f"Wikipedia Quantum dots: {len(text)} chars")
        print(text[:500])
        print("---")
except Exception as e:
    print(f"Error: {e}")

# Also check spin defect Wikipedia
url2 = 'https://en.wikipedia.org/wiki/Spin_defect'
try:
    req = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        print(f"\nWikipedia Spin defect: {len(text)} chars")
        print(text[:500])
        print("---")
except Exception as e:
    print(f"Error: {e}")

# Check Physical Review Letters for the article
url3 = 'https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.123.123101'
try:
    req = urllib.request.Request(url3, headers={'User-Agent': 'Mozilla/5.0 (compatible; OurWorldBot/1.0)'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        print(f"\nPhysical Review Letters: {len(text)} chars")
        print(text[:1000])
except Exception as e:
    print(f"Error: {e}")

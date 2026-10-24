import urllib.request
import re

# Cross-check with EurekAlert or another source
# Let's search for "MIT muscle robot biohybrid" on various sources

# Try MIT News
urls = [
    'https://news.mit.edu/2026/robot-swimming-muscle-cells-1023',
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            text = re.sub(r'<[^>]+>', ' ', html)
            text = re.sub(r'\s+', ' ', text)
            print(f"=== {url} ({len(text)} chars) ===")
            # Find relevant section
            idx = text.find('robot')
            if idx > 0:
                print(text[max(0,idx-100):idx+2000])
            else:
                print(text[:1500])
            print("\n---\n")
    except Exception as e:
        print(f"{url}: ERROR - {e}")
        print("---")

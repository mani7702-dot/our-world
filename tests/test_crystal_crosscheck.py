import urllib.request
import re
import xml.etree.ElementTree as ET

# Cross-check source 1: ScienceDaily article
url1 = 'https://www.sciencedaily.com/releases/2026/10/261022081302.htm'
req = urllib.request.Request(url1, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
with urllib.request.urlopen(req, timeout=20) as resp:
    html = resp.read().decode('utf-8', errors='replace')
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Find the full story
    idx = text.find('FULL STORY')
    print("=== SOURCE 1: ScienceDaily ===")
    print(text[idx:idx+5000])

# Cross-check source 2: Look for University of Chicago press release
print("\n\n=== Looking for University of Chicago source ===")
url2 = 'https://www.uchicagomedicine.org/forefront/research-directions/quantum-defects-crystal-internal-conversion'
try:
    req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req2, timeout=15) as resp:
        html2 = resp.read().decode('utf-8', errors='replace')
        text2 = re.sub(r'<[^>]+>', ' ', html2)
        text2 = re.sub(r'\s+', ' ', text2)
        print(f"Found: {len(text2)} chars")
        print(text2[:2000])
except Exception as e:
    print(f"UChicago page error: {e}")

# Try Nature/Physical Review Letters abstract
print("\n\n=== Trying Physical Review Letters ===")
# The journal is Physical Review Letters

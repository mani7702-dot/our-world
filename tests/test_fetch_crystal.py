import urllib.request
import re

# Cross-check with the ScienceDaily article about crystal defect
url = 'https://www.sciencedaily.com/releases/2026/10/261022081302.htm'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
with urllib.request.urlopen(req, timeout=20) as resp:
    html = resp.read().decode('utf-8', errors='replace')
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    idx = text.find('FULL STORY')
    if idx > 0:
        print(text[idx:idx+3000])
    else:
        print(text[:3000])

import urllib.request
import re

# Try searching for MIT muscle robot on other sources
# Let's try the ScienceDaily article directly and also look for MIT.edu mentions

# First, let's get more of the ScienceDaily article
url = 'https://www.sciencedaily.com/releases/2026/10/261022081308.htm'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
with urllib.request.urlopen(req, timeout=20) as resp:
    html = resp.read().decode('utf-8', errors='replace')
    
# Extract full text
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text)

# Get the full story section
idx = text.find('FULL STORY')
if idx > 0:
    print(text[idx:idx+4000])
else:
    idx = text.find('A swimming robot')
    if idx > 0:
        print(text[idx:idx+4000])
    else:
        print(text[:4000])

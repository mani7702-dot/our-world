import urllib.request
import re

# Fetch MIT robot article from ScienceDaily
url1 = 'https://www.sciencedaily.com/releases/2026/10/261022081308.htm'

req = urllib.request.Request(url1, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
with urllib.request.urlopen(req, timeout=20) as resp:
    html = resp.read().decode('utf-8', errors='replace')
    
# Extract text content
# Remove scripts and styles
html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
# Get the main content
# Try to find article content
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)
# Find the relevant section
idx = text.find('MIT engineers')
if idx == -1:
    idx = text.find('tiny robot')
if idx == -1:
    idx = text.find('muscle cell')
if idx >= 0:
    print("=== MIT Robot Article ===")
    print(text[max(0,idx-200):idx+3000])
else:
    print("Full text (first 3000 chars):")
    print(text[:3000])

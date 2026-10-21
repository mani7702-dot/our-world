import re, sys
from html.parser import HTMLParser

with open(sys.argv[1], "r", encoding="utf-8", errors="replace") as f:
    html = f.read()

# Remove script and style tags
html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

# Find the article body
# NASA pages often have <article> or <div class="node__content"> or <p> tags in the main body

# Try to find the main article content
article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
body = article_match.group(1) if article_match else html

# Extract text from <p> tags
paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', body, re.DOTALL | re.IGNORECASE)
print(f"Found {len(paragraphs)} paragraphs in article body")
print()

for i, p in enumerate(paragraphs[:30]):
    # Clean HTML tags
    text = re.sub(r'<[^>]+>', '', p)
    # Unescape entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    text = text.replace('\n', ' ').strip()
    if len(text) > 20:  # Skip short paragraphs
        print(f"P{i+1}: {text[:300]}")
        print()
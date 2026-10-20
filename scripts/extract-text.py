"""Extract text content from an HTML article file."""
import sys
import re

html_path = sys.argv[1]
with open(html_path, errors='replace') as f:
    html = f.read()

# Extract title
title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
title = title_match.group(1).strip() if title_match else 'N/A'
print('TITLE:', title)

# Strip HTML tags
text = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text)
text = text.strip()

# Print full text
print('FULL TEXT:')
print(text[:5000])

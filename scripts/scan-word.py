"""Scan a file for altermagnetism mentions."""
import re
import sys

path = sys.argv[1]
with open(path, 'r', errors='replace') as f:
    h = f.read()
text = re.sub(r'<script[^>]*>.*?</script>', ' ', h, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<[^>]+>', ' ', text)
text = ' '.join(text.split())
idx = text.lower().find('altermagnet')
if idx >= 0:
    print(text[max(0,idx-200):idx+800])
else:
    print("NO altermagnetism mention. First 500 chars:")
    print(text[:500])

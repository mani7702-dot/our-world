#!/usr/bin/env python3
"""Extract main text from NASA tracks blog post."""
import re, sys
html = open(sys.argv[1]).read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text)
idx = text.find('Written by Vandi Verma')
print(text[idx:idx+3500])

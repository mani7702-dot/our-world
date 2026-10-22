#!/usr/bin/env python3
with open('/tmp/nasa_cyclone.html') as f:
    content = f.read()
# Find the actual article body paragraphs
import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_body = False
        self.texts = []
        self.skip = False
        
    def handle_starttag(self, tag, attrs):
        if tag in ('p', 'h1', 'h2', 'h3', 'li', 'div'):
            self.skip = False
            
    def handle_data(self, data):
        data = data.strip()
        if len(data) > 10:
            self.texts.append(data)

# Extract text between body content markers
# Find image of the day section
idx = content.find('Oct 21, 2026')
if idx > 0:
    body = content[idx:idx+5000]
    # clean HTML
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'\s+', ' ', body)
    print(body[:3000])

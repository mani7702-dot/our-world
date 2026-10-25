#!/usr/bin/env python3
import urllib.request, re, html, sys

url = 'https://www.goodnewsnetwork.org/rescuers-ensure-orphaned-baby-walrus-gets-a-second-chance-look/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
resp = urllib.request.urlopen(req, timeout=30)
content = resp.read().decode('utf-8', errors='replace')

# Find td-post-content div - balance divs to get full content
start = content.find('class="td-post-content"')
if start == -1:
    start = content.find('class="entry-content"')
if start != -1:
    # Find the opening div tag
    div_start = content.rfind('<div', 0, start)
    # Now balance open/close divs
    depth = 0
    i = div_start
    end_pos = len(content)
    while i < len(content) and i < end_pos:
        open_tag = content.find('<div', i)
        close_tag = content.find('</div>', i)
        if close_tag == -1:
            break
        if open_tag != -1 and open_tag < close_tag:
            depth += 1
            i = open_tag + 5  # skip past '<div'
        else:
            if depth == 0:
                end_pos = close_tag + 6
                break
            depth -= 1
            i = close_tag + 6
    body_html = content[div_start:end_pos]
else:
    body_html = content

body = re.sub(r'<[^>]+>', ' ', body_html)
body = html.unescape(body)
body = re.sub(r'\s+', ' ', body).strip()
print(body)

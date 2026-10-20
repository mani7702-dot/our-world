#!/usr/bin/env python3
"""Try fetching the MDPI paper with browser-like headers."""
import subprocess, re

# More browser-like UA
browsers = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]
urls = [
    'https://www.mdpi.com/2075-5391/12/3/30',
    'https://www.mdpi.com/2075-5391/12/3/30/html',
    'https://www.mdpi.com/2075-5391/12/3/30/htm',
]
for u in urls:
    r = subprocess.run(['curl', '-s', '--compressed', '--max-time', '25', '-A', browsers[0], '-L', '-H', 'Accept: text/html', u],
                       capture_output=True, text=True)
    title = re.search(r'<title>(.*?)</title>', r.stdout, re.I | re.S)
    t = title.group(1).strip()[:100] if title else "???"
    has_abstract = 'abstract' in r.stdout.lower()
    print(f'{u} -> {t} ({len(r.stdout)} bytes) abstract={has_abstract}')
    if has_abstract:
        text = re.sub(r'<[^>]+>', ' ', r.stdout)
        text = re.sub(r'\s+', ' ', text).strip()
        idx = text.lower().find('abstract')
        print(f'  ABSTRACT: {text[idx:idx+800]}')

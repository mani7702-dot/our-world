#!/usr/bin/env python3
"""Search for the original paper using ar5iv (arxiv HTML mirror) and crossref."""
import subprocess, re, json

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

# Try ar5iv for various possible arxiv IDs
ar5iv_urls = [
    'https://ar5iv.org/abs/arxiv:2409.15076',
    'https://ar5iv.org/abs/arxiv:2410.12345',
    'https://ar5iv.org/abs/arxiv:2410.15076',
    'https://ar5iv.org/abs/arxiv:2409.15077',
    'https://ar5iv.org/abs/arxiv:2409.15078',
]
for u in ar5iv_urls:
    r = subprocess.run(['curl', '-s', '--compressed', '--max-time', '15', '-A', UA, '-L', u],
                       capture_output=True, text=True)
    title = re.search(r'<title>(.*?)</title>', r.stdout, re.I|re.S)
    print(f'{u} -> {title.group(1).strip()[:80] if title else "???"} ({len(r.stdout)} bytes)')

# Try crossref API for the paper
print("\n=== Crossref search ===")
r = subprocess.run(['curl', '-s', '--compressed', '--max-time', '20', '-A', UA,
                    'https://api.crossref.org/works?query.bibliographic=mrk+501+binary+supermassive+black+hole+jet+orbit'],
                   capture_output=True, text=True)
try:
    data = json.loads(r.stdout)
    items = data.get('message', {}).get('items', [])
    print(f"Found {len(items)} results")
    for item in items[:5]:
        title = item.get('title', [''])[0][:100]
        doi = item.get('DOI', '')
        pub = item.get('container-title', [''])
        print(f"  TITLE: {title}")
        print(f"  DOI: {doi}")
        print(f"  PUB: {pub}")
        print()
except Exception as e:
    print(f"Parse error: {e}")

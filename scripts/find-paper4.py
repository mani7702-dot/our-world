#!/usr/bin/env python3
"""Search for the 2026 paper on Mrk 501 binary black hole jets via crossref."""
import subprocess, json

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

# Search crossref for the specific paper
url = 'https://api.crossref.org/works?query.bibliographic=Mrk+501+jet+binary+black+hole+orbit+2026&rows=10'
r = subprocess.run(['curl', '-s', '--compressed', '--max-time', '25', '-A', UA, url],
                   capture_output=True, text=True)
try:
    data = json.loads(r.stdout)
    items = data.get('message', {}).get('items', [])
    print(f"Found {len(items)} results")
    for item in items:
        title = item.get('title', [''])[0][:120]
        doi = item.get('DOI', '')
        pub = item.get('container-title', [''])
        year = item.get('published-print', {}).get('date-parts', [['']])
        print(f"  TITLE: {title}")
        print(f"  DOI: {doi}")
        print(f"  PUB: {pub}")
        if year:
            print(f"  YEAR: {year[0][0] if year[0] else ''}")
        print()
except Exception as e:
    print(f"Parse error: {e}")
    print(r.stdout[:500])

#!/usr/bin/env python3
"""Search for the specific 2026 paper on Mrk 501 - use author + journal + year."""
import subprocess, json

UA = "Mozilla/5.0 (OurWorld picker; contact anddugulamani722@gmail.com)"

# Search more specifically
url = 'https://api.crossref.org/works?query.bibliographic=Mrk+501+binary+black+hole+jet+orbit+candidates&rows=10&sort=published&order=desc'
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
        year = item.get('published', {}).get('date-parts', [['']])
        ystr = year[0][0] if year and year[0] else ''
        print(f"  [{ystr}] {title}")
        print(f"  DOI: {doi}")
        print(f"  PUB: {pub[0] if pub else ''}")
        # Print authors
        authors = [a.get('family','') for a in item.get('author',[])]
        print(f"  AUTHORS: {', '.join(authors[:5])}")
        print()
except Exception as e:
    print(f"Parse error: {e}")

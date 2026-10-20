#!/usr/bin/env python3
"""Search for the actual 2026 paper on Mrk 501 binary black hole - likely a 2025/2026 follow-up."""
import subprocess, json

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

# Search crossref specifically for 2026 papers on Mrk 501 + black hole
url = 'https://api.crossref.org/works?query.bibliographic=Mrk+501+supermassive+black+hole+binary+jet+chandra&filter=from-pub-date:2025&rows=15&sort=published&order=desc'
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
        print()
except Exception as e:
    print(f"Parse error: {e}")
    print(r.stdout[:500])

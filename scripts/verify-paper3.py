#!/usr/bin/env python3
"""Search for a press release or author page confirming the Mrk 501 binary BH discovery."""
import subprocess, re, json

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

# Search for press release
urls = [
    # Max Planck Institute for Radio Astronomy English press releases
    'https://www.mpifr.de/en/',
    'https://www.mpifr.de/en/news/2026.html',
    # Try the specific paper on ADS via DOI
    'https://ui.adsabs.harvard.edu/abs/2024Galax...12....30B/abstract',
    # Try semantic scholar
    'https://api.semanticscholar.org/graph/v1/paper/DOI:10.3390/galaxies12030030?fields=title,abstract,year,external_ids,authors',
]
for u in urls:
    headers = '-H' 'Accept: text/html'
    r = subprocess.run(['curl', '-s', '--compressed', '--max-time', '20', '-A', UA, '-L', u],
                       capture_output=True, text=True)
    title = re.search(r'<title>(.*?)</title>', r.stdout, re.I | re.S)
    t = title.group(1).strip()[:100] if title else "???"
    print(f'{u} -> {t} ({len(r.stdout)} bytes)')
    if '200' in r.stdout[:200] and len(r.stdout) > 1000:
        text = re.sub(r'<[^>]+>', ' ', r.stdout)
        text = re.sub(r'\s+', ' ', text).strip()
        # Look for Mrk 501 / binary
        idx = text.lower().find('mrk 501')
        if idx < 0:
            idx = text.lower().find('binary black')
        if idx > 0:
            print(f'  CONTEXT: ...{text[idx:idx+400]}...')

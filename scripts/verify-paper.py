#!/usr/bin/env python3
"""Verify the paper DOI and extract abstract from MDPI using ar5iv."""
import subprocess, re

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

# Try ar5iv with the DOI
urls = [
    'https://ar5iv.org/abs/doi:10.3390/galaxies12030030',
    'https://ar5iv.org/abs/10.3390/galaxies12030030',
    'https://ar5iv.org/abs/doi.org/10.3390/galaxies12030030',
]
for u in urls:
    r = subprocess.run(['curl', '-s', '--compressed', '--max-time', '25', '-A', UA, '-L', u],
                       capture_output=True, text=True)
    title = re.search(r'<title>(.*?)</title>', r.stdout, re.I|re.S)
    t = title.group(1).strip()[:100] if title else "???"
    # Check for abstract content
    has_abstract = 'abstract' in r.stdout.lower()
    has_britzen = 'britzen' in r.stdout.lower()
    print(f'{u} -> {t} ({len(r.stdout)} bytes) abstract={has_abstract} britzen={has_britzen}')
    if 'abstract' in r.stdout.lower() or 'binary' in r.stdout.lower():
        # Extract text
        text = re.sub(r'<[^>]+>', ' ', r.stdout)
        text = re.sub(r'\s+', ' ', text).strip()
        idx = text.lower().find('abstract')
        if idx > 0:
            print(f'  ABSTRACT: {text[idx:idx+600]}')

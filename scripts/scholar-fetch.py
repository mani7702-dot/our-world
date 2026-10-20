#!/usr/bin/env python3
"""Fetch Semantic Scholar info for the paper - fixed fields."""
import subprocess, json

UA = "Mozilla/5.0 (OurWorld picker; contact anddugulamani722@gmail.com)"
url = 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.3390/galaxies12030030?fields=title,abstract,year,authors,venue'
r = subprocess.run(['curl', '-s', '--compressed', '--max-time', '25', '-A', UA, '-L', url],
                   capture_output=True, text=True)
try:
    data = json.loads(r.stdout)
    print(f"Title: {data.get('title', '???')}")
    print(f"Year: {data.get('year', '???')}")
    print(f"Venue: {data.get('venue', '???')}")
    authors = data.get('authors', [])
    print(f"Authors: {', '.join(a.get('name','') for a in authors)}")
    print(f"\nAbstract: {data.get('abstract', 'N/A')[:1000]}")
except Exception as e:
    print(f"Error: {e}")
    print(r.stdout[:500])

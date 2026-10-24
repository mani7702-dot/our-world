#!/usr/bin/env python3
"""Cron-side space feed fetcher (Tirith-safe: no inline exec).
Fetches Universe Today + Space.com RSS, parses pubDates,
dedups against existing content/news + content/blog, applies kid-safe BLOCK filter."""
import urllib.request
import xml.etree.ElementTree as ET
import os
import re
from datetime import datetime, timezone

BASE = "/home/ubuntu/our-world"
EXISTING_DIRS = ["content/news", "content/blog"]

BLOCK = ("killing","death","dies","disease","cancer","therapy","surgery","implant",
         "virus","stroke","alzheimer","parkinson","clinical trial","court","lawsuit",
         "election","politic","terror","bomb","shooting","war","conflict","weapon",
         "crisis","disaster","fatal","killed","murder","dead","grave","funeral")

FEEDS = [
    ("UniverseToday", "https://www.universetoday.com/rss.xml"),
    ("SpaceCom", "https://www.space.com/feeds/rss"),
]

def existing_stems():
    stems = set()
    for d in EXISTING_DIRS:
        full = os.path.join(BASE, d)
        if os.path.isdir(full):
            for f in os.listdir(full):
                if f.endswith(".md"):
                    stems.add(f[:-3])
                    # also bare slug after date prefix
                    no_date = re.sub(r'^20\d{2}-\d{2}-\d{2}-', '', f[:-3])
                    stems.add(no_date)
    return stems

def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

def is_blocked(text):
    low = text.lower()
    for b in BLOCK:
        if b in low:
            return True
    return False

def parse_items(raw):
    items = []
    root = ET.fromstring(raw)
    # handle both Atom and RSS
    for it in root.findall('.//item'):
        title_el = it.find('title')
        link_el = it.find('link')
        pd_el = it.find('pubDate')
        desc_el = it.find('description')
        title = (title_el.text or '').strip() if title_el is not None else ''
        link = (link_el.text or '').strip() if link_el is not None else ''
        pubdate = (pd_el.text or '').strip() if pd_el is not None else ''
        desc = (desc_el.text or '').strip() if desc_el is not None else ''
        if not title or not link:
            continue
        # parse date
        dt = None
        for fmt in ('%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S %Z', '%a, %d %b %Y %H:%M:%S +0000', '%a, %d %b %Y %H:%M:%S GMT'):
            try:
                dt = datetime.strptime(pubdate, fmt)
                break
            except Exception:
                pass
        if not dt:
            try:
                dt = datetime.fromisoformat(pubdate.replace('Z','+00:00'))
            except Exception:
                dt = datetime(1970,1,1)
        if dt.tzinfo:
            dt = dt.astimezone()
        items.append({'feed':'?','title':title,'link':link,'pubdate':pubdate,'dt':dt,'desc':desc})
    # also handle Atom entries
    for it in root.iter('{http://www.w3.org/2005/Atom}entry'):
        title_el = it.find('{http://www.w3.org/2005/Atom}title')
        link_el = it.find('{http://www.w3.org/2005/Atom}link')
        pd_el = it.find('{http://www.w3.org/2005/Atom}updated') or it.find('{http://www.w3.org/2005/Atom}published')
        title = (title_el.text or '').strip() if title_el is not None else ''
        link = link_el.get('href','') if link_el is not None else ''
        pubdate = (pd_el.text or '').strip() if pd_el is not None else ''
        desc = ''
        if not title or not link:
            continue
        try:
            dt = datetime.fromisoformat(pubdate.replace('Z','+00:00'))
        except Exception:
            dt = datetime(1970,1,1)
        if dt.tzinfo:
            dt = dt.astimezone()
        items.append({'feed':'?','title':title,'link':link,'pubdate':pubdate,'dt':dt,'desc':desc})
    return items

def main():
    stems = existing_stems()
    all_items = []
    for name, url in FEEDS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (OurWorld cron; contact andugulamani722@gmail.com)"})
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = resp.read()
            if data[:2] == b'\x1f\x8b':
                import gzip; data = gzip.decompress(data)
            txt = data.decode('utf-8','replace')
            print(f"=== {name} ({len(txt)} bytes) ===")
            items = parse_items(txt)
            for it in items:
                it['feed'] = name
                all_items.append(it)
        except Exception as e:
            print(f"=== {name} ERROR: {e} ===")
    # sort newest first
    all_items.sort(key=lambda x: x['dt'], reverse=True)
    # dedup by link
    seen_links = set()
    print("\n--- CANDIDATES (newest first, kid-safe, unwritten) ---")
    printed = 0
    selected = None
    for it in all_items:
        if it['link'] in seen_links:
            continue
        seen_links.add(it['link'])
        full = it['title'] + ' ' + it['desc']
        if is_blocked(full):
            continue
        slug = slugify(it['title'])
        # check dedup against existing content
        if slug in stems:
            continue
        # also check the date-prefixed slug variant
        if slug.replace(' ','-') in ' '.join(stems):
            pass
        date_str = it['dt'].strftime('%Y-%m-%d')
        proposed_filename = f"{date_str}-{slug}"
        if proposed_filename in stems:
            continue
        printed += 1
        print(f"[{printed}] feed={it['feed']}")
        print(f"    title: {it['title']}")
        print(f"    pubDate: {it['pubdate']}")
        print(f"    link: {it['link']}")
        print(f"    slug: {slug}")
        print(f"    date_prefix: {date_str}")
        print(f"    proposed: {proposed_filename}")
        if printed == 1:
            selected = it
    if selected:
        print(f"\nSELECTED: {selected['title']}")
        # write a candidate file for downstream steps
        sel = {
            'title': selected['title'],
            'link': selected['link'],
            'pubDate': selected['pubdate'],
            'slug': slugify(selected['title']),
            'feed': selected['feed'],
            'dt': selected['dt'].strftime('%Y-%m-%d'),
        }
        import json
        with open(os.path.join(BASE, '_candidate_picked.json'),'w') as f:
            json.dump(sel, f, indent=2)
    else:
        print("\nNO PUBLISHABLE CANDIDATE")

if __name__ == "__main__":
    main()

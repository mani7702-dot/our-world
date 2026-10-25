#!/usr/bin/env python3
"""Deep space candidate finder - fetches more candidates and applies
full topic-level keyword dedup across ALL of content/news/.
Tirith-safe: standalone script file, no inline exec.
"""
import urllib.request
import xml.etree.ElementTree as ET
import os
import re
from datetime import datetime

BASE = "/home/ubuntu/our-world"
EXISTING_DIRS = ["content/news", "content/blog"]

BLOCK = ("killing","death","dies","disease","cancer","therapy","surgery","implant",
         "virus","stroke","alzheimer","parkinson","clinical trial","court","lawsuit",
         "election","politic","terror","bomb","shooting","war","conflict","weapon",
         "crisis","disaster","fatal","killed","murder","dead","grave","funeral",
         "podcast","strange new worlds","blade runner","halo","x-files","op-ed",
         "review","trailer","where did")

FEEDS = [
    ("UniverseToday", "https://www.universetoday.com/rss.xml"),
    ("SpaceCom", "https://www.space.com/feeds/rss"),
]

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

def fetch_feed(name, url):
    items = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (OurWorld cron; contact andugulamani722@gmail.com)"})
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = resp.read()
        if data[:2] == b'\x1f\x8b':
            import gzip; data = gzip.decompress(data)
        txt = data.decode('utf-8','replace')
        # Strip trailing HTML after </rss>
        idx = txt.rfind('</rss>')
        if idx > 0:
            txt = txt[:idx+6]
        root = ET.fromstring(txt)
        for it in root.findall('.//item'):
            title = (it.findtext('title') or '').strip()
            link = (it.findtext('link') or '').strip()
            pd = (it.findtext('pubDate') or '').strip()
            desc = (it.findtext('description') or '').strip()[:300]
            if not title or not link:
                continue
            try:
                dt = datetime.strptime(pd, '%a, %d %b %Y %H:%M:%S %z')
            except:
                try:
                    dt = datetime.fromisoformat(pd.replace('Z','+00:00'))
                except:
                    dt = datetime(1970, 1, 1)
            items.append({'feed':name, 'title':title, 'link':link, 'pubdate':pd, 'dt':dt, 'desc':desc})
    except Exception as e:
        print(f"=== {name} ERROR: {e} ===")
    return items

def check_topic_dedup(title):
    """Check if topic keywords (5+ core nouns from title) appear in any existing article.
    Returns True if DUPLICATE (already written), False if fresh."""
    # Extract core keywords from title (words with 5+ chars, excluding common stop words)
    stop = {'this','that','with','from','will','have','their','they','will','what','when','where','into','the','and','for','are','was','were','has','had','been','being','not','but','all','can','your','about','into','will','from','have','this','that','with','will','have','their','they','will','what','when','where','into','the','and','for','are','was','were','has','had','been','being','not','but','all','can','your','about'}
    words = re.findall(r'\b[a-zA-Z]{5,}\b', title.lower())
    keywords = [w for w in words if w not in stop]
    # Take top keywords (at least 3 core nouns)
    if not keywords:
        keywords = words[:3]
    else:
        keywords = keywords[:5]
    
    for d in EXISTING_DIRS:
        full = os.path.join(BASE, d)
        if not os.path.isdir(full):
            continue
        for f in os.listdir(full):
            if not f.endswith('.md'):
                continue
            try:
                content = open(os.path.join(full, f), encoding='utf-8', errors='ignore').read().lower()
                matches = sum(1 for kw in keywords if kw in content)
                if matches >= 3:  # 3+ core nouns matched = topic already covered
                    return True, f, keywords, matches
            except:
                continue
    return False, None, keywords, 0

def main():
    all_items = []
    for name, url in FEEDS:
        items = fetch_feed(name, url)
        all_items.extend(items)
        print(f"=== {name}: {len(items)} items fetched ===")

    # Sort newest first
    all_items.sort(key=lambda x: x['dt'], reverse=True)
    seen_links = set()
    
    print(f"\n--- DEEP CANDIDATE ANALYSIS ({len(all_items)} total) ---")
    printed = 0
    fresh_candidates = []
    
    for it in all_items:
        if it['link'] in seen_links:
            continue
        seen_links.add(it['link'])
        full = it['title'] + ' ' + it['desc']
        if is_blocked(full):
            verdict = "BLOCKED"
            continue
        
        slug = slugify(it['title'])
        date_str = it['dt'].strftime('%Y-%m-%d')
        proposed = f"{date_str}-{slug}"
        
        # Check slug-level dedup
        for d in EXISTING_DIRS:
            full_d = os.path.join(BASE, d)
            if os.path.isdir(full_d):
                for f in os.listdir(full_d):
                    if f.endswith('.md'):
                        stem = f[:-3]
                        no_date = re.sub(r'^20\d{2}-\d{2}-\d{2}-', '', stem)
                        if slug == stem or slug == no_date or proposed == stem:
                            # slug-level dup, but still check topic keywords
                            break
                    continue
        
        # Full topic-level dedup check
        is_dupe, dup_file, keywords, match_count = check_topic_dedup(it['title'])
        
        if is_dupe:
            verdict = f"DUPE (topic={keywords}, {match_count} matches in {dup_file})"
        else:
            verdict = "FRESH"
            printed += 1
            fresh_candidates.append(it)
        
        print(f"[{printed if verdict == 'FRESH' else '--'}] feed={it['feed']} {verdict}")
        print(f"    title: {it['title']}")
        print(f"    link: {it['link']}")
        print(f"    pubDate: {it['pubdate']}")
        print(f"    slug: {slug}")
        if verdict.startswith("DUPE"):
            print(f"    {verdict}")
        print()

    if fresh_candidates:
        print(f"\n=== FRESH CANDIDATES FOUND: {len(fresh_candidates)} ===")
        for i, c in enumerate(fresh_candidates[:10], 1):
            print(f"\n[{i}] {c['title']}")
            print(f"    link: {c['link']}")
            print(f"    feed: {c['feed']}")
            print(f"    pubDate: {c['pubdate']}")
            print(f"    slug: {slugify(c['title'])}")
    else:
        print("\n=== NO FRESH CANDIDATES — TOTAL SATURATION ===")

if __name__ == '__main__':
    main()

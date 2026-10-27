import urllib.request, re, os

# Collect all existing release IDs from content/
existing_rids = set()
for root, dirs, files in os.walk('content/'):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            try:
                text = open(path, encoding='utf-8').read()
                rids = re.findall(r'/releases/(\d+)/(\d+)/(\d+)\.htm', text)
                for r in rids:
                    existing_rids.add(r[2])  # the 12-digit ID
            except:
                pass

# Also collect existing slugs
existing_slugs = set()
for root, dirs, files in os.walk('content/'):
    for f in files:
        if f.endswith('.md'):
            existing_slugs.add(f[:-3])  # remove .md

print(f"Existing release IDs: {len(existing_rids)}")
print(f"Existing slugs: {len(existing_slugs)}")

# Check ScienceDaily plants_animals section
for feed_url, label in [
    ('https://www.sciencedaily.com/rss/earth_climate/plants_animals.xml', 'earth_climate/plants_animals'),
    ('https://news.mongabay.com/feed/', 'mongabay'),
]:
    print(f"\n=== {label} ===")
    try:
        req = urllib.request.Request(feed_url,
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8','ignore')
        raw = re.sub(r'<!--.*-->', '', raw, flags=re.S)
        items = re.findall(r'<item>(.*?)</item>', raw, re.S)
        print(f'Items: {len(items)}')
        for item in items[:40]:
            title = re.search(r'<title>(.*?)</title>', item, re.S)
            link = re.search(r'<link>(.*?)</link>', item, re.S)
            if title and link:
                t = title.group(1).strip()
                l = link.group(1).strip()
                # Check release ID
                rid_match = re.search(r'/releases/(\d+)/(\d+)/(\d+)\.htm', l)
                rid = rid_match.group(3) if rid_match else None
                published = rid in existing_rids if rid else False
                print(f'  {t[:80]} | published={published} | {l[:80]}')
    except Exception as e:
        print(f'Error fetching {label}: {e}')

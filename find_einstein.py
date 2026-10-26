import re, os, urllib.request, xml.etree.ElementTree as ET

# Get existing release IDs from content
existing = set()
for root_d, dirs, files in os.walk('content'):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root_d, f)
            with open(path, 'r', errors='replace') as fh:
                text = fh.read()
            ids = re.findall(r'/releases/(\d+)/(\d+)/(\d+)\.htm', text)
            for a, b, c in ids:
                existing.add(c)

print(f"Existing IDs: {len(existing)}")

# Fetch first astronomy feed
feed_url = 'https://www.sciencedaily.com/rss/space_time/astronomy.xml'
req = urllib.request.Request(feed_url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=30)
data = resp.read().decode('utf-8', errors='replace')
data = re.sub(r'<!--.*-->', '', data, flags=re.S)
print(f"Feed data length: {len(data)}")
root_elem = ET.fromstring(data)
channel = root_elem.find('channel')
items = channel.findall('item')
print(f"Total items: {len(items)}")

count = 0
for item in items:
    link_el = item.find('link')
    title_el = item.find('title')
    if link_el is not None and link_el.text:
        m = re.search(r'/releases/(\d+)/(\d+)/(\d+)\.htm', link_el.text)
        if m:
            rid = m.group(3)
            ttext = title_el.text if title_el is not None else ''
            if rid not in existing:
                count += 1
                print(f"  [{rid}] {ttext[:100]}")
                print(f"    URL: {link_el.text}")
                print()

print(f"\nFresh items: {count}")

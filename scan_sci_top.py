import re, os, xml.etree.ElementTree as ET

# Get existing release IDs from content
existing = set()
for root, dirs, files in os.walk('content'):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            with open(path, 'r', errors='replace') as fh:
                text = fh.read()
            ids = re.findall(r'/releases/(\d+)/(\d+)/(\d+)\.htm', text)
            for a, b, c in ids:
                existing.add(c)

# Also get existing titles/content for keyword-based dedup
existing_text = ""
for root, dirs, files in os.walk('content'):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            with open(path, 'r', errors='replace') as fh:
                existing_text += fh.read().lower() + "\n"

# Parse _sci_top.xml
tree = ET.parse('_sci_top.xml')
root_elem = tree.getroot()
channel = root_elem.find('channel')
if channel is None:
    channel = root_elem

items = channel.findall('item')
print(f'Total items in _sci_top.xml: {len(items)}')
print(f'Existing release IDs: {len(existing)}')
print()

# Medical/block keywords for kid-safety
MEDICAL_KW = ['cancer', 'tumor', 'alzheimer', 'dementia', 'aspirin', 'blood pressure',
              'heart disease', 'diabetes', 'covid', 'pandemic', 'depression', 'anxiety',
              'ptsd', 'parkinson', 'stroke', 'heart attack', 'cholesterol', 'obesity',
              'smoking', 'lung cancer', 'breast cancer', 'colon cancer', 'therapy',
              'treatment', 'clinical trial', 'drug', 'medication', 'risk', 'death',
              'mortality', 'mental health', 'suicide', 'brain shrinkage']

fresh = []
for item in items:
    link_el = item.find('link')
    if link_el is not None and link_el.text:
        m = re.search(r'/releases/(\d+)/(\d+)/(\d+)\.htm', link_el.text)
        if m:
            rid = m.group(3)
            title_el = item.find('title')
            ttext = title_el.text if title_el is not None else 'NO TITLE'
            if rid not in existing:
                # Check medical keywords
                is_medical = any(kw in ttext.lower() for kw in MEDICAL_KW)
                fresh.append((rid, ttext, link_el.text, is_medical))

print(f'Fresh (unpublished) items: {len(fresh)}')
print(f'Fresh non-medical: {len([f for f in fresh if not f[3]])}')
print()
for rid, title, url, is_medical in fresh:
    status = "MEDICAL" if is_medical else "OK"
    print(f'  [{status}] {rid}: {title[:90]}')
    print(f'    URL: {url}')

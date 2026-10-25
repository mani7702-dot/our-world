import re, html, subprocess, sys

data = open('/tmp/sd-top.xml', encoding='utf-8').read()
items = re.findall(r'<item>(.*?)</item>', data, re.DOTALL)

fresh_count = 0
for it in items:
    title = re.search(r'<title>(.*?)</title>', it, re.DOTALL)
    link = re.search(r'<link>(.*?)</link>', it, re.DOTALL)
    if not title or not link:
        continue
    t = html.unescape(title.group(1).strip())
    u = link.group(1).strip()
    
    # Skip medical topics
    skip_medical = any(kw in t.lower() for kw in [
        'cancer', 'alzheimer', 'brain health', 'brain damage', 'brain shrink',
        'dementia', 'arthritis', 'diabetes', 'blood pressure', 'heart',
        'ptsd', 'weight loss', 'weight-loss', 'fat burning', 'muscle pain',
        'statin', 'steroid', 'immune system', 'immune response', 'immune defense',
        'lung', 'breast', 'retatrutide', 'fish oil', 'omega-3', 'diet',
        'aging', 'carpal tunnel', 'hydrodissection', 'ultra-processed',
        'colorectal', 'blood', 'inflammatory', 'arthritis', 'rheumatoid',
        'supplement', 'vaccine', 'drug', 'treatment', 'clinical trial',
        'cell', 'protein', 'RNA', 'muscle', 'gut bacteria', 'microbiome',
    ])
    
    # Skip scary/disaster content
    skip_scary = any(kw in t.lower() for kw in [
        'chernobyl', 'nuclear', 'fallout', 'tsunami', 'disaster', 'landslide',
        'massive asteroid', 'exploding stars', 'volcano', 'hurricane',
        'storm', 'earthquake', 'fatal', 'deadly', 'dangerous', 'threat',
    ])
    
    if skip_medical or skip_scary:
        continue
    
    # Dedup check - grep topic keywords
    keywords = [' '.join(w for w in t.split() if len(w) > 3)[:80]]
    result = subprocess.run(['grep', '-rilE', re.escape(t.split(':')[0][:15]) if ':' in t else t[:20], 'content/news/'], capture_output=True, text=True)
    found = result.stdout.strip()
    
    print(f'FRESH? {"YES" if not found else "NO"}: {t}')
    if found:
        print(f'  MATCHED: {found.strip()[:80]}')
    fresh_count += 1

print(f"\nTotal non-medical/non-scary candidates: {fresh_count}")

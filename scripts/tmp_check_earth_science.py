import re, html, subprocess, sys

data = open('/home/ubuntu/our-world/sd-earth-science.xml', encoding='utf-8').read()
items = re.findall(r'<item>(.*?)</item>', data, re.DOTALL)

fresh = []
for it in items:
    title = re.search(r'<title>(.*?)</title>', it, re.DOTALL)
    link = re.search(r'<link>(.*?)</link>', it, re.DOTALL)
    desc = re.search(r'<description>(.*?)</description>', it, re.DOTALL)
    if not title or not link:
        continue
    t = html.unescape(title.group(1).strip())
    u = link.group(1).strip()
    d = html.unescape(desc.group(1).strip()[:200]) if desc else ''
    
    # Kid-safety: skip medical, scary, disaster
    t_lower = t.lower()
    skip = any(kw in t_lower for kw in [
        'cancer', 'alzheimer', 'brain health', 'brain damage', 'dementia',
        'arthritis', 'diabetes', 'blood pressure', 'heart ', 'ptsd',
        'weight loss', 'weight-loss', 'fat burning', 'muscle pain',
        'statin', 'steroid', 'immune system', 'immune response',
        'lung', 'breast', 'retatrutide', 'fish oil', 'omega-3',
        'ultra-processed', 'colorectal', 'inflammatory', 'rheumatoid',
        'supplement', 'vaccine', 'drug ', 'treatment', 'clinical trial',
        'chernobyl', 'nuclear', 'fallout', 'tsunami', 'disaster',
        'landslide', 'volcano', 'hurricane', 'storm', 'earthquake',
        'fatal', 'deadly', 'dangerous', 'threat', 'fire', 'smoke',
    ])
    if skip:
        print(f'  SKIP: {t}')
        continue
    
    # Check explainers lane keywords
    is_explainer = any(kw in t_lower for kw in ['how ', 'why ', 'what is', 'does ', 'can ', 'how do', 'how can'])
    
    # Dedup against all content/news/
    # Use a broad keyword from the title
    result = subprocess.run(['grep', '-ril', t[:25], 'content/news/'], capture_output=True, text=True)
    found = result.stdout.strip()
    
    if not found:
        fresh.append((t, u, d, is_explainer))
        print(f'  FRESH: {t} (explainer={is_explainer})')
    else:
        print(f'  DUP: {t} -> {found.strip()[:60]}')

print(f'\n=== {len(fresh)} fresh candidates ===')
for t, u, d, e in fresh:
    print(f'  [{"EXPLAINER" if e else "maybe"}] {t}')
    print(f'    URL: {u}')
    print(f'    DESC: {d}')
    print()

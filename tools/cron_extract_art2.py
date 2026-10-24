#!/usr/bin/env python3
"""Fetch Artemis article and extract main body text."""
import urllib.request, re

URL = "https://www.space.com/space-exploration/artemis/nasa-lays-out-plan-for-artemis-3-moon-lander-test-flight-but-when-will-it-launch"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
req = urllib.request.Request(URL, headers={"User-Agent": UA, "Accept":"text/html"})
with urllib.request.urlopen(req, timeout=30) as resp:
    html = resp.read().decode('utf-8','replace')
print(f"Fetched {len(html)} bytes")

# Try to isolate main article body sections
# Space.com article bodies often within <div class="...wysiwyg..."> or article tag
# Try several patterns
candidates = []
for pat in [r'<div[^>]*class="[^"]*article-body[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*wysiwyg[^"]*"[^>]*>(.*?)</div>',
            r'<article[^>]*>(.*?)</article>']:
    found = re.findall(pat, html, re.DOTALL|re.IGNORECASE)
    candidates.extend(found)
    if found:
        break

if not candidates:
    # fallback: grab all <p> with min length, skip nav
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL|re.IGNORECASE)
    out = []
    for p in paras:
        txt = re.sub(r'<[^>]+>','',p).strip()
        if len(txt) > 60 and not txt.lower().startswith(('sign','subscribe','get ','by submitting','contact','view','join','latest')):
            out.append(re.sub(r'\s+',' ',txt))
    print("\n".join(out[:40]))
else:
    body = candidates[0]
    paras = re.findall(r'<p[^>]*>(.*?)</p>', body, re.DOTALL|re.IGNORECASE)
    out = []
    for p in paras:
        txt = re.sub(r'<[^>]+>','',p).strip()
        if len(txt)>40:
            out.append(re.sub(r'\s+',' ',txt))
    print("\n--- MAIN BODY ---")
    print('\n'.join(out[:50]))

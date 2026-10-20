"""Extract headline article paragraphs from a saved BBC HTML file."""
import re, sys
path = sys.argv[1]
html = open(path, encoding="utf-8", errors="ignore").read()
mt = re.search(r'<title[^>]*>(.*?)</title>', html, re.S|re.I)
print("TITLE:", (mt.group(1).strip() if mt else "n/a"))
m = re.search(r'<article[^>]*>(.*?)</article>', html, re.S|re.I)
body = m.group(1) if m else html
body = re.sub(r'<script.*?</script>', '', body, flags=re.S|re.I)
body = re.sub(r'<style.*?</style>', '', body, flags=re.S|re.I)
paras = re.findall(r'<p[^>]*>(.*?)</p>', body, flags=re.S|re.I)
text = []
for p in paras:
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(clean) > 40:
        text.append(clean)
print("---", len(text), "paragraphs ---")
for t in text[:12]:
    print(t[:380])
    print()

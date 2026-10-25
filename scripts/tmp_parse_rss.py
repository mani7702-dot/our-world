import re, html, sys
data = open('/tmp/sd-top.xml', encoding='utf-8').read()
items = re.findall(r'<item>(.*?)</item>', data, re.DOTALL)
count = int(sys.argv[1]) if len(sys.argv) > 1 else 15
for it in items[:count]:
    title = re.search(r'<title>(.*?)</title>', it, re.DOTALL)
    link = re.search(r'<link>(.*?)</link>', it, re.DOTALL)
    desc = re.search(r'<description>(.*?)</description>', it, re.DOTALL)
    if title and link:
        t = html.unescape(title.group(1).strip())
        u = link.group(1).strip()
        d = html.unescape(desc.group(1).strip()[:200]) if desc else ''
        print('TITLE:', t)
        print('URL:', u)
        print('DESC:', d)
        print('---')

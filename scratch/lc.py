import os, re
root_base = os.getcwd()
issues = 0
for root, _, files in os.walk('.'):
    for f in files:
        if not f.endswith('.html') or 'templates/' in root:
            continue
        p = os.path.join(root, f)
        html = open(p, encoding='utf-8', errors='ignore').read()
        for m in re.finditer(r"<img[^>]+src=(\S+)", html):
            src = m.group(1).strip('\'"')
            if src.startswith(('data:', 'http', '//')):
                continue
            target = os.path.normpath(os.path.join(root_base, root, src))
            if not os.path.exists(target):
                print('BROKEN IMG:', p, '->', src)
                issues += 1
        for m in re.finditer(r'href=(\S+)', html):
            h = m.group(1).strip('\'"')
            if h in ('#', 'javascript:void(0)'):
                continue
            if h.startswith(('http', 'mailto:', '#')):
                continue
            if not h.endswith('.html'):
                continue
            target = os.path.normpath(os.path.join(root_base, root, h))
            if not os.path.exists(target):
                print('BROKEN LINK:', p, '->', h)
                issues += 1
print('link/img check done; issues:', issues)

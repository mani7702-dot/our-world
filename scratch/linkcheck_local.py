import os, re
os.chdir(r'C:/Users/uday/our-world')
issues = 0
for root, _, files in os.walk('.'):
    for f in files:
        if not f.endswith('.html') or 'templates/' in root:
            continue
        p = os.path.join(root, f)
        html = open(p, encoding='utf-8', errors='ignore').read()
        for m in re.finditer(r'<img[^>]+src=[' + q + r'"]([^ + q + r]+)[' + q + r'"]', html):
            src = os.path.normpath(m.group(1).replace('\\', '/'))
            if src.startswith(('data:', 'http', '//')):
                continue
            target = os.path.normpath(os.path.join(root, src))
            if not os.path.exists(target):
                print('BROKEN IMG:', p, '->', src)
                issues += 1
        for m in re.finditer(r'href=[' + q + r'"]([^ + q + r]+)[' + q + r'"]', html):
            h = os.path.normpath(m.group(1).replace('\\', '/'))
            if h in ('#', 'javascript:void(0)'):
                continue
            if h.startswith(('http', 'mailto:', '#')):
                continue
            target = os.path.normpath(os.path.join(root, h))
            if not h.endswith('.html'):
                continue
            if not os.path.exists(target):
                print('BROKEN LINK:', p, '->', h)
                issues += 1
print('link/img check done; issues:', issues)

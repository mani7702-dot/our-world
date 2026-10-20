import os, re
breaks = 0
for dp, _, fs in os.walk("."):
    if any(p in dp for p in ("/content", "/templates", "/tools", ".git", "__pycache__")):
        continue
    for f in fs:
        if not f.endswith(".html"):
            continue
        s = open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
        for m in re.findall(r'(?:href|src)="([^"]+)"', s):
            u = m.replace("\\", "/")
            if u.startswith(("http", "//", "data:", "#", "mailto:")) or "{{" in u:
                continue
            if not os.path.exists(os.path.normpath(os.path.join(dp, u))):
                print(f"{f}->{u}")
                breaks += 1
print("Broken links:", breaks)

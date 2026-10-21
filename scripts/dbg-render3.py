#!/usr/bin/env python3
import sys, os
sys.path.insert(0, "/home/ubuntu/our-world")
import build
news = build.load_posts("news")
p = next((x for x in news if x["slug"]=="history-solar-storm-train-delay-typo"), None)
fg = p.get("for-grown-ups","")
print("fg len:", len(fg))
print("fg bool:", bool(fg))
# exact replica of article_page lines 311-318
grownups = ""
if p.get("for-grown-ups"):
    grownups = (
        '<aside class="grownups" data-reveal>\n'
        "      <h2>For grown-ups</h2>\n"
        "      <p>%s</p>\n"
        "    </aside>"
    ) % build.esc(p["for-grown-ups"])
print("grownups len:", len(grownups))
print("grownups starts:", repr(grownups[:60]))
# Now the tokens dict + render, exactly like article_page
section = p["section"]; prefix = "../"
tokens = {
    "ZONE": build.ZONE[section],
    "GROWNUPS": grownups,
}
tpl = open(os.path.join(build.TPL_DIR,"article.html")).read()
# render exactly as build.render
t = tpl
for k,v in tokens.items():
    t = t.replace("{{"+k+"}}", v)
import re
leftover = re.findall(r"\{\{[A-Z_]+\}\}", t)
print("after replacing ONLY GROWNUPS+ZONE, leftover includes GROWNUPS?:", "{{GROWNUPS}}" in t, "count:", t.count("{{GROWNUPS}}"))
print("grownups in final t?:", "grownups" in t)

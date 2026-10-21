#!/usr/bin/env python3
import sys
sys.path.insert(0, "/home/ubuntu/our-world")
import build
text = open("/home/ubuntu/our-world/content/news/history-solar-storm-train-delay-typo.md").read()
p, body = build.parse_frontmatter(text)
p["slug"] = "history-solar-storm-train-delay-typo"
p["section"] = "news"
p["body_html"] = build.md_to_html(body)

# Reproduce article_page logic for grownups
grownups = ""
if p.get("for-grownups"):
    print("for-grown-ups IS truthy, len:", len(p["for-grown-ups"]))
    grownups = (
        '<aside class="grownups" data-reveal>\n'
        "      <h2>For grown-ups</h2>\n"
        "      <p>%s</p>\n"
        "    </aside>"
    ) % build.esc(p["for-grownups"])
    print("grownups html built, len:", len(grownups))
else:
    print("for-grown-ups is EMPTY/FALSE in article_page context")

# Check if esc() or % breaks
v = p["for-grown-ups"]
print("esc'd len:", len(build.esc(v)))
print("contains {{:", "{{" in v)
print("contains ---:", "---" in v)
# the actual aside line:
print("ASIDE LINE:", '<aside class="grownups"' in grownups)
# write a tiny test to see if token gets into the final render
tokens = {"GROWNUPS": grownups}
import os
tpl = open(os.path.join(build.TPL_DIR, "article.html")).read()
out = tpl.replace("{{GROWNUPS}}", grownups)
print("tpl has GROWNUPS token?:", "{{GROWNUPS}}" in tpl)
print("rendered has aside?:", "grownups" in out)
# leftover tokens?
import re
leftover = re.findall(r"\{\{[A-Z_]+\}\}", tpl.replace("{{GROWNUPS}}", grownups))
print("leftover tokens after manual replace:", leftover)

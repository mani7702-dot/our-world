#!/usr/bin/env python3
import sys, os
sys.path.insert(0, "/home/ubuntu/our-world")
import build
# Re-run ARTICLE_PAGE only on this post by calling build with fresh import
news = build.load_posts("news")
p = next(x for x in news if x["slug"]=="history-solar-storm-train-delay-typo")
# Manually replicate article_page's grownups + tokens + page() to find the failure
section = p["section"]; prefix = "../"
grownups = ""
if p.get("for-grown-ups"):
    grownups = ('<aside class="grownups" data-reveal>\n'
                "      <h2>For grown-ups</h2>\n"
                "      <p>%s</p>\n"
                "    </aside>") % build.esc(p["for-grownups"])
print("grownups len:", len(grownups), "has 'aside':", "aside" in grownups)
# Reproduce tokens (the ones used in page())
import json
p["body_html"] = build.md_to_html(build.parse_frontmatter(open(os.path.join(build.CONTENT_DIR,"news","history-solar-storm-train-delay-typo.md")).read())[1])
# Need post_image, etc. Just call page()
try:
    out = build.page("Test — Our World", p["excerpt"][:155], section, prefix, "article.html", {"GROWNUPS":grownups})
    print("page() ok, len:", len(out), "grownups in out:", "grownups" in out)
except SystemExit as e:
    print("SystemExit from render:", e)
    import traceback; traceback.print_exc()
except Exception as e:
    print("Exception:", e)
    import traceback; traceback.print_exc()

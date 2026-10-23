#!/usr/bin/env python3
"""Our World — static site builder.

Reads content/blog/*.md and content/news/*.md, renders them with templates/
into pages at the project root. Stdlib only.

Publish flow: drop a .md file into content/ -> run `python build.py` -> done.
"""
import html as html_mod
import json
import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL_DIR = os.path.join(ROOT, "templates")
CONTENT_DIR = os.path.join(ROOT, "content")

ZONE = {"blog": "#15803d", "news": "#1d4ed8"}
DRAFT = '<span class="badge-draft">Sample — phase 2</span>'


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def parse_frontmatter(text):
    """Returns (meta dict, body). Only simple `key: value` lines — no YAML needed."""
    meta, body = {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        body = m.group(2)
    return meta, body


def esc(s):
    return html_mod.escape(s, quote=False)


def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: '<a href="%s"%s>%s</a>'
        % (
            m.group(2),
            ' target="_blank" rel="noopener"' if m.group(2).startswith("http") else "",
            m.group(1),
        ),
        s,
    )
    return s


def md_to_html(md):
    """Small, honest markdown subset: headings, bold/italic, links, lists, quotes, hr, paragraphs."""
    lines = md.strip().split("\n")
    out, para = [], []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            flush()
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush()
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2).strip()), lvl))
            i += 1
            continue
        if line.strip() == "---":
            flush()
            out.append("<hr>")
            i += 1
            continue
        if re.match(r"^>\s?", line):
            flush()
            buf = []
            while i < len(lines) and re.match(r"^>\s?", lines[i]):
                t = re.sub(r"^>\s?", "", lines[i]).strip()
                if t:
                    buf.append(t)
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(buf)) + "</p></blockquote>")
            continue
        if re.match(r"^[-*]\s+", line):
            flush()
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                items.append(inline(re.sub(r"^[-*]\s+", "", lines[i]).strip()))
                i += 1
            out.append("<ul>" + "".join("<li>%s</li>" % x for x in items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", line):
            flush()
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(inline(re.sub(r"^\d+\.\s+", "", lines[i]).strip()))
                i += 1
            out.append("<ol>" + "".join("<li>%s</li>" % x for x in items) + "</ol>")
            continue
        para.append(line.strip())
        i += 1
    flush()
    return "\n".join(out)


def load_posts(section):
    d = os.path.join(CONTENT_DIR, section)
    posts = []
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"):
            continue
        meta, body = parse_frontmatter(read(os.path.join(d, fn)))
        meta["slug"] = fn[:-3]
        meta["section"] = section
        meta["body_html"] = md_to_html(body)
        meta["is_sample"] = meta.get("sample", "").lower() == "true"
        meta["tag_list"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
        try:
            meta["date_long"] = datetime.strptime(meta.get("date", ""), "%Y-%m-%d").strftime("%d %B %Y")
        except ValueError:
            meta["date_long"] = meta.get("date", "")
        meta["time"] = str(meta.get("time", "")).strip()
        meta.setdefault("title", meta["slug"])
        meta.setdefault("excerpt", "")
        meta.setdefault("category", section.capitalize())
        meta.setdefault("read", "2 min")
        posts.append(meta)
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    return posts


def nav_html(active, prefix):
    items = [
        ("Home", "index.html", "home"),
        ("Blog", "blog/index.html", "blog"),
        ("Games", "games/index.html", "games"),
        ("News", "news/index.html", "news"),
        ("Parents", "parents/index.html", "parents"),
        ("Privacy", "privacy/index.html", "privacy"),
        ("Terms", "terms/index.html", "terms"),
        ("Contact", "contact/index.html", "contact"),
        ("About", "about/index.html", "about"),
    ]
    parts = []
    for label, href, key in items:
        cur = ' aria-current="page"' if key == active else ""
        parts.append('<li><a href="%s%s"%s>%s</a></li>' % (prefix, href, cur, label))
    return "<ul>" + "".join(parts) + "</ul>"


def render(name, tokens):
    t = read(os.path.join(TPL_DIR, name))
    for k, v in tokens.items():
        t = t.replace("{{" + k + "}}", v)
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", t)
    if leftover:
        raise SystemExit("template %s has unfilled tokens: %s" % (name, leftover))
    return t


def page(title, desc, active, prefix, main_name, main_tokens, base_extra=None, canonical_path=None):
    """Render a generated page with canonical + og:url + og:image.

    canonical_path is the site-root-relative path of the page (e.g. "/blog/",
    "/blog/foo.html"). When omitted it is derived from `active`: "home" -> "/",
    otherwise "/<section>/".
    """
    base_extra = base_extra or {}
    if canonical_path is None:
        canonical_path = "/" if active == "home" else "/%s/" % active
    canon_url = SITE_BASE + canonical_path
    base_extra.setdefault("CANONICAL_TAG", canonical_tag(canon_url))
    base_extra.setdefault("OG_URL_TAG", '<meta property="og:url" content="%s">\n' % canon_url)
    # og:image must be an ABSOLUTE URL — social scrapers do not resolve relative paths.
    base_extra.setdefault("OG_IMAGE", "%s/assets/og-cover.png" % SITE_BASE)
    # AdSense header script tag — empty until ADSENSE_PUB_ID is configured.
    base_extra.setdefault("ADSENSE_TAG", build_adsense_tag() if ADSENSE_PUB_ID else "")
    tokens = {
        "TITLE": title,
        "DESC": desc,
        "PREFIX": prefix,
        "NAV": nav_html(active, prefix),
        "MAIN": render(main_name, main_tokens),
        "CANONICAL_TAG": base_extra.get("CANONICAL_TAG", ""),
        "OG_URL_TAG": base_extra.get("OG_URL_TAG", ""),
        "OG_IMAGE": base_extra.get("OG_IMAGE", "%s/assets/og-cover.png" % SITE_BASE),
        "JSONLD": base_extra.get("JSONLD", ""),
        "ADSENSE_TAG": base_extra.get("ADSENSE_TAG", build_adsense_tag() if ADSENSE_PUB_ID else ""),
    }
    return render("base.html", tokens)


def draft_badge(p):
    return DRAFT if p["is_sample"] else ""


def thumb(p, url, prefix):
    """Small article image, clickable through to the post."""
    if not p.get("image"):
        return ""
    return (
        '<a class="row-thumb" href="%s" tabindex="-1" aria-label="Open: %s">'
        '<img src="%s%s" alt="%s" loading="lazy" decoding="async" '
        'width="480" height="252"></a>'
    ) % (url, esc(p["title"]), prefix, p["image"], esc(p["title"]))


def today_card(p, label, prefix=""):
    return (
        '<div class="today-card" style="--zone:%s" data-reveal>\n'
        "      %s\n"
        '      <span class="kicker">%s · %s</span>\n'
        '      <h3><a href="%s/%s.html">%s</a></h3>\n'
        '      <p class="small muted">%s</p>\n'
        "      %s\n"
        "    </div>"
    ) % (
        ZONE[p["section"]],
        thumb(p, "%s/%s.html" % (p["section"], p["slug"]), prefix),
        label,
        esc(p["date_long"]),
        p["section"],
        p["slug"],
        esc(p["title"]),
        esc(p["excerpt"]),
        draft_badge(p),
    )


def blog_row(p, url, prefix=""):
    return (
        '<article class="article-row" data-reveal>\n'
        '      %s\n'
        "      <div>\n"
        '        <span class="kicker" style="--zone:%s;margin-bottom:8px">%s · %s · %s read</span>\n'
        '        <h3><a href="%s">%s</a></h3>\n'
        "        <p>%s</p>\n"
        "        %s\n"
        "      </div>\n"
        "    </article>"
    ) % (
        thumb(p, url, prefix),
        ZONE["blog"],
        esc(p["category"]),
        esc(p["date_long"]),
        esc(p["read"]),
        url,
        esc(p["title"]),
        esc(p["excerpt"]),
        draft_badge(p),
    )


def news_item(p, url, prefix=""):
    return (
        '<li class="news-item" data-reveal>\n'
        "      %s\n"
        '      <div>\n'
        '      <time datetime="%s">%s</time>\n'
        '      <a href="%s">%s</a>\n'
        "      <p>%s</p>\n"
        "      %s\n"
        "      </div>\n"
        "    </li>"
    ) % (
        thumb(p, url, prefix),
        esc(p.get("date", "")),
        esc(p["date_long"]),
        url,
        esc(p["title"]),
        esc(p["excerpt"]),
        draft_badge(p),
    )


def popular_strip(all_posts, limit=8, prefix=""):
    """Horizontal row of small image-title cards on the news index."""
    picks = [p for p in all_posts if p.get("image")][:limit]
    if not picks:
        return ""
    cards = []
    for p in picks:
        url = "%s%s/%s.html" % (prefix, p["section"], p["slug"])
        img = ('<img src="%s%s" alt="%s" loading="lazy" decoding="async" '
               'width="96" height="56" class="popular-thumb">') % (prefix, p["image"], esc(p["title"]))
        cards.append(
            '<a class="popular-card" href="%s" title="%s">%s<span>%s</span></a>'
            % (url, esc(p["title"]), img, esc(p["title"]))
        )
    return '<div class="popular-row">' + "".join(cards) + "</div>"

def article_page(p):
    section = p["section"]
    prefix = "../"
    meta_extra = ""
    if section == "blog":
        meta_extra = '<span class="reading-time">%s read</span>' % esc(p["read"])
    tag_list = ""
    if p["tag_list"]:
        tag_list = (
            '<ul class="tag-list">'
            + "".join(
                '<li class="tag"><a href="../search/?q=%s">%s</a></li>' % (esc(t), esc(t))
                for t in p["tag_list"]
            )
            + "</ul>"
        )
    grownups = ""
    if p.get("for-grownups"):
        grownups = (
            '<aside class="grownups" data-reveal>\n'
            "      <h2>For grown-ups</h2>\n"
            "      <p>%s</p>\n"
            "    </aside>"
        ) % esc(p["for-grownups"])
    sample_note = (
        '<p class="sample-note">Sample post — swap in your own copy whenever you are ready.</p>'
        if p["is_sample"]
        else ""
    )
    article_url = "%s/%s/%s.html" % (SITE_BASE, section, p["slug"])
    jsonld_script = (
        '<script type="application/ld+json">'
        + json.dumps({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": p["title"],
            "description": p["excerpt"],
            "datePublished": p.get("date", ""),
            "mainEntityOfPage": article_url,
            "publisher": {"@type": "Organization", "name": "Our World", "url": SITE_BASE},
            "author": {"@type": "Organization", "name": "Our World"},
            "inLanguage": "en",
        }, ensure_ascii=False)
        + "</script>"
    )
    post_image = ""
    if p.get("image"):
        cap = '<figcaption>%s</figcaption>' % esc(p["image_caption"]) if p.get("image_caption") else ""
        post_image = ('<figure class="post-figure">\n'
                      '  <img src="../%s" alt="%s" loading="lazy" width="1200" height="630">\n'
                      '  %s\n</figure>' % (p["image"], esc(p["title"]), cap))
        v = p.get("video", "")
        if v:
            post_image += ('<figure class="post-figure"><video class="post-video" controls preload="none" '
                           'poster="../%s"><source src="%s" type="video/webm">Your browser does not support video.</video></figure>'
                           % (p["image"], v))
    body_html = p["body_html"]
    def insert_fig(body, pth, frac):
        parts = body.split("</p>")
        if len(parts) < 3:
            return body
        at = max(1, int(len(parts) * frac))
        fig = ('<figure class="post-figure in-body">\n'
               '  <img src="../%s" alt="Photo" loading="lazy" width="1200" height="630">\n'
               '</figure>' % pth)
        parts.insert(at, fig)
        return "</p>".join(parts)
    if p.get("image2"):
        body_html = insert_fig(body_html, p["image2"], 0.38)
    if p.get("image3"):
        body_html = insert_fig(body_html, p["image3"], 0.72)
    tokens = {
        "ZONE": ZONE[section],
        "JSONLD": jsonld_script,
        "AUTHOR": "Our World",
        "TIME_PART": (" at %s IST" % p["time"]) if p.get("time") else "",
        "POST_IMAGE": post_image,
        "CATEGORY": esc(p["category"]),
        "TITLE": esc(p["title"]),
        "DATE": esc(p.get("date", "")),
        "DATE_LONG": esc(p["date_long"]),
        "META_EXTRA": meta_extra,
        "SAMPLE_NOTE": sample_note,
        "LEDE": esc(p["excerpt"]),
        "BODY": body_html,
        "TAG_LIST": tag_list,
        "GROWNUPS": grownups,
        "BACK_URL": "../%s/index.html" % section,
        "BACK_LABEL": "the blog" if section == "blog" else "the news",
    }
    title = "%s — Our World" % esc(p["title"])
    desc = p["excerpt"][:155]
    canon_url = "%s/%s/%s.html" % (SITE_BASE, section, p["slug"])
    out = page(title, desc, section, prefix, "article.html", tokens,
               base_extra={
                   "JSONLD": jsonld_script,
                   "CANONICAL_TAG": canonical_tag(canon_url),
                   "OG_URL_TAG": '<meta property="og:url" content="%s">\n' % canon_url,
               })
    write(os.path.join(ROOT, section, p["slug"] + ".html"), out)


def build_search_index(posts):
    """Client-side search data: a flat array, written to the site root.

    Keys are exactly what assets/js/search.js needs — title, url (root-relative),
    section, excerpt, tags. No HTML is stored, so the JSON stays plain text.
    """
    entries = []
    for p in posts:
        entries.append(
            {
                "title": p["title"],
                "url": "%s/%s.html" % (p["section"], p["slug"]),
                "section": p["section"],
                "excerpt": p.get("excerpt", ""),
                "tags": p.get("tag_list", []),
            }
        )
    return json.dumps(entries, ensure_ascii=False, indent=2) + "\n"


def search_page():
    """Renders search/index.html — the page that consumes search-index.json."""
    return page(
        "Search — Our World",
        "Search every story and news item on Our World by title, topic or tag. No accounts, no chat — searching happens in your own browser.",
        "blog",
        "../",
        "search.html",
        {},
        canonical_path="/search/",
    )


# Allow overriding the deployed domain via env so the same build can serve a custom domain:
#   SITE_BASE="https://ourworld.news" python build.py
SITE_BASE = os.environ.get("SITE_BASE", "https://mani7702-dot.github.io/our-world")

# AdSense publisher ID (leave empty until you have an approved account). When set, every
# page gets the AdSense <script> so revenue is "code-ready" at launch.
ADSENSE_PUB_ID = os.environ.get("ADSENSE_PUB_ID", "")


def build_adsense_tag():
    """Render the AdSense <script async data-ad-client> tag. Empty until a pub ID is set.

    The canonical AdSense header script is:
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
    With a publisher ID, add  data-ad-client="ca-pub-<ID>"  to enable auto-ads.
    Until you're approved, ADSENSE_PUB_ID stays empty and NO script is injected.
    """
    if not ADSENSE_PUB_ID:
        return ""
    return ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"'
            ' data-ad-client="ca-pub-{pub}"></script>').format(pub=ADSENSE_PUB_ID)


def build_adsense_slot(slot_id):
    """Render an AdSense ad <ins> slot. Returns empty until ADSENSE_PUB_ID is set.

    Drop into an article template as {{ADSENSE_SLOT}}; the page auto-hides it (display:none)
    when empty so layout is stable pre-approval.
    """
    if not ADSENSE_PUB_ID:
        return ""
    return ('<ins class="adsbygoogle" style="display:block;margin:2rem auto"'
            ' data-ad-client="ca-pub-{pub}" data-ad-slot="{slot}"'
            ' data-ad-format="auto" data-full-width-responsive="true"></ins>').format(
                pub=ADSENSE_PUB_ID, slot=slot_id)


def build_ads_txt():
    """Generate ads.txt at the site root. Empty/comment-only until a pub ID is set.

    Google will not suppress earnings on an empty ads.txt, but a valid line here is
    required once you go live with ads:
        google.com, ca-pub-<YOUR_ID>, DIRECT, f08c47fec0940fa3
    """
    if not ADSENSE_PUB_ID:
        return "# ads.txt placeholder — add your AdSense ca-pub line after approval.\n"
    return "google.com, ca-pub-{pub}, DIRECT, f08c47fec0940fa3\n".format(pub=ADSENSE_PUB_ID)


def build_adsense_slot(slot_id):
    """Render an ad <ins> slot. Caller styles placement. Empty until a pub ID is set."""
    if not ADSENSE_PUB_ID:
        return ""
    return '<ins class="adsbygoogle" data-ad-client="ca-pub-{pub}" data-ad-slot="{slot}"></ins>'.format(pub=ADSENSE_PUB_ID, slot=slot_id)


def canonical_tag(canonical_url):
    """<link rel=canonical> tag for a page. Empty when no URL supplied."""
    return '<link rel="canonical" href="%s">\n' % canonical_url if canonical_url else ""


def build_robots_txt():
    """Robots.txt with an absolute Sitemap URL."""
    return "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE_BASE


def build_sitemap(blog, news):
    """Sitemap over known static pages + every article, with absolute URLs."""
    static_entries = [
        "/",
        "/blog/",
        "/news/",
        "/games/",
        "/games/memory-match.html",
        "/games/math-quiz.html",
        "/games/draw-paint.html",
        "/games/bubble-pop.html",
        "/games/colour-echo.html",
        "/games/tic-tac-toe.html",
        "/games/number-slide.html",
        "/games/hungry-snake.html",
        "/parents/",
        "/about/",
        "/privacy/",
        "/terms/",
        "/contact/",
        "/search/",
    ]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for entry in static_entries:
        lines.append("  <url><loc>%s%s</loc></url>" % (SITE_BASE, entry))
    for p in blog + news:
        loc = "%s/%s/%s.html" % (SITE_BASE, p["section"], p["slug"])
        lastmod = p.get("date", "") or "2026-01-01"
        lines.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (loc, lastmod))
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def build_feed(blog, news):
    """Atom feed over the latest ~20 articles; feed.xml (RSS is expected by aggregators)."""
    items = sorted(blog + news, key=lambda p: p.get("date", ""), reverse=True)[:20]
    ent = []
    for p in items:
        loc = "%s/%s/%s.html" % (SITE_BASE, p["section"], p["slug"])
        ent.append(
            "  <entry><title>%s</title><link href=\"%s\"/><id>%s</id>"
            "<updated>%s</updated>%s</entry>"
            % (esc(p["title"]), loc, loc, p.get("date", "") or "2026-01-01",
               "<summary>%s</summary>" % esc(p.get("desc", "")) if p.get("desc") else "")
        )
    return (
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom"><title>Our World</title>'
        '<link href="%s/feed.xml" rel="self"/><id>%s/</id><updated>%s</updated>'
        % (SITE_BASE, SITE_BASE, (items[0].get("date", "") if items else "2026-01-01")),
        *ent,
        "</feed>",
        "",
    )


# Hand-authored pages (not produced by a template). They still need canonical/og tags,
# and those must follow SITE_BASE when the domain changes, so a build pass injects them.
STATIC_HTML = [
    "about/index.html",
    "contact/index.html",
    "parents/index.html",
    "privacy/index.html",
    "terms/index.html",
    "games/index.html",
    "games/memory-match.html",
    "games/math-quiz.html",
    "games/draw-paint.html",
    "games/bubble-pop.html",
    "games/colour-echo.html",
    "games/tic-tac-toe.html",
    "games/number-slide.html",
    "games/hungry-snake.html",
]

CANON_START = "<!-- ow:canonical -->"
CANON_END = "<!-- /ow:canonical -->"


def add_canonical_to_static_pages():
    """Inject canonical + og tags into hand-authored pages, idempotently.

    build.py generates the home page, section indexes and articles; the pages above are
    edited by hand. Without this pass they would silently lack canonical tags and would
    have to be hand-edited whenever the domain changes. The marked block is stripped and
    re-inserted on every build, so repeated runs converge instead of accumulating tags.
    """
    changed = []
    for rel in STATIC_HTML:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        html = read(path)
        if rel.endswith("index.html"):
            url = "%s/%s" % (SITE_BASE, rel[: -len("index.html")])
        else:
            url = "%s/%s" % (SITE_BASE, rel)
        block = "\n".join([
            CANON_START,
            canonical_tag(url).rstrip("\n"),
            '<meta property="og:url" content="%s">' % url,
            '<meta property="og:image" content="%s/assets/og-cover.png">' % SITE_BASE,
            CANON_END,
            "",
        ])
        # Drop any block from a previous run so this is safe to run repeatedly.
        html = re.sub(
            re.escape(CANON_START) + r".*?" + re.escape(CANON_END) + r"\n?",
            "", html, flags=re.S,
        )
        marker = '<link rel="icon"'
        if marker not in html:
            continue
        write(path, html.replace(marker, block + marker, 1))
        changed.append(rel)
    return changed


def main():
    blog = load_posts("blog")
    news = load_posts("news")
    written = []

    # robots.txt + sitemap.xml (root-relative; update the domain once chosen)
    write(os.path.join(ROOT, "robots.txt"), build_robots_txt())
    written.append("robots.txt")
    # ads.txt — required for AdSense; empty/comment-only until a pub ID is configured.
    write(os.path.join(ROOT, "ads.txt"), build_ads_txt())
    written.append("ads.txt")
    write(os.path.join(ROOT, "sitemap.xml"), build_sitemap(blog, news))
    written.append("sitemap.xml")
    write(os.path.join(ROOT, "feed.xml"), "\n".join(build_feed(blog, news)))
    written.append("feed.xml")

    # client-side search index (site root, fetched by search/index.html)
    write(os.path.join(ROOT, "search-index.json"), build_search_index(blog + news))
    written.append("search-index.json")

    # canonical/og tags for hand-authored pages (idempotent; follows SITE_BASE)
    written.extend(add_canonical_to_static_pages())

    # home
    home_tokens = {
        "TODAY_BLOG": today_card(blog[0], "Latest story") if blog else "",
        "TODAY_NEWS": today_card(news[0], "News headline") if news else "",
        "BLOG_ROWS": "\n".join(blog_row(p, "blog/%s.html" % p["slug"]) for p in blog[:2]),
        "NEWS_LIST": "\n".join(news_item(p, "news/%s.html" % p["slug"]) for p in news[:3]),
    }
    write(os.path.join(ROOT, "index.html"),
          page("Our World — stories, games and news for curious kids",
               "Our World is a safe place for young readers: short stories, three playful browser games, and kid-safe world news — free, and supported by ads. No accounts, no chat.",
               "home", "", "home.html", home_tokens))
    written.append("index.html")

    # section indexes
    for section, posts, tpl in (("blog", blog, "blog-index.html"), ("news", news, "news-index.html")):
        if section == "blog":
            listing = "\n".join(blog_row(p, "%s.html" % p["slug"], "../") for p in posts)
        else:
            listing = "\n".join(news_item(p, "%s.html" % p["slug"], "../") for p in posts)
        tokens = {
            "COUNT": str(len(posts)),
            "ROWS": listing,
            "LIST": listing,
            "POPULAR": popular_strip(blog + news, prefix="../") if section == "news" else "",
        }
        write(os.path.join(ROOT, section, "index.html"),
              page("%s — Our World" % section.capitalize(),
                   "Posts and news from Our World, written for young readers.",
                   section, "../", tpl, tokens))
        written.append("%s/index.html" % section)

    # articles
    for p in blog + news:
        article_page(p)
        written.append("%s/%s.html" % (p["section"], p["slug"]))

    # search page
    write(os.path.join(ROOT, "search", "index.html"), search_page())
    written.append("search/index.html")

    print("Built %d files:" % len(written))
    for w in written:
        print("  " + w)
    print("Blog posts: %d  |  News items: %d" % (len(blog), len(news)))


if __name__ == "__main__":
    main()

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


def page(title, desc, active, prefix, main_name, main_tokens, base_extra=None):
    tokens = {
        "TITLE": title,
        "DESC": desc,
        "JSONLD": (base_extra or {}).get("JSONLD", ""),
        "PREFIX": prefix,
        "NAV": nav_html(active, prefix),
        "MAIN": render(main_name, main_tokens),
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


def popular_strip(all_posts, limit=8):
    """Horizontal row of small image-title cards on the news index."""
    picks = [p for p in all_posts if p.get("image")][:limit]
    if not picks:
        return ""
    cards = []
    for p in picks:
        url = "%s/%s.html" % (p["section"], p["slug"])
        img = ('<img src="../%s" alt="%s" loading="lazy" decoding="async" '
               'width="96" height="56" class="popular-thumb">') % (p["image"], esc(p["title"]))
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
    out = page(title, desc, section, prefix, "article.html", tokens, base_extra={"JSONLD": jsonld_script})
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
    )


SITE_BASE = "https://mani7702-dot.github.io/our-world"


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


def main():
    blog = load_posts("blog")
    news = load_posts("news")
    written = []

    # robots.txt + sitemap.xml (root-relative; update the domain once chosen)
    write(os.path.join(ROOT, "robots.txt"), build_robots_txt())
    written.append("robots.txt")
    write(os.path.join(ROOT, "sitemap.xml"), build_sitemap(blog, news))
    written.append("sitemap.xml")
    write(os.path.join(ROOT, "feed.xml"), "\n".join(build_feed(blog, news)))
    written.append("feed.xml")

    # client-side search index (site root, fetched by search/index.html)
    write(os.path.join(ROOT, "search-index.json"), build_search_index(blog + news))
    written.append("search-index.json")

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
            "POPULAR": popular_strip(blog + news) if section == "news" else "",
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

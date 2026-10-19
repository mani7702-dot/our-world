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
        ("Blog", "blog/", "blog"),
        ("Games", "games/", "games"),
        ("News", "news/", "news"),
        ("Parents", "parents/", "parents"),
        ("About", "about/", "about"),
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


def page(title, desc, active, prefix, main_name, main_tokens):
    tokens = {
        "TITLE": title,
        "DESC": desc,
        "PREFIX": prefix,
        "NAV": nav_html(active, prefix),
        "MAIN": render(main_name, main_tokens),
    }
    return render("base.html", tokens)


def draft_badge(p):
    return DRAFT if p["is_sample"] else ""


def today_card(p, label):
    return (
        '<div class="today-card" style="--zone:%s" data-reveal>\n'
        '      <span class="kicker">%s</span>\n'
        '      <h3><a href="%s/%s.html">%s</a></h3>\n'
        '      <p class="small muted">%s</p>\n'
        "      %s\n"
        "    </div>"
    ) % (
        ZONE[p["section"]],
        label,
        p["section"],
        p["slug"],
        esc(p["title"]),
        esc(p["excerpt"]),
        draft_badge(p),
    )


def blog_row(p, url):
    return (
        '<article class="article-row" data-reveal>\n'
        "      <div>\n"
        '        <span class="kicker" style="--zone:%s;margin-bottom:8px">%s · %s read</span>\n'
        '        <h3><a href="%s">%s</a></h3>\n'
        "        <p>%s</p>\n"
        "      </div>\n"
        "      %s\n"
        "    </article>"
    ) % (
        ZONE["blog"],
        esc(p["category"]),
        esc(p["read"]),
        url,
        esc(p["title"]),
        esc(p["excerpt"]),
        draft_badge(p),
    )


def news_item(p, url):
    return (
        '<li class="news-item" data-reveal>\n'
        '      <time datetime="%s">%s</time>\n'
        '      <a href="%s">%s</a>\n'
        "      <p>%s</p>\n"
        "      %s\n"
        "    </li>"
    ) % (
        esc(p.get("date", "")),
        esc(p["date_long"]),
        url,
        esc(p["title"]),
        esc(p["excerpt"]),
        draft_badge(p),
    )


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
            + "".join('<li class="tag">%s</li>' % esc(t) for t in p["tag_list"])
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
    tokens = {
        "ZONE": ZONE[section],
        "CATEGORY": esc(p["category"]),
        "TITLE": esc(p["title"]),
        "DATE": esc(p.get("date", "")),
        "DATE_LONG": esc(p["date_long"]),
        "META_EXTRA": meta_extra,
        "SAMPLE_NOTE": sample_note,
        "LEDE": esc(p["excerpt"]),
        "BODY": p["body_html"],
        "TAG_LIST": tag_list,
        "GROWNUPS": grownups,
        "BACK_URL": "../%s/" % section,
        "BACK_LABEL": "the blog" if section == "blog" else "the news",
    }
    title = "%s — Our World" % esc(p["title"])
    desc = p["excerpt"][:155]
    out = page(title, desc, section, prefix, "article.html", tokens)
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
        "Search every story and news item on Our World by title, topic or tag. No ads, no trackers, no accounts.",
        "blog",
        "../",
        "search.html",
        {},
    )


def main():
    blog = load_posts("blog")
    news = load_posts("news")
    written = []

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
               "Our World is a safe place for young readers: short stories, three playful browser games, and kid-safe world news. No ads, no trackers, no accounts.",
               "home", "", "home.html", home_tokens))
    written.append("index.html")

    # section indexes
    for section, posts, tpl in (("blog", blog, "blog-index.html"), ("news", news, "news-index.html")):
        if section == "blog":
            listing = "\n".join(blog_row(p, "%s.html" % p["slug"]) for p in posts)
        else:
            listing = "\n".join(news_item(p, "%s.html" % p["slug"]) for p in posts)
        tokens = {"COUNT": str(len(posts)), "ROWS": listing, "LIST": listing}
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

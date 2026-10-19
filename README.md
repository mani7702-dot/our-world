# Our World — static site

A calm kids' site: blog, browser games, kid-safe news. **No backend, no database, no accounts.**

## How it works

- Pages are plain HTML + CSS + JS. Content lives in `content/` as Markdown files.
- `build.py` compiles the content into finished pages.
- `assets/` holds the design system, self-hosted fonts and JS.

## Publishing a post (2 steps)

1. Drop a file like this into `content/blog/` or `content/news/`:

```markdown
---
title: My post title
date: 2026-10-19
category: Science
read: 3 min
excerpt: One-sentence summary shown on lists and home page.
tags: science, space
sample: false
---

The article body in Markdown. ## Headings, **bold**, lists, > quotes all work.
```

2. Run:

```
python build.py
```

That regenerates `index.html`, `blog/`, `news/` and every article page. Upload the result and it's live.

Set `sample: false` on posts you want shown as final (the "Sample — phase 2" badge disappears).

## Reading comfort

Every article page has **A− / A+** (text size) and **Easy-read** (dyslexia-friendly spacing). Both are remembered per device in the browser — nothing is sent anywhere.

## Safety model

- No ads, no trackers, no analytics, no accounts, no chat.
- Fonts are self-hosted — no third party sees who reads the site.
- Game progress (when games land) stays in browser localStorage only.

## Deploy target

Cloudflare Pages (primary) + GitHub Pages (mirror). Push the built site to the repo; both hosts serve it free with automatic HTTPS.

## Local preview

Just open `index.html` in any browser. For a closer-to-live check:

```
python -m http.server 8137
# then open http://localhost:8137
```

# Our World — static site

A calm kids' site: blog, browser games, kid-safe news. **No backend, no database, no accounts.**

## How it works

- Pages are plain HTML + CSS + JS. Content lives in `content/` as Markdown files.
- `build.py` compiles the content into finished pages.
- `assets/` holds the design system, self-hosted fonts and JS.

## What's on the site

- **Ads** — Our World is free, supported by Google AdSense. No accounts, no chat, and your progress never leaves your device.
- **Blog** — explainers and reading guides for 7–11 year olds.
- **Games** — three browser games (Memory Match, Math Quiz, Draw & Paint). No installs, no accounts.
- **News** — short, kind news items with links to the original story.
- **Dark mode** — moon toggle in the header. It follows your device setting and remembers your choice.
- **Site search** — rolling out shortly; it works on the built site with no server.

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

- Ads keep the site free (Google AdSense). The ad network sees what it needs to serve ads — nothing here sells your data.
- No chat, no accounts, no sign-ups. Self-hosted fonts; the ad network is the only third party.
- Game progress stays in browser localStorage only. Never transmitted.
- The About page carries a contact form that stays dormant until a real form ID is set — nothing connects anywhere until then.

## After any change

Every page you touch (a post, a page, an asset) is stale until rebuilt. The loop is always the same: edit, then `python build.py`, then push. Never push unbuilt pages.

## Deploy target

Cloudflare Pages (primary) + GitHub Pages (mirror). Both serve the built site free with automatic HTTPS.
Step-by-step instructions are in **[DEPLOY.md](DEPLOY.md)**.

## Local preview

Just open `index.html` in any browser. For a closer-to-live check:

```
python -m http.server 8137
# then open http://localhost:8137
```

# Our World — Site Audit & Traffic-Building Report

**Site:** https://mani7702-dot.github.io/our-world/ (GitHub Pages, repo `mani7702-dot/our-world`)
**Author:** audited from the local repo at `C:\Users\uday\our-world` + the live site + the publishing VPS (`bots` @ 129.225.91.213).
**Date:** 2026-10-23. Live evidence is fresh as of this audit.
**TL;DR:** The site is **technically healthy and live**, but it is **invisible to Google** (zero-indexed), its **AdSense setup is fiction** (no ad code exists and the AdSense account is missing), and its **content pipeline, while running, is leaking posts** (the VPS is 39 commits and ~15 recent articles ahead of GitHub). Traffic will not appear until you fix **indexing + AdSense + the publishing gap**. The fixes are concrete; none require re-authoring the site.

---

## 0. Executive summary

| # | Finding | Severity | One-line fix |
|---|---------|----------|--------------|
| 1 | Site is live but **0% indexed / 0 traffic** | 🔴 Blocker | Add `ads.txt`, submit sitemap in Search Console, fix domain |
| 2 | **AdSense is not implemented.** README promises ads; no `ca-pub` / `adsbygoogle` exists. No AdSense account. | 🔴 Blocker | Set up AdSense account, get domain, install ad tags |
| 3 | **GitHub Pages free subdomain is not AdSense-eligible.** AdSense requires a domain you own. | 🔴 Blocker | Buy `ourworld.com`-style domain, point GitHub Pages to it |
| 4 | **VPS is 39 commits + ~15 articles ahead of GitHub.** Posts are being written and *not published*. | 🔴 High | Fix `ow-deploy.sh` / sync, or push the backlog now |
| 5 | **Images are 104 MB, unoptimized** (one hero = 3.7 MB). Site is slow; penalized by Google Images. | 🟠 High | Convert to WebP, resize to <=1200 px, add `loading=lazy` + `srcset` |
| 6 | **No canonical tags / no `og:url`.** Duplicate-content risk vs. the mirror host. | 🟠 Medium | Add `<link rel=canonical>` and `og:url` in `build.py` |
| 7 | **No Search Console property.** You cannot diagnose indexing without it. | 🟡 Medium | Add & verify the property, submit sitemap |
| 8 | **`content/news/science/`** stray folder = 1 duplicated article (build confusion). | 🟡 Low | Move out, rebuild |
| 9 | **6 articles still flagged `sample: true`** ("Sample — phase 2" badge live). | 🟡 Low | Set `sample: false`, rebuild |

**Bottom line:** you have a real, well-built site with a working 24/7 writer-bot pipeline, but **nothing is wired to Google** and **nothing is monetized**. Fix the three red blockers (indexing, domain+AdSense, and the VPS push gap) and the daily-cadence content engine compounds.

---

## 1. Live status & performance

- **GitHub Pages host** `https://mani7702-dot.github.io/our-world/` — **HTTP 200**, serves the real site: 248 HTML pages, 240-URL `sitemap.xml`, 185 news posts + 39 blog posts, 8 browser games.
- **DEPLOY.md's "Cloudflare Pages primary" was never created.** `https://our-world.pages.dev` resolves to a *different person's* Chinese bookmark site (`My Website Collection`). The "primary + GitHub mirror" split in DEPLOY.md does not match reality: **GitHub Pages is your only live host.**
- **`ourworld.com`** currently returns an unrelated Google-hosted JPEG (`our-world-retirement.jpg`). It is **not pointed at your site** and you do not control it — do not assume ownership.
- **Speed:** home page = 17.9 KB HTML in 0.55 s; but article hero images are 0.37–3.7 MB and take ~4 s to download. Mobile experience will be slow.
- **404:** a real `404.html` is served (good).
- **Broken internal links:** 0 found across 1,032 links checked → navigation is robust.
- **Site age:** first commit `2026-10-19`, 308 commits, daily publishing. The site is **4 days old**. Google treats fresh small sites as low-trust until signals accumulate.

> Evidence: `README.md`, `DEPLOY.md`, `robots.txt`, `sitemap.xml`, `feed.xml`, live `curl` probes.

---

## 2. Traffic / indexing diagnosis — "why no visitors"

Four independent reasons traffic is zero. Any one of them keeps you out of Google; together they guarantee it.

### 2.1 Google has never been told about the site
- `site:mani7702-dot.github.io/our-world` returns **0 results** on Google, Bing, and DuckDuckGo.
- `robots.txt` is correct (allows all, lists the sitemap), but correct robots does **not** mean Google reads or acts on the sitemap. The sitemap must be **submitted** in Search Console.

### 2.2 No Google Search Console property
- No Search Console verification meta tag is in the rendered `<head>`.
- The repo holds `googleab4657799e540d71.html` and `BingSiteAuth.xml`, but **neither is wired into the build** — they are orphan files, so GSC/Bing verification fails.
- Without Search Console you cannot (a) submit the sitemap, (b) see indexing errors, or (c) learn why Google isn't ranking you.

### 2.3 Free subdomain ranks slowly; trust is low
- GitHub Pages `*.github.io` is a free subdomain. Google indexes it, but treats it as lower-trust / fresh / thin. With only 4 days of history and **zero backlinks**, it sits below established domains for any query.

### 2.4 Content cadence is good but distribution is broken
- The VPS agent pipeline **is running** and producing ~24 articles/day (8 active cron jobs confirmed via `hermes cron list`). Freshness and volume are not the problem — **distribution to Google is.**

---

## 3. AdSense / monetization diagnosis — "how do we earn"

The single largest risk to your revenue goal. Three blockers, in order.

### 3.1 AdSense is **not actually installed**
- `grep -ri "adsbygoogle"` across `*.html`, `*.py`, `templates/*` → **0 results**. (One source file, `news/blueberries-mood-gut-brain-link.html`, contains the *word* "AdSense" in prose, but no ad tags.)
- No `ads.txt` at the root (`curl ads.txt` → **404**). Google requires `ads.txt` declaring authorized sellers; without it, **AdSense revenue is suppressed and your account risks policy suspension.**
- The README line "supported by Google AdSense" is **descriptive fiction** — there are no ads to support anything.

### 3.2 There is no AdSense account
- No `ca-pub-*` ID exists anywhere in the repo. You cannot monetize without an approved AdSense account tied to a verified property.

### 3.3 Free subdomain `*.github.io` is **not eligible for AdSense**
- AdSense requires that you **own the site you submit**. Google's policy excludes free-hosting subdomains where you do not control DNS (Blogger and a short list of *host partners* are the documented exceptions; `github.io` is not one). You cannot apply AdSense directly on `mani7702-dot.github.io`.

**Conclusion on AdSense:** You cannot turn on revenue on the current host with the current build. The revenue path is: own a domain → point it at this site → install AdSense tags + `ads.txt` → apply. That is a prerequisite, not an optimization.

---

## 4. Content pipeline audit (the 24/7 agents)

### 4.1 The pipeline is live and healthy
Confirmed on the VPS (`bots`):
- 8 `hermes` cron jobs running via the `our-world-site` skill: `news-science`, `news-space`, `news-animals`, `news-world`, `news-history`, `news-explainers`, `news-listicles`, `news-trending`.
- Schedules span 20–60 min intervals; each publishes **1 original article per run**.
- `lane-prompt-template.txt` enforces real guardrails: original text only, kid-safe tone, 2-independent-source fact-check, exact IST time, `Sources` block, abort-on-no-candidate.
- `tools/fetch-news.py` pulls from free feeds (ScienceDaily, GNN, BBC Science, Smithsonian, NASA, SpaceX).

### 4.2 Critical defect: posts are not reaching GitHub
- The VPS repo HEAD is **39 commits ahead** of `origin/main` in this local checkout, and contains the latest article ("Euclid comet discovery") that is **not present locally or on GitHub**.
- `git log --since='24 hours ago'` on VPS = **105 commits** vs. 347 total locally. The agents have published ~15 articles in the last 24h that are **stuck on the VPS and never pushed**.
- `ow-deploy.sh` ("git pull --rebase, build, commit, push") is failing on the push step or not running it. Each missed push = content the world never sees.
- All 8 jobs report **"Delivery failed: no delivery target resolved for deliver=telegram"** — the Telegram report channel is dead, so you get **no notification that pushes are failing**; you believe content is flowing when it is not.

### 4.3 Content quality is genuinely good
- 223 Markdown articles; 1 stray duplicate (same title in `content/news/` and `content/news/science/` — the `science/` folder is an anomaly).
- All 39 blog + 185 news posts carry `sample: false`; **6 stray posts still show `sample: true`** → "Sample — phase 2" badge is live on them.
- Articles use real Structured Data (`application/ld+json` Article schema) with `datePublished`, `author`, `publisher`, `inLanguage` — good for Google News/Top Stories.
- Tone is consistently kid-safe; no medical/legal/scary content found. Sources are cited with live URLs.

### 4.4 Minor issues
- `content/news/science/` should be emptied/moved back; `build.py` may double-publish the one file in it.
- Some image filenames are non-dated while others are dated — harmless but inconsistent.

> Evidence: `lane-prompt-template.txt`, `.github/workflows/telegram-notify.yml`, `build.py` (SITE_BASE), live `hermes cron list` via SSH.

---

## 5. Site quality / SEO hygiene

| Item | Status | Note |
|---|---|---|
| `robots.txt` | ok | allows all, lists sitemap |
| `sitemap.xml` / `feed.xml` | ok | 240 URLs |
| Structured data | ok | Article schema with date/author/publisher |
| Meta tags | ok | title/description/og/twitter via `templates/base.html` |
| **Canonical tags** | **missing** | duplicate-content risk vs. mirror host |
| **`og:url`** | **missing** | social previews may pick wrong URL |
| `ads.txt` | **missing** | blocks AdSense revenue |
| Page weight | wary | hero image 3.7 MB; home 18 KB but slow |
| Images | wary | 104 MB total, mostly unresized JPGs/PNGs; 3 WebP only |
| Lazy loading | partial | `loading="lazy"` on one `<img>`; no `srcset`/`sizes` |
| Internal links | solid | 0 broken of 1,032 checked |
| Sitemap **submitted** to Google | **no** | no Search Console = not submitted |

---

## 6. What's *not* broken (keep it)
- The design system, dark-mode toggle, 3 browser games, and kid-safe reading controls (A−/A+, easy-read) are working and intentional.
- The `build.py` static-site generator is simple and correct — the `build-guard.yml` CI even catches stale-build pushes.
- Content tone, fact-sourcing, and the agent prompt are strong and safe.

---

## 7. Action plan — ordered fixes

### A. Unblock indexing first (this week)
1. **Verify ownership in Google Search Console** — add the `googlebab4657799e540d71.html` file (already in repo) AND add a verification meta tag to `<head>` in `templates/base.html`, or let GSC verify via the HTML file served at `/google<...>.html`.
2. **Submit `sitemap.xml`** in GSC. Request index for the homepage + 2–3 flagship articles.
3. **Publish 2–3 human-written "pillar" pieces** (e.g. a parents' reading guide) so the home page has depth and backlinkable content.

### B. Unlock AdSense (next 1–3 weeks)
4. **Buy a real domain** (e.g. `ourworld.news` / `ourworld.site`). Do **not** reuse `ourworld.com` — it is taken and unrelated.
5. **Point the domain at GitHub Pages** — add a `CNAME` file (`ourworld.news`) and set a CNAME DNS record at your registrar → `<username>.github.io`. GitHub issues the HTTPS cert.
6. **Wait for Google to register first impressions** in GSC (needs days of verified traffic on the custom domain).
7. **Apply for AdSense** on the new domain.
8. **Install:** add the `ca-pub-xxxxxxxxxxxx` script in `templates/base.html`, one `<ins class="adsbygoogle">` slot above/below the article body, and a root-level `ads.txt` with `google.com, ca-pub-xxxxxxxx, DIRECT, f08c47fec0940fa3`.
9. **Rebuild + redeploy after every AdSense edit** (`python build.py && git add -A && git commit && git push`).

### C. Fix the publishing pipeline (this week)
10. **On the VPS, push the 39 missing commits + 15 missing articles to GitHub now** (`git push origin main` from `~/our-world`).
11. **Fix `tools/ow-deploy.sh` push step** — check exit codes and credentials; add a `git push` log line so failures are visible.
12. **Restore the Telegram delivery target** (currently failing everywhere) so you receive a report when an article publishes — otherwise you will not notice the next failure.
13. **Empty `content/news/science/`** so it can't double-build.

### D. Fix performance (this week)
14. **Resize images** to ≤1200 px and convert to WebP; hero should be ≤600 KB. Script this (`cwebp`/`ImageMagick` loop over `assets/images`).
15. **Add `loading="lazy"` + explicit `width`/`height`** to all `<img>`; make the article hero `loading="eager"` with a `<link rel=preload>`.
16. **Preload the hero image** and the CSS (`assets/css/styles.css`, 32 KB).

### E. Hygiene
17. **Add canonical + `og:url`** in `build.py` using the new `SITE_BASE`.
18. Set `sample: false` on the 6 remaining posts; rebuild.
19. Add a brief "About this site" note that it is an AI-assisted educational project (Google's transparency guidance increasingly favors clear authorship disclosure).

---

## 8. Expected outcome
- After **A1–3 + D**: Google begins indexing within days; expect 50–200 impressions/day by week 2.
- After **B4–7 + first approved ads**: AdSense revenue begins. For a kid-safety niche with 185+ articles, a realistic estimate is **$2–20 / month after 60–90 days** once traffic accumulates — AdSense is low-yield per impression, so the lever is *volume × targeting*, not the ad unit.
- The content engine (4 agents writing 24×7) is a real asset. Once indexing + domain + AdSense are fixed, the daily-cadence machine compounds.

**The site is not broken. It is simply not connected to Google, not monetized, and half its publishing is being swallowed by the VPS.** Fix the three red blockers above — Indexing → Domain + AdSense → VPS push gap — and traffic and revenue follow.

---

*Method: live `curl` probes of `mani7702-dot.github.io/our-world/`, `our-world.pages.dev`, and `ourworld.com`; grep audit of the repo for ad tags/Canonical; SSH session on the `bots` VPS reading `hermes cron list`, `git log`, and `ow-deploy.sh`; Bing/DuckDuckGo `site:` queries returning zero; `build.py` and template inspection; 1,032-link internal-link check. Repo is fresh, healthy, and under CI guard (`build-guard.yml`). No source was modified in producing this audit.*

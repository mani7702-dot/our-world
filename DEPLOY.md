# Deploying Our World

The site is plain static files, so hosting is free on either of two hosts. This guide assumes Windows + git-bash and the repo at `C:/Users/uday/our-world`.

## 0. Prerequisites

- [git](https://git-scm.com/download/win) installed
- A GitHub account
- A Cloudflare account (free plan is enough)

## 1. Push to GitHub

If you haven't pushed yet, run once:

```bash
gh auth login                       # one-time; or skip gh and use git directly (see below)
gh repo create our-world --public --source=. --push
```

No GitHub CLI? Do it by hand:

```bash
git remote add origin https://github.com/<your-username>/our-world.git
git push -u origin main
```

You should see the files appear on github.com within a few seconds.

## 2a. Cloudflare Pages (primary host)

1. Go to the Cloudflare dashboard → **Workers & Pages** → **Pages** → **Create a project**.
2. Choose **Connect to Git** and authorize Cloudflare on your GitHub account.
3. Select the `our-world` repository → **Begin setup**.
4. Settings:
   - **Framework preset:** `None`
   - **Build command:** *(leave empty)* — the site is already built
   - **Build output directory:** `/`
5. **Save and Deploy.** In about a minute the site is live at `https://<project-name>.pages.dev`.

### No-git quick test

Drag the whole `our-world` folder onto the Pages **"upload assets"** dropzone on the dashboard. Good for a 30-second preview before wiring up git.

### Custom domain (later)

Pages → your project → **Custom domains** → **Set up a domain** → follow the DNS step. Cloudflare handles the HTTPS certificate automatically.

## 2b. GitHub Pages (free mirror)

1. On GitHub: repo → **Settings** → **Pages**.
2. **Source:** Deploy from a branch → **Branch:** `main`, **Folder:** `/(root)` → **Save**.
3. After a minute or two the mirror is live at `https://<your-username>.github.io/our-world/`.

This is the backup. If Cloudflare ever has a bad day, the mirror keeps the site up. (Note: GitHub Pages is slower outside North America and has soft bandwidth limits — fine for a mirror, not as primary.)

## 3. Turn on the contact form (optional)

The About page already contains a Formspree-ready form. It stays dormant until you set a real form ID:

1. Create a free form at [formspree.io](https://formspree.io) (free tier: 50 submissions/month).
2. In `about/index.html`, replace `REPLACE_WITH_YOUR_FORM_ID` in the form action with your ID.
3. Rebuild and push:

```bash
python build.py
git add -A && git commit -m "Activate contact form"
git push
```

## 4. The daily update loop

Every change — a post, a page, the design — follows the same loop:

```bash
# 1. edit content/*.md (or any page/asset)
# 2. rebuild
python build.py
# 3. commit and push
git add -A
git commit -m "New post: why stars twinkle"
git push
```

Both hosts redeploy automatically within about a minute. Never push without rebuilding first — the repo's generated pages would ship stale.

## 5. Verify after each deploy

- Open the `*.pages.dev` URL.
- Check one article page (reading controls work), one game (plays), and the dark-mode toggle.
- Check the browser console for errors (F12 → Console tab): expect zero.

## Rollback

Cloudflare Pages keeps every deployment. Dashboard → your project → **Deployments** → pick the previous one → **Rollback**.

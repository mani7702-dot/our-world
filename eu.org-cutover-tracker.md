# Our World — eu.org cutover tracker

Date: 2026-10-24

## State
- eu.org DNS: live on Cloudflare (NS lee/keyla.ns.cloudflare.com), A proxied to 104.21.82.192 / 172.67.206.51, valid TLS cert (GTS).
- **BLOCKER: `https://ourworld.eu.org/` and `https://ourworld.pages.dev/` both return Cloudflare error 522 (origin timeout).** The eu.org origin appears to be a Cloudflare Pages project named `ourworld`, which is itself in a broken/unreachable state.
- No Cloudflare API token and no GSC API credentials exist on this machine → the 522 and any GSC data pulls require the Cloudflare/GSC dashboards (human).
- Repo still built for `mani7702-dot.github.io/our-world`; no CNAME file; GitHub Pages custom domain = null.

## Agreed plan (user chose "Fix 522 first, then cutover", "Cloudflare-proxied primary")
1. [ ] HUMAN: fix the 522 in the Cloudflare dashboard (see handoff note below).
2. [ ] Cutover: rebuild for eu.org + write CNAME + set GitHub Pages custom domain via API + commit + push.
3. [ ] Re-verify eu.org in GSC + Bing; set up 301s for old /our-world/ URLs.
4. [ ] (after live on eu.org) repoint the 5 tooling files off github.io:
       tools/ow-deploy.sh:64,71 · tools/indexnow-submit.py:8,9,10 · scripts/verify-live.py:5 · build.py:452 default.

## Verified
- `SITE_BASE="https://ourworld.eu.org" SITE_CNAME="ourworld.eu.org" CONTACT_EMAIL="contact@ourworld.eu.org" python3 build.py`
  builds clean; output has correct CNAME/robots/sitemap; 340 files carry eu.org. Proven in scratch copy /tmp/ow-cutover-test.
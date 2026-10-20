"""Fetch article text via urllib (no shell), strip HTML tags."""
import sys, re, urllib.request, html

UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=35) as r:
        return r.read().decode("utf-8", "replace")

def to_text(htmlstr):
    t = re.sub(r"<script[^>]*>.*?</script>", " ", htmlstr, flags=re.S)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()

for url in sys.argv[1:]:
    print("=== " + url + " ===")
    try:
        txt = fetch(url)
        print(to_text(txt)[:3500])
    except Exception as e:
        print("ERROR:", e)
    print()

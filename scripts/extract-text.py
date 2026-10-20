"""Extract readable text from a ScienceDaily (or similar) article URL.
Usage: python3 scripts/extract-text.py <url>
Downloads HTML to /tmp, strips boilerplate, walks <p> tags in the article.
File-based (Tirith-safe): never pipes curl into python -c.
"""
import sys, subprocess, re, os
from html.parser import HTMLParser

UA = "Mozilla/5.0 (OurWorldSite/1.0; contact: andugulamani722@gmail.com)"

def fetch(url, out):
    subprocess.run(["curl", "-s", "--compressed", "--max-time", "35", "-A", UA, url, "-o", out],
                   check=False, timeout=40)
    return out

class TextGrab(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.in_article = False
        self.seen = set()
        self.buf = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        cls = d.get("class", "") + " " + d.get("id", "")
        if any(k in cls.lower() for k in ("header","footer","nav","sidebar","menu","ad","cookie","social","popup","comment")):
            self.skip += 1
        if tag in ("script","style","svg"):
            self.skip += 1
        if tag == "p" and not self.skip:
            self._cap = True
        else:
            self._cap = False
    def handle_endtag(self, tag):
        if tag in ("script","style","svg"):
            self.skip = max(0, self.skip-1)
        if tag in ("header","footer","nav","aside","script","style","svg") and self.skip:
            self.skip = max(0, self.skip-1)
        if tag == "p":
            self._cap = False
    def handle_data(self, data):
        if self.skip or getattr(self, "_cap", False):
            return
        s = data.strip()
        if s and len(s) > 2:
            self.buf.append(s)

def main():
    url = sys.argv[1]
    fn = "/tmp/_article.html"
    fetch(url, fn)
    html = open(fn, encoding="utf-8", errors="ignore").read()
    # prefer the science-body / article-content div
    m = re.search(r'id="(?:science-body|article-body|text-body|mc-|main-text)"', html)
    h2 = re.search(r'class="(?:article|story|body)[^"]*text', html)
    # strip scripts/styles for cleaner grab
    html2 = re.sub(r'<(script|style|svg)[^>]*>.*?</\1>', '', html, flags=re.S|re.I)
    p = TextGrab()
    p.feed(html2)
    text = "\n".join(p.buf)
    # fallback: all <p>
    if len(text) < 400:
        ps = re.findall(r'<p[^>]*>(.*?)</p>', html2, re.S|re.I)
        text = "\n".join(re.sub(r'<[^>]+>','',x).strip() for x in ps if re.sub(r'<[^>]+>','',x).strip())
    print(text[:3000])

if __name__ == "__main__":
    main()

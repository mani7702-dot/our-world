#!/usr/bin/env python3
"""Extract article text from BBC article using urllib and HTML parsing."""
import urllib.request, re, html as htmlmod

UA = "Mozilla/5.0 (compatible; OurWorldBot/1.0; contact andugulamani722@gmail.com)"

urls = [
    "https://www.bbc.com/news/articles/c20917w25n4o",  # How cleaning up the air is speeding up global warming
    "https://www.bbc.com/news/videos/cmx2302xe931o",  # Why is a peat fire so bad?
]

for url in urls:
    print(f"\n=== {url} ===")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=20)
        content = resp.read().decode("utf-8", errors="ignore")
        # Remove scripts and styles
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL|re.IGNORECASE)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL|re.IGNORECASE)
        # Try to get title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE|re.DOTALL)
        if title_match:
            title = htmlmod.unescape(title_match.group(1).strip())
            print(f"TITLE: {title}")
        
        # Get meta description
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE|re.DOTALL)
        if desc_match:
            desc = htmlmod.unescape(desc_match.group(1).strip())
            print(f"DESC: {desc[:300]}")
        
        # Get paragraphs from main content
        # Remove tags but keep text
        body = re.sub(r'<[^>]+>', ' ', content)
        body = htmlmod.unescape(body)
        body = re.sub(r'\s+', ' ', body).strip()
        # Find the main article content
        # Look for key phrases
        for phrase in ["peat", "global warming", "aerosol", "sulfate", "dimethyl", "sulphate"]:
            if phrase.lower() in body.lower():
                idx = body.lower().find(phrase)
                print(f"\nContext around '{phrase}':")
                start = max(0, idx-200)
                end = min(len(body), idx+500)
                print(body[start:end])
                break
        print("...")
        
    except Exception as e:
        print(f"ERROR: {e}")

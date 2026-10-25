#!/usr/bin/env python3
"""Check for fresh science stories from multiple sources."""
import urllib.request, re, html, os, json
import xml.etree.ElementTree as ET

os.chdir("/home/ubuntu/our-world")
UA = "Mozilla/5.0 (compatible: OurWorldBot; contact andugulamani722@gmail.com)"

feeds = {
    "BBC Science": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "Smithsonian": "https://www.smithsonianmag.com/feed/",
    "NPR Science": "https://www.npr.org/rss/rss.php?f=1007",
    "NPR Health": "https://www.npr.org/rss/rss.php?f=1127",
    "PhysOrg": "https://www.phys.org/rss/Science/",
    "EurekAlert": "https://www.eurekalert.org/rss/science-news.xml",
    "ScienceDaily": "https://www.sciencedaily.com/rss/top.xml",
}

# Build content corpus
all_content = ""
for f in os.listdir("content/news"):
    if f.endswith(".md"):
        with open(f"content/news/{f}", "r", errors="replace") as fh:
            all_content += fh.read().lower() + "\n"

BLOCK = (
    "cancer", "alzheimer", "covid", "pandemic", "stroke", "depression",
    "anxiety", "ptsd", "parkinson", "arthritis", "diabetes", "blood pressure",
    "statin", "colorectal", "cardiovascular", "heart disease", "glioblastoma",
    "rheumatoid", "weight-loss", "lung cancer", "breast cancer", "brain cancer",
    "political", "election", "lawsuit",
)

for name, url in feeds.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        data = urllib.request.urlopen(req, timeout=20).read()
        
        if data[:5] == b"<?xml" or b"<rss" in data[:200] or b"<feed" in data[:200]:
            idx = data.rfind(b"</rss>")
            if idx > 0:
                data = data[:idx + 6]
            elif b"<feed" in data[:200]:
                idx = data.rfind(b"</feed>")
                if idx > 0:
                    data = data[:idx + 7]
            try:
                root = ET.fromstring(data)
            except:
                root = ET.fromstring(data[:data.rfind(b">") + 1])
            
            count = 0
            for it in root.iter("item"):
                t = (it.findtext("title") or "").strip()
                l = (it.findtext("link") or "").strip()
                d = (it.findtext("description") or "").strip()
                d = re.sub(r"<[^>]+>", "", d).strip()
                pd = (it.findtext("pubDate") or "").strip()
                
                if not t or len(t) < 25:
                    continue
                if any(b in t.lower() for b in BLOCK):
                    continue
                
                slug = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
                slug_match = any(slug[:15] in f.lower() for f in os.listdir("content/news"))
                
                title_words = [w for w in re.findall(r"\b[a-zA-Z]{6,}\b", t.lower())]
                title_matches = sum(1 for w in title_words[:5] if w in all_content)
                
                status = "PUBLISHED" if slug_match or title_matches >= 3 else "*** FRESH? ***"
                print(f"{status} | {name}: {t}")
                print(f"  URL: {l}")
                count += 1
            
            print(f"\n--- {name}: {count} kid-safe items ---\n")
        else:
            print(f"{name}: NOT XML (blocked)\n")
    except Exception as e:
        print(f"{name}: ERROR - {e}\n")
#!/usr/bin/env python3
"""Comprehensive dedup check: fetch ScienceDaily top.xml, extract titles/links,
check each against existing content/news/ articles by keyword AND by slug."""
import urllib.request, re, html, os, json

os.chdir("/home/ubuntu/our-world")

URL = "https://www.sciencedaily.com/rss/top.xml"
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

req = urllib.request.Request(URL, headers={"User-Agent": UA})
data = urllib.request.urlopen(req, timeout=25).read()
idx = data.rfind(b"</rss>")
data = data[:idx + 6]

# Parse with regex to get pubDate too
items = re.findall(rb"<item>(.*?)</item>", data, re.DOTALL)
parsed = []
for it in items:
    t = re.search(rb"<title>(.*?)</title>", it, re.DOTALL)
    l = re.search(rb"<link>(.*?)</link>", it, re.DOTALL)
    pd = re.search(rb"<pubDate>(.*?)</pubDate>", it, re.DOTALL)
    d = re.search(rb"<description>(.*?)</description>", it, re.DOTALL)
    if t and l:
        title = html.unescape(t.group(1).decode("utf-8", errors="replace").strip())
        # Remove CDATA wrapper if present
        title = re.sub(r"^<!\[CDATA\[(.*?)\]\]>$", r"\1", title)
        link = html.unescape(l.group(1).decode("utf-8", errors="replace").strip())
        date = html.unescape(pd.group(1).decode("utf-8", errors="replace").strip()) if pd else ""
        desc = html.unescape(re.sub(rb"<[^>]+>", b"", d.group(1) if d else b"").decode("utf-8", errors="replace"))
        parsed.append({"title": title, "link": link, "date": date, "desc": desc[:300]})

# Get existing article titles from filenames and frontmatter
existing_articles = {}  # slug -> title
for f in sorted(os.listdir("content/news")):
    if f.endswith(".md"):
        filepath = f"content/news/{f}"
        with open(filepath, "r", errors="replace") as fh:
            content = fh.read()
        # Extract title from frontmatter
        title_match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
        title = title_match.group(1) if title_match else ""
        existing_articles[f] = title

# Build full content corpus
all_content = ""
for f in os.listdir("content/news"):
    filepath = f"content/news/{f}"
    if os.path.isfile(filepath):
        with open(filepath, "r", errors="replace") as fh:
            all_content += fh.read().lower() + "\n"

print(f"Total ScienceDaily items: {len(parsed)}")
print(f"Existing articles: {len(existing_articles)}")

# Check each ScienceDaily item
BLOCK = (
    "cancer", "alzheimer", "covid", "pandemic", "stroke", "depression",
    "anxiety", "ptsd", "parkinson", "arthritis", "diabetes", "blood pressure",
    "statin", "colorectal", "inflammatory bowel", "cardiovascular",
    "heart disease", "glioblastoma", "rheumatoid", "weight-loss drug",
    "blood thinner", "brain cancer", "lung cancer", "breast cancer",
    "surgery", "therapy", "clinical trial",
)

fresh = []
for item in parsed:
    title = item["title"]
    link = item["link"]
    low_title = title.lower()
    
    # Skip blocked
    if any(b in low_title for b in BLOCK):
        continue
    
    # Check slug
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", low_title).strip("-")
    
    # Check if slug matches any existing file
    slug_match = any(slug in f.lower() for f in existing_articles)
    if slug_match:
        continue
    
    # Check if title keywords appear in existing content
    words = [w.lower() for w in re.findall(r"\b[a-zA-Z]{5,}\b", title)]
    matches = sum(1 for w in words[:6] if w in all_content)
    
    if matches >= 3:
        continue
    
    fresh.append(item)

print(f"\n=== FRESH CANDIDATES ({len(fresh)}) ===")
for item in fresh:
    print(f"\n  Title: {item['title']}")
    print(f"  Date:  {item['date']}")
    print(f"  URL:   {item['link']}")
    print(f"  Desc:  {item['desc'][:300]}")

# Save fresh candidates
with open("_fresh_candidates.json", "w") as f:
    json.dump(fresh, f, indent=2)

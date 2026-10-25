#!/usr/bin/env python3
"""Cross-check Amazon forest conservation study via Wikipedia API and Science journal."""
import urllib.request, json, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# 1. ScienceDaily article (primary source) - already fetched
# Key facts from SD:
# - Study published in Science journal
# - International team: UK, Brazil, Sweden, Australia
# - Lead: Lancaster University
# - Study area: >3M hectares in Santarém and Paragominas, Pará, Brazil (2010-2020)
# - 381 survey transects, 38 catchments, 499 rural properties
# - 160 bird species, 426 tree species models
# - Key finding: protecting standing forests (preventing fire + logging) delivers greatest biodiversity + carbon benefits
# - Restoration important but more expensive, less effective alone

# 2. Wikipedia cross-check - Amazon rainforest, deforestation, protected areas
topics = [
    "Amazon_rainforest",
    "Deforestation",
    "Protected_area",
    "List_of_places_converted_from_other_use_to_protected_areas",
]

for topic in topics:
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=true&explaintext=true&titles={topic}&format=json"
    req = urllib.request.Request(api_url, headers={"User-Agent": UA})
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        data = json.loads(resp.read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if "extract" in page:
                extract = page["extract"][:600]
                print(f"\n=== Wikipedia: {topic} ===")
                print(extract)
                break
        else:
            print(f"\n=== Wikipedia: {topic} ===")
            print("  (no extract / page not found)")
    except Exception as e:
        print(f"\n=== Wikipedia: {topic} ===")
        print(f"  Error: {e}")

# 3. Also check the ScienceDaily article for journal reference
print("\n=== Checking ScienceDaily for journal citation ===")
url = "https://www.sciencedaily.com/releases/2026/09/260920222356.htm"
req = urllib.request.Request(url, headers={"User-Agent": UA})
resp = urllib.request.urlopen(req, timeout=30)
html = resp.read().decode("utf-8", errors="replace")

# Look for journal name, DOI, or citation
journal_refs = re.findall(r'(Science|Nature|PNAS|Proceedings)[^<]{0,80}', html)
print(f"Journal refs: {journal_refs[:5]}")

doi_refs = re.findall(r'doi\.org/[^"<\s]+', html)
print(f"DOI refs: {doi_refs[:5]}")

# Look for the research paper link
paper_links = re.findall(r'https://[^"]*(science|advances|nature|pnas)[^"]*', html, re.I)
print(f"Paper links: {paper_links[:5]}")

# Extract more of the article body for cross-check
paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
for i, p in enumerate(paragraphs[15:25], 15):
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(clean) > 40:
        print(f"\n[{i}] {clean[:300]}")

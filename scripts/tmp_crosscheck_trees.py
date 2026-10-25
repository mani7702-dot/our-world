import urllib.request, re, html

# Source 1: ScienceDaily article
url1 = "https://www.sciencedaily.com/releases/2026/09/260922005712.htm"
req1 = urllib.request.Request(url1, headers={"User-Agent": "Mozilla/5.0 (compatible; OurWorldBot/1.0)"})
sd_html = urllib.request.urlopen(req1, timeout=25).read().decode('utf-8', errors='replace')

desc = re.search(r'<meta name="description" content="([^"]+)"', sd_html)
print("=== ScienceDaily ===")
print(html.unescape(desc.group(1)[:800]) if desc else "No desc")

# Source 2: Wikipedia on CAM photosynthesis
url2 = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=true&explaintext=true&format=json&titles=Crassulacean%20acid%20metabolism"
req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0 (compatible; OurWorldBot/1.0)"})
wp_data = urllib.request.urlopen(req2, timeout=25).read().decode('utf-8', errors='replace')
wp = __import__('json').loads(wp_data)
pages = wp.get('query', {}).get('pages', {})
for pid, pg in pages.items():
    extract = pg.get('extract', '')
    print("\n=== Wikipedia (CAM photosynthesis) ===")
    print(extract[:1200])

# Source 3: Wikipedia on Clusia
url3 = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=true&explaintext=true&format=json&titles=Clusia"
req3 = urllib.request.Request(url3, headers={"User-Agent": "Mozilla/5.0 (compatible; OurWorldBot/1.0)"})
wp2_data = urllib.request.urlopen(req3, timeout=25).read().decode('utf-8', errors='replace')
wp2 = __import__('json').loads(wp2_data)
pages2 = wp2.get('query', {}).get('pages', {})
for pid, pg in pages2.items():
    extract = pg.get('extract', '')
    print("\n=== Wikipedia (Clusia) ===")
    print(extract[:800])

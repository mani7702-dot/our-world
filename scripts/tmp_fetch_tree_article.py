import urllib.request, re

url = "https://www.sciencedaily.com/releases/2026/09/260922005712.htm"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; OurWorldBot/1.0)"})
html_data = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='replace')

# Extract description from meta
desc = re.search(r'<meta name="description" content="([^"]+)"', html_data)
if desc:
    print("META DESC:", desc.group(1)[:500])

# Find the article body - look for story-body or typical ScienceDaily content
body_match = re.search(r'<div[^>]*id="text-body-[^"]*"[^>]*>(.*?)</div>', html_data, re.DOTALL)
if not body_match:
    body_match = re.search(r'<div[^>]*class="[^"]*story-body[^"]*"[^>]*>(.*?)</div>', html_data, re.DOTALL)
if body_match:
    text = body_match.group(1)
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    print("BODY:", text[:2000])

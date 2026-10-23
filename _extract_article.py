import subprocess, re, html, os

url = "https://phys.org/news/2026-10-farming-medieval-tsunamis-italian-lake.html"
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
p = subprocess.run(['curl', '-sL', '--max-time', '30', '-A', ua, url], capture_output=True)
content = p.stdout.decode('utf-8', errors='replace')

# Save raw for inspection
with open('/tmp/physorg_article.html', 'w') as f:
    f.write(content)

print(f"Content length: {len(content)}")

# Extract text
text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = html.unescape(text)
text = re.sub(r'\s+', ' ', text)

# Find the article section
idx = text.find('farming helped cause')
if idx > 0:
    article = text[idx:]
else:
    article = text[-3000:]

print(article[:5000])

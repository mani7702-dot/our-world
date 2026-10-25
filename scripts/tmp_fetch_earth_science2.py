import urllib.request
url = "https://www.sciencedaily.com/rss/earth_climate/earth_science.xml"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; OurWorldBot/1.0)"})
data = urllib.request.urlopen(req, timeout=25).read()
open('/home/ubuntu/our-world/sd-earth-science.xml', 'wb').write(data)
print("Saved", len(data), "bytes")

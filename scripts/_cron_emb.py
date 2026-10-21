import re
raw = open("/tmp/bbc-air.html", encoding="utf-8", errors="replace").read()
# Find all hrefs pointing to external research/orgs (ETH, Cicero, Met Office, Nature, Science, IPCC, Wiley)
links = re.findall(r'href="(https?://[^"]+)"', raw)
seen = set()
for l in links:
    low = l.lower()
    if any(k in low for k in ["ethz", "eth.ch", "cicero", "metoffice", "metoffice.gov.uk", "nature.com", "science.org", "ipcc.ch", "wiley.com", "springer.com", "sciencedaily", "doi.org", "nasa.gov", "noaa", "climate.gov"]):
        if l not in seen:
            seen.add(l)
            print(l)

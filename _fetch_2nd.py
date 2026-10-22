#!/usr/bin/env python3
import subprocess

# Fetch the BBC source referenced in the NASA article
url = "https://www.bbc.co.uk/news/articles/cq78pzl85nglo" # Not the right URL
# Actually the NASA article references BBC (2026, October 14) Gales and heavy rain
# Let me search for the BBC article about Isaias Iceland gales

result = subprocess.run(['curl', '-s', '--compressed', '--max-time', '20', '-A', 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'https://www.bbc.com/news/topics/cb8q0g5lygmt/topics/gales-heavy-rain-uk-wind-warning'],
    capture_output=True, text=True)
print(f"BBC search bytes: {len(result.stdout)}")

# Try CIMSS satellite blog
result2 = subprocess.run(['curl', '-s', '--compressed', '--max-time', '20', '-A',
    'Mozilla/5.0',
    'https://cimss.wisc.edu/satblog/'], capture_output=True, text=True)
print(f"CIMSS bytes: {len(result2.stdout)}")

# Try Wikipedia for extratropical cyclone info as 2nd source
result3 = subprocess.run(['curl', '-s', '--compressed', '--max-time', '20', '-A',
    'Mozilla/5.0',
    'https://en.wikipedia.org/wiki/Extratropical_cyclone'], capture_output=True, text=True)
print(f"Wikipedia bytes: {len(result3.stdout)}")

# Save what we have
with open('/tmp/bbc_search.html', 'w') as f:
    f.write(result.stdout)
with open('/tmp/cimss.html', 'w') as f:
    f.write(result2.stdout)
with open('/tmp/wiki_extratropical.html', 'w') as f:
    f.write(result3.stdout)

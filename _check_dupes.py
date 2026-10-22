import os

existing = []
for fn in sorted(os.listdir('/home/ubuntu/our-world/content/news')):
    if fn.endswith('.md'):
        existing.append(fn[:-3])

candidates = [
    ("RS-25 Engine Test", "rs-25-engine-test"),
    ("JPL 90th anniversary", "jpl-90th"),
    ("NASA simulated mars crew", "simulated-mars"),
    ("Hubble Spiral Edge", "hubbles-spiral"),
    ("NASA NCAA flyover", "ncaa"),
    ("Science Station Jessica Watkins", "jessica-watkins"),
    ("CASALS instrument", "casals"),
    ("TIME Best Inventions", "time-best"),
    ("What's Up October", "whats-up-october"),
    ("Roman Telescope", "roman-telescope"),
    ("Artemis II", "artemis-ii"),
]

for title, keyword in candidates:
    found = [e for e in existing if keyword.lower() in e.lower()]
    if found:
        print(f'"{title}" ({keyword}) -> FOUND: {found}')
    else:
        print(f'"{title}" ({keyword}) -> NOT FOUND')

# Also list all existing articles with dates
print("\n--- ALL EXISTING ARTICLES ---")
for e in sorted(existing):
    print(e)

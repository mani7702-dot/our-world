#!/usr/bin/env python3
"""Cross-check Artemis III facts from NASA + Wikipedia via urllib (Tirith-safe)."""
import urllib.request, re, json

def fetch(url, ua="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"):
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return resp.read().decode('utf-8','replace')
    except Exception as e:
        return f"ERROR fetching {url}: {e}"

def to_text(html):
    h = re.sub(r'<script[^>]*>.*?</script>',' ',html,flags=re.DOTALL|re.IGNORECASE)
    h = re.sub(r'<style[^>]*>.*?</style>',' ',h,flags=re.DOTALL|re.IGNORECASE)
    h = re.sub(r'<[^>]+>',' ',h)
    h = re.sub(r'&mdash;','—',h); h = re.sub(r'&ndash;','–',h)
    h = re.sub(r'&amp;','&',h); h = re.sub(r'&nbsp;',' ',h)
    h = re.sub(r'\s+',' ',h)
    return h.strip()

# NASA Artemis III program page
nasa = fetch("https://www.nasa.gov/specials/artemis-iii/")
nasa2 = fetch("https://www.nasa.gov/missions/arty/artemis-iii/")

# Wikipedia: Artemis II, III, Orion, Starship, New Glenn, astronauts
wiki_articles = [
    "Artemis_II",
    "Artemis_III",
    "Orion_(spacecraft)",
    "Starship_(vehicle)",
    "New_Glenn_(rocket)",
    "Luca_Parmitano",
    "Randy_Bresnik",
]
wikis = {}
for art in wiki_articles:
    rest = fetch(f"https://en.wikipedia.org/api/rest_v1/page/summary/{art}")
    wikis[art] = to_text(rest)[:500]

# Artemis II (April 2026 around moon)
wiki_ar2_full = to_text(fetch("https://en.wikipedia.org/wiki/Artemis_II"))

print("=== WIKIPEDIA SUMMARIES (cross-check) ===")
for art, txt in wikis.items():
    print(f"\n--- {art} ---")
    print(txt[:300] if txt else "NO CONTENT")

# grep for key facts
print("\n\n=== KEY FACT GREP (NASA Artemis III) ===")
print("NASA III contains 'crew':", "crew" in nasa.lower(), "astronaut" in nasa.lower())
print("NASA III contains 'Parmitano':", "parmitano" in nasa.lower())
print("NASA III contains 'Bresnik':", "bresnik" in nasa.lower())
print("NASA III contains 'Starship':", "starship" in nasa.lower())
print("NASA III contains 'New Glenn':", "new glenn" in nasa.lower())
print("NASA III contains 'Blue Moon':", "blue moon" in nasa.lower())

print("\n=== Wikipedia Artemis III section (key phrases) ===")
for phrase in ["Bresnik","Parmitano","Douglas","Rubio","Starship","New","2028","south pole"]:
    hits = [a for a,t in wikis.items() if phrase.lower() in t.lower()]
    print(f"phrase '{phrase}' in wiki summaries: {hits}")

print("\n=== Wikipedia Artemis_II summary ===")
print(wikis.get('Artemis_II','none')[:400])

# Also full text of Artemis III wiki for astronaut crew
full_iii = fetch("https://en.wikipedia.org/wiki/Artemis_III")
full_iii_txt = to_text(full_iii)
print("\n=== Artemis III wiki (astronaut names found) ===")
for name in ["Bresnik","Parmitano","Douglas","Rubio","Victor Glover","Reid Wiseman","Jeemin"]:
    print(f"  {name}: {name.lower() in full_iii_txt.lower()}")
print("  '2028' south pole:", "2028" in full_iii_txt, "south pole" in full_iii_txt.lower())
print("\nNASA III first 800 chars of text:")
print(to_text(nasa)[:800])

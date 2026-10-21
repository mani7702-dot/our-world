import os, re

content_dirs = ["content/news", "content/blog"]
all_content = {}
for d in content_dirs:
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                fpath = os.path.join(d, f)
                with open(fpath, "r", errors="replace") as fh:
                    all_content[fpath] = fh.read().lower()

# BBC Science candidates with specific stable tokens per item
candidates = [
    ("Storm Austen to bring severe gales to UK", "https://www.bbc.co.uk/weather/articles/c9rkyjzgp6kdo", "world", ["storm", "austen", "gale", "uk", "wind"]),
    ("Orionid meteor shower to peak in UK skies this week", "https://www.bbc.co.uk/weather/articles/cm17knj9kpv8o", "world", ["orionid", "meteor", "shower"]),
    ("First dinosaur bone from Antarctica found in a drawer", "https://www.bbc.co.uk/news/articles/cdep67jnn9zo", "world", ["dinosaur", "antarctica", "fossil", "titanosaur"]),
    ("Fears for protected bats if glamping pod plans are approved", "https://www.bbc.co.uk/news/articles/c6dxwg50pq8lo", "world", ["glamping", "pod", "bat", "protected"]),
    ("Fuel leak spreads more than two miles along River Taff", "https://www.bbc.co.uk/news/articles/c8vgxnp5w6vzo", "world", ["fuel", "leak", "river", "taff"]),
    ("Massive wasps nest in wildlife office dismantled", "https://www.bbc.co.uk/news/articles/cwx28pkn8p8yo", "world", ["wasp", "nest", "wildlife", "dismantled"]),
    ("Estate records abundance of wildlife despite drought", "https://www.bbc.co.uk/news/articles/crgqw4lg3y83o", "world", ["estate", "wildlife", "abundance", "drought"]),
    ("Farmer lost out by minutes in race for wildlife funding", "https://www.bbc.co.uk/news/articles/cm9qznp3gdvdo", "world", ["farmer", "wildlife", "funding", "lost"]),
    ("The British island where red squirrels are thriving", "https://www.bbc.co.uk/news/articles/cw1m4e3mrljxo", "world", ["red", "squirrel", "island", "jersey", "thriving"]),
    ("Capybara pups at Manx zoo draw record crowds", "https://www.bbc.co.uk/news/articles/cw7vplvjd3elo", "world", ["capybara", "pup", "manx", "zoo"]),
    ("How to move 1300 plants for Kews Palm House mega makeover", "https://www.bbc.co.uk/news/videos/c914d43gg2zdo", "world", ["palm", "house", "kew", "plant", "makeover"]),
    ("After record heat could the Atlantic make Britains weather even more extreme", "https://www.bbc.co.uk/news/articles/c992e8g10nmo", "world", ["atlantic", "heat", "record", "weather", "extreme"]),
    ("Severe drought declared and hosepipe bans in force", "https://www.bbc.co.uk/news/articles/crk661074ejo", "world", ["drought", "hosepipe", "ban", "severe"]),
    ("The hidden cost of the night shift and how to sleep it off", "https://www.bbc.co.uk/news/articles/cp9errxl97go", "world", ["night", "shift", "sleep"]),
    ("Giant tunnel proposed to clean up Windermere's sewage problem", "https://www.bbc.co.uk/news/articles/cr5yn4pky527o", "world", ["windermere", "sewage", "tunnel", "clean"]),
    ("Huge fin whale filmed off Welsh coast", "https://www.bbc.co.uk/news/videos/cxly491v6p7yo", "world", ["fin", "whale", "wales", "welsh"]),
    ("BBC visits wildfire front in haze-choked Indonesia", "https://www.bbc.co.uk/news/videos/cm9wzye55j4xo", "world", ["indonesia", "wildfire", "haze"]),
    ("World's oldest shipwreck found off coast of Turkey", "https://www.bbc.co.uk/news/articles/c6gr80rk1yyko", "world", ["shipwreck", "turkey", "kekova", "amphora"]),
    ("Dog that hunts invasive sea vomit honoured as animal of the year", "https://www.bbc.co.uk/news/articles/cvwy761zyx7eo", "world", ["sea", "vomit", "squirt", "dog", "sgiath"]),
    ("How cleaning up the air is speeding up global warming", "https://www.bbc.co.uk/news/articles/c20917w25n4o", "world", ["air", "clean", "aerosol", "warming"]),
    ("Five ways El Nino is affecting the weather around the world", "https://www.bbc.co.uk/weather/articles/c6dx07dznpyyo", "world", ["el nino", "weather", "global"]),
    ("Mission blasts off for Mars to grab a piece of its moon", "https://www.bbc.co.uk/news/articles/cmvgxvkv54w1o", "world", ["mars", "moon", "phobos", "mmx"]),
    ("Moment giant fin whale's huge mouth engulfs thousands of gallons of water", "https://www.bbc.co.uk/news/articles/cjr4yeygwdxvo", "world", ["fin", "whale", "mouth", "engulf"]),
]

MED_BLOCK = ("medical", "poisoning", "disease", "treatment", "therapy", "diagnosis", "disorder", 
             "surgery", "cancer", "ebola", "epidemic", "virus", "infection", "patient", 
             "clinical", "illness", "symptom", "health problem", "hospital")
POL_BLOCK = ("election", "politic", "lawsuit", "war", "terror", "killed", "death toll", 
             "murder", "shooting", "bomb", "riot", "protest", "arrest", "charged", 
             "beheaded", "military", "tariff", "putin", "trump", "zelenksy", "kim jong",
             "ukraine", "sudan", "haitian", "immigration", "openai", "federal probe")
VIOLENCE_BLOCK = ("killed", "death", "attack", "bomb", "shooting", "beheaded", "blood", 
                   "violent clash", "died", "fatal", "deadly")

for title, url, lane, stable_tokens in candidates:
    dupes = []
    for fpath, content in all_content.items():
        # Match stable tokens
        matches = [t for t in stable_tokens if t in content]
        if len(matches) >= 2:  # need at least 2 stable tokens to match
            dupes.append((fpath, matches))

    title_lower = title.lower()
    is_med = any(b in title_lower for b in MED_BLOCK)
    is_pol = any(b in title_lower for b in POL_BLOCK)
    is_violence = any(b in title_lower for b in VIOLENCE_BLOCK)

    status = "FRESH"
    if dupes:
        status = "DUP"
    elif is_med:
        status = "MED-BLOCK"
    elif is_pol or is_violence:
        status = "POL-BLOCK"

    print(f"[{lane}] {status}: {title}")
    if dupes:
        for d, m in dupes:
            print(f"  -> dupe: {d} (matched: {m})")
    print(f"  url: {url}")
    if status == "FRESH":
        print(f"  ** CANDIDATE **")
    print()

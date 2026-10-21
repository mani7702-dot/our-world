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

# BBC Science & Environment candidates
candidates = [
    ("Giant tunnel proposed to clean up Windermere's sewage problem", "https://www.bbc.co.uk/news/articles/cr5yn4pky527o", "world"),
    ("Huge fin whale filmed off Welsh coast", "https://www.bbc.co.uk/news/videos/cxly491v6p7yo", "world"),
    ("Moment giant fin whale's huge mouth engulfs thousands of gallons of water", "https://www.bbc.co.uk/news/articles/cjr4yeygwdxvo", "world"),
    ("Storm Austen to bring severe gales to UK", "https://www.bbc.co.uk/weather/articles/c9rkyjzgp6kdo", "world"),
    ("Orionid meteor shower to peak in UK skies this week", "https://www.bbc.co.uk/weather/articles/cm17knj9kpv8o", "world"),
    ("Northern Ireland needs courage and leadership to tackle climate change", "https://www.bbc.co.uk/news/articles/cxzd6j5q0g7eo", "world"),
    ("Five ways El Nino is affecting the weather around the world", "https://www.bbc.co.uk/weather/articles/c6dx07dznpyyo", "world"),
    ("Mission blasts off for Mars to grab a piece of its moon", "https://www.bbc.co.uk/news/articles/cmvgxvkv54w1o", "world"),
    ("BBC visits wildfire front in haze-choked Indonesia", "https://www.bbc.co.uk/news/videos/cm9wzye55j4xo", "world"),
    ("Fears for protected bats if glamping pod plans are approved", "https://www.bbc.co.uk/news/articles/c6dxwg50pq8lo", "world"),
    ("Fuel leak spreads more than two miles along River Taff", "https://www.bbc.co.uk/news/articles/c8vgxnp5w6vzo", "world"),
    ("How to see the Orionid meteor shower", "https://www.bbc.co.uk/weather/articles/c64gr18jrvx3o", "world"),
    ("Massive wasps nest in wildlife office dismantled", "https://www.bbc.co.uk/news/articles/cwx28pkn8p8yo", "world"),
    ("Estate records abundance of wildlife despite drought", "https://www.bbc.co.uk/news/articles/crgqw4lg3y83o", "world"),
    ("Farmer lost out by minutes in race for wildlife funding", "https://www.bbc.co.uk/news/articles/cm9qznp3gdvdo", "world"),
    ("The British island where red squirrels are thriving", "https://www.bbc.co.uk/news/articles/cw1m4e3mrljxo", "world"),
    ("Capybara pups at Manx zoo draw record crowds", "https://www.bbc.co.uk/news/articles/cw7vplvjd3elo", "world"),
    ("First dinosaur bone from Antarctica found in a drawer", "https://www.bbc.co.uk/news/articles/cdep67jnn9zo", "world"),
    ("Fossil identified as first dinosaur ever found in Antarctica", "https://www.bbc.co.uk/news/videos/c8r2074l0rmo", "world"),
    ("How cleaning up the air is speeding up global warming", "https://www.bbc.co.uk/news/articles/c20917w25n4o", "world"),
    ("After record heat could the Atlantic make Britains weather even more extreme", "https://www.bbc.co.uk/news/articles/c992e8g10nmo", "world"),
    ("How to move 1300 plants for Kews Palm House mega makeover", "https://www.bbc.co.uk/news/videos/c914d43gg2zdo", "world"),
    ("World's oldest shipwreck found off coast of Turkey", "https://www.bbc.co.uk/news/articles/c6gr80rk1yyko", "world"),
    ("Dog that hunts invasive sea vomit honoured as animal of the year", "https://www.bbc.co.uk/news/articles/cvwy761zyx7eo", "world"),
    ("Severe drought declared and hosepipe bans in force", "https://www.bbc.co.uk/news/articles/crk661074ejo", "world"),
    ("The hidden cost of the night shift and how to sleep it off", "https://www.bbc.co.uk/news/articles/cp9errxl97go", "world"),
]

MED_BLOCK = ("medical", "poisoning", "disease", "treatment", "therapy", "diagnosis", "disorder", 
             "surgery", "cancer", "ebola", "epidemic", "virus", "infection", "patient", 
             "clinical", "illness", "symptom", "health", "hospital", "drug")
POL_BLOCK = ("election", "politic", "lawsuit", "war", "terror", "killed", "death toll", 
             "murder", "shooting", "bomb", "riot", "protest", "arrest", "charged", 
             "beheaded", "drone", "military", "tariff", "Putin", "Trump", "Zelensky", 
             "Kim Jong", "Ukraine", "Sudan", "Haitian", "immigration", "OpenAI", 
             "federal probe", "intelligence", "spying", "senator", "investigation",
             "leadership", "climate change", "Northern Ireland")  # climate change = political topic

for title, url, lane in candidates:
    dupes = []
    for fpath, content in all_content.items():
        tokens = [t for t in title.lower().split() if len(t) > 4]
        if len(tokens) > 0:
            matches = sum(1 for t in tokens if t in content)
            if matches >= 2:
                dupes.append(fpath)

    is_med = any(b in title.lower() for b in MED_BLOCK)
    is_pol = any(b in title.lower() for b in POL_BLOCK)

    status = "FRESH"
    if dupes:
        status = "DUP"
    elif is_med:
        status = "MED-BLOCK"
    elif is_pol:
        status = "POL-BLOCK"

    print(f"[{lane}] {status}: {title}")
    if dupes:
        for d in dupes:
            print(f"  -> dupe: {d}")
    print(f"  url: {url}")
    if status == "FRESH":
        print(f"  ** CANDIDATE **")
    print()

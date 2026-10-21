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

# Raw BBC World candidates
candidates = [
    ("US envoy arrives in Russia ahead of meeting with Putin Zelensky intelligence sharing", "https://www.bbc.co.uk/news/articles/cq5ynkx3xy11o", "world"),
    ("Trump and Zelensky appear at loggerheads despite Oslo optimism", "https://www.bbc.co.uk/news/articles/ckrey51jrgnro", "world"),
    ("France divided over riots", "https://www.bbc.co.uk/news/articles/cq0me4g9p970o", "world"),
    ("Elon Musk considering Tesla-SpaceX merger", "https://www.bbc.co.uk/news/articles/cmlyl09xjke4o", "world"),
    ("Pakistan arrests man hunted by US over postage fraud", "https://www.bbc.co.uk/news/articles/ckdd8m1z1z3yo", "world"),
    ("Sudan army drones hit mourners killing 300 people", "https://www.bbc.co.uk/news/articles/cr3el70jz1nqo", "world"),
    ("Alberta votes to stay in Canada Carney takes on Trump", "https://www.bbc.co.uk/news/articles/cr62ylj832vxo", "world"),
    ("Swimmer killed in shark attack South Africa", "https://www.bbc.co.uk/news/articles/cqx297pxg1djo", "world"),
    ("Trump sued over Canadian tariffs", "https://www.bbc.co.uk/news/articles/cqrkyj13m588o", "world"),
    ("North Korea publishes photos of Kim Jong Un", "https://www.bbc.co.uk/news/articles/cmvg6qv1jdydo", "world"),
    ("Tourist found guilty stealing Las Vegas flamingo", "https://www.bbc.co.uk/news/articles/cq398rjewd1jo", "world"),
    ("Suspect arrested after historic town hall set alight France", "https://www.bbc.co.uk/news/articles/cw5yn5e8mezvo", "world"),
    ("Kenya cult leader children still being starved", "https://www.bbc.co.uk/news/articles/c6d7q2rxqxgxo", "world"),
    ("Cornell Jane Doe university head doubted gang-rape allegation", "https://www.bbc.co.uk/news/articles/cwn73z5gnnrro", "world"),
    ("Mission blasts off for Mars to grab piece of moon", "https://www.bbc.co.uk/news/articles/cmvgxvkv54w1o", "world"),
    ("Violent clashes Albanian protesters and police", "https://www.bbc.co.uk/news/articles/cmy4xjlpqgd3o", "world"),
    ("Tennis Svitolina Ukraine war separation", "https://www.bbc.co.uk/news/articles/ckd7qy12j148o", "world"),
    ("Vinted blocks French looters listing stolen goods", "https://www.bbc.co.uk/news/articles/cm8xzrljv72ro", "world"),
    ("Ex-OpenAI worker accused of planting bug Saudi support", "https://www.bbc.co.uk/news/articles/c6gel2dlyxvyo", "world"),
    ("Exiled critic of Rwandan president found beheaded", "https://www.bbc.co.uk/news/articles/c3lylj78777do", "world"),
    ("Houthi missile strike Yemen camp kills 73", "https://www.bbc.co.uk/news/articles/cv0ld6lrr2zeo", "world"),
    ("Obama blasts federal probe of Ilhan Omar", "https://www.bbc.co.uk/news/articles/cr15jl7dd42vo", "world"),
    ("US airman dies daredevil descent Texas football", "https://www.bbc.co.uk/news/articles/crd6dn63j2xwo", "world"),
    ("Deadly fire Canada military base kilometre in 60 seconds", "https://www.bbc.co.uk/news/articles/ckj0ly6qnp1lo", "world"),
    ("Elon Musk says merging Tesla and SpaceX good idea", "https://www.bbc.co.uk/news/articles/cr93z1e87e0do", "world"),
    ("Haitian migrants changed US town Trump deportation", "https://www.bbc.co.uk/news/articles/crp3gvpek8njo", "world"),
    ("Trash Island golf course Trump legal dispute", "https://www.bbc.co.uk/news/articles/c6ly3dlm0dr2o", "world"),
    ("Borneo burning toxic haze", "https://www.bbc.co.uk/news/articles/cqm2dzwdmmywo", "world"),
    ("Is Ebola under control in Kenya", "https://www.bbc.co.uk/news/articles/c693z948px0jo", "world"),
    ("Australian court MP attack suspect silent hearing", "https://www.bbc.co.uk/news/videos/cq398rg0lnd1o", "world"),
    ("Clean up begins after French riots", "https://www.bbc.co.uk/news/videos/cwr7y0e57r50o", "world"),
    ("Ukraine drone airlift of wounded soldier", "https://www.bbc.co.uk/news/videos/c3vgx05p149wo", "world"),
    ("US church drug tranq battle", "https://www.bbc.co.uk/news/videos/cqd097z3epvno", "world"),
    ("Pope Leo XIV thanks wellwishers after cancer surgery", "https://www.bbc.co.uk/news/videos/cq70px6pjkg5o", "world"),
    ("Shops looted restaurants gutted Paris riots", "https://www.bbc.co.uk/news/videos/cmn5vey19q3go", "world"),
]

MED_BLOCK = ("medical", "poisoning", "disease", "treatment", "therapy", "diagnosis", "disorder", "surgery", "cancer", 
             "ebola", "epidemic", "virus", "infection", "patient", "clinical", "illness", "symptom")
POL_BLOCK = ("election", "politic", "court", "lawsuit", "war", "attack", "terror", "killed", "death toll", 
             "murder", "shooting", "bomb", "riot", "protest", "arrest", "charged", "beheaded", "drone", 
             "military", "tariff", "Putin", "Trump", "Zelensky", "Kim Jong", "Norway", "Ukraine", 
             "Sudan", "Alberta", "Canada", "Haitian", "immigration", "OpenAI", "federal probe", 
             "intelligence", "spying", "spying", "defence", "defense department", "OSINT")
VIOLENCE_BLOCK = ("killed", "death", "attack", "bomb", "shooting", "beheaded", "blood", "violent clash")

for title, url, lane in candidates:
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    dupes = []
    for fpath, content in all_content.items():
        tokens = [t for t in title.lower().split() if len(t) > 4]
        if len(tokens) > 0:
            matches = sum(1 for t in tokens if t in content)
            if matches >= 2:
                dupes.append(fpath)

    is_med = any(b in title.lower() for b in MED_BLOCK)
    is_pol = any(b in title.lower() for b in POL_BLOCK)
    is_violence = any(b in title.lower() for b in VIOLENCE_BLOCK)

    status = "FRESH"
    if dupes:
        status = "DUP"
    elif is_med:
        status = "MED-BLOCK"
    elif is_pol or is_violence:
        status = "POL-BLOCK"

    print(f"[{lane}] {status}: {title}")
    if dupes:
        for d in dupes:
            print(f"  -> dupe: {d}")
    print(f"  url: {url}")
    if status == "FRESH":
        print(f"  ** CANDIDATE **")
    print()

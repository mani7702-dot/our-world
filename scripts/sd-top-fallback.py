#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sd-top-fallback.py — ScienceDaily top.xml fallback for explainers lane.
Fetches top.xml via curl, strips trailing HTML comment after </rss>,
parses items, applies kid-safety + dedup filters.
"""
import subprocess, xml.etree.ElementTree as ET, re, os, sys, json

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
FEED = "https://www.sciencedaily.com/rss/top.xml"

BLOCK = ("war", "attack", "death toll", "killed", "murder", "court", "lawsuit",
         "covid", "pandemic", "election", "politic", "terror", "bomb", "shooting",
         "protest", "riot", "disaster", "climate change", "global warming",
         "disease", "cancer", "tumor", "carcinoma", "alzheimer", "dementia",
         "parkinson", "arthritis", "diabetes", "blood pressure", "cardiovascular",
         "ptsd", "ibd", "inflammatory bowel", "weight loss", "obesity",
         "supplement", "vitamin", "surgery", "cholesterol", "dental", "implant")

# Published-topic signatures to skip
PUBLISHED_SIGS = [
    "magnetic web", "hidden bias", "mirror life", "tiny snakes roll",
    "jurassic bird", "swiss glacier", "muscle robot", "fat switch",
    "brain messaging", "blood pressure ear", "chernobyl", "kikai",
    "dental implant", "ptsd", "parkinson", "inflammatory bowel",
    "quantum surprise", "quantum fourier", "viruses build", "cold atoms",
    "bird afraid", "big bang helium", "perseverance", "bennu", "jurassic squid",
    "marmoset brain", "brain alway predict", "why-do-we-yawn",
    "tongue eating louse", "ghostly eyeless", "cave snail", "stygofauna",
    "troblobite", "blue planet", "octopus escape", "humpback whale",
    "astronaut", "moon still shrinking", "valles marineris", "magnetic switchback",
    "milky way", "black hole", "x-ray", "weight loss drug", "skin science",
    "sleep muscle", "neu5gc", "lions Mmane", "peat fire", "silverpit",
    "spider crater", "van gogh", "venus slides", "virus self-assemble",
    "scorpion praearcturus", "glass recycling", "lube", "honey bee",
    "iguazu falls", "pupils space", "math geniuses", "moon base",
    "jessica watkins", "roman telescope", "sr25", "griffin moon",
    "flip rover", "tesla spacex", "ukraine starlink", "double starship",
    "dna typewriter", "molecule quantum", "sentinel 3c", "halloween skywatch",
    "hunters moon", "fin whale", "bronze whaler", "bukangi shark",
    "shark", "dog yellowstone", "lost dog", "texas boat", "magic mushroom",
    "mushroom", "sweetener", "marmoset", "soy", "yuezhuornis",
    "microscope", "laser microscope", "cell machinery",
    "muscle robot swims", "paper thin", "quantum", "carrington",
    "solar storm", "solar", "telescope", "webb", "mars", "moon",
    "asteroid", "supernova", "dark energy", "galaxy", "gravity",
    "black hole", "neutron star", "exoplanet", "climate",
    "brain", "aging brain", "memory wisdom",
]

EXPLAINERS_KW = ("how ", "why ", "what is", "does ", "can ", "how did", "how fast",
                 "how strong", "how hot", "how ancient", "why do", "why are",
                 "what makes", "how big", "how much", "how old", "how are",
                 "why is", "what is the", "science explained", "explained")

MEDICAL_BLOCK = ("cancer", "glioblastoma", "tumor", "carcinoma", "alzheimer",
                 "dementia", "parkinson", "arthritis", "diabetes", "blood pressure",
                 "cardiovascular", "ptsd", "ibd", "inflammatory bowel",
                 "weight loss", "obesity", "supine", "statin", "cholesterol",
                 "dental", "implant")

def fetch_top_xml():
    p = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-A", UA, FEED],
                       capture_output=True)
    data = p.stdout
    if data[:2] == b"\x1f\x8b":
        import gzip
        data = gzip.decompress(data)
    text = data.decode("utf-8", "replace")
    idx = text.find("</rss>")
    if idx != -1:
        text = text[:idx + len("</rss>")]
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text

def load_published_texts():
    chunks = []
    for d in ["content/news", "content/blog", "content/explainers", "content/world",
              "content/animals", "content/science"]:
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.endswith(".md"):
                with open(os.path.join(d, fn), encoding="utf-8", errors="replace") as f:
                    chunks.append(f.read().lower())
    return " ".join(chunks)

def classify(title_lower, desc_lower, big_text):
    hay = (title_lower + " " + desc_lower)
    for b in BLOCK:
        if b in hay:
            return "BLOCKED"
    for b in MEDICAL_BLOCK:
        if b in hay:
            return "MEDICAL"
    for sig in PUBLISHED_SIGS:
        if re.search(sig, hay):
            return "DUP"
    return "ok"

def main():
    text = fetch_top_xml()
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        print(f"# PARSE ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    big = load_published_texts()

    items = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        desc = (it.findtext("description") or "").strip()
        # strip HTML tags from desc
        desc = re.sub(r"<[^>]+>", "", desc).strip()[:300]
        if not title or len(title) < 20:
            continue
        tl = title.lower()
        dl = desc.lower()
        tag = classify(tl, dl, big)
        explainers_friendly = any(k in tl for k in EXPLAINERS_KW)
        items.append({"title": title, "url": link, "desc": desc,
                      "tag": tag, "flag": "" if explainers_friendly else " (not q-word)"})

    for r in items[:30]:
        print(json.dumps(r, ensure_ascii=False))
    print(f"# TOTAL: {len(items)} items", file=sys.stderr)

if __name__ == "__main__":
    main()

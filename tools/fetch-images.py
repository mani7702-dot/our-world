import io, os, re, json, time, subprocess, urllib.parse

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".gz", ".webm", ".ogg", ".ogv", ".pdf")
OK_MIME = ("image/jpeg", "image/png", "image/webp")
OK_LICENSE = ("public domain", "cc0", "cc by")
QUERY = {
    "bear-bread-farmers-market-aspen": "black bear",
    "bronze-whaler-shark-busan-canal": "bronze whaler shark",
    "cheetah-cub-cam-five-cubs": "cheetah cub",
    "manhattan-barn-owls-water-tower": "barn owl",
    "nasa-moon-base-cave-search": "moon",
    "orangutans-return-borneo-wild": "orangutan",
    "record-breaking-crayfish-tennessee": "crayfish",
    "roman-telescope-performs-better-than-expected": "Nancy Grace Roman Space Telescope",
    "roman-telescope-best-inventions-2026": "Roman Space Telescope",
    "webb-brown-dwarf-weather": "brown dwarf",
    "bleached-corals-recover-by-touching": "bleached coral",
    "mosasaurs-fast-sneaky-sea-hunters": "mosasaur fossil",
    "mmx-mars-phobos-sample": "Phobos",
    "how-does-a-compass-work": "compass",
    "forests-swallowing-methane-climate-shift": "forest floor leaf litter",
    "why-do-seeds-know-which-way-is-up": "plant seedling",
    "jersey-marine-reefs-protected-sea": "marine protected area Jersey",
    "colorado-wildlife-overpass-i25-collisions-down-91": "wildlife overpass",
    "coral-recovery-by-touch-stanford-7-weeks": "coral bleaching recovery",
    "green-star-white-dwarf-wdj1330-6435": "green star",
    "spacex-crs35-jellyfish-launch": "SpaceX Falcon 9 launch jellyfish",
    "masaya-volcano-hidden-magma": "Masaya volcano Nicaragua lava lake",
    "2026-10-20-sloth-bear-odum-julia-roberts-rescue": "sloth bear",
    "big-bang-helium-first-five-minutes": "Big Bang nucleosynthesis helium",
    "2026-10-20-belemnite-squid-jurassic-wyoming": "belemnite fossil Jurassic squid",
    "ancient-peruvian-hairless-dogs-wari-huarmey": "Peruvian hairless dog",
    "2026-10-20-mount-mabu-butterfly-forest-protected": "African butterfly",
    "bennu-boulders-hidden-cracks-osiris-rex": "asteroid Bennu OSIRIS-REx boulder",
    "nasa-simon-atmospheric-waves-above-hurricane": "atmospheric gravity waves hurricane satellite",
    "two-black-holes-hurtling-toward-cosmic-collision": "binary supermassive black hole galaxy jet",
    "mrk501-twin-black-holes-collide-100-years": "supermassive black hole galaxy jet",
    "webb-wasp-17b-lopsided-atmosphere": "exoplanet atmosphere",
    "2026-10-20-nasa-16-galaxies-cosmic-chaos": "galaxy Messier 82 Chandra X-ray",
    "dog-weighed-baby-hippo-sheds-pounds-rspca": "rescue dog",
    "brazil-ends-6-day-workweek-constitutional-amendment": "Brazilian National Congress",
    "amelia-earhart-taraia-object-trees": "Nikumaroro",
    "dianjunus-rex-giant-fungus-china": "Xylaria fungus stroma",
    "swimmer-turbine-tidal-power-scotland": "tidal power turbine",
    "jurassic-squid-beast-wyoteuthis-linsterorum-found": "belemnite fossil Jurassic squid",
    "jurassic-squid-butt-was-chunkiest-ever": "belemnite fossil Jurassic squid",
    "altermagnetism-third-magnetism-europhysics-prize": "altermagnetism magnetic crystal",
    "dussehra-india-good-over-evil": "Dussehra effigy burning India",
    "third-form-of-magnetism-altermagnetism-europhysics-prize": "altermagnetism magnetic crystal",
    "dussehra-festival-good-over-evil-celebrated-india": "Dussehra effigy burning India",
    "dussehra-effigies-india-good-over-evil": "Dussehra effigy burning India",
    "sgiath-sea-squirt-hunting-dog-animal-of-the-year": "Labrador retriever",
    "sea-vomit-detecting-dog-sgiath": "Labrador retriever",
    "aldabra-giant-tortoises-thrive-180000-survey": "Aldabra giant tortoise Seychelles",
    "2026-10-20-wfp-cuts-gaza-food-aid-funding-shortfall": "World Food Programme food distribution",
    "musk-tesla-spacex-merger-considered": "Tesla Model S electric car",
    "tourist-guilty-stolen-las-vegas-flamingo": "Chilean flamingo",
    "alaska-tracy-arm-landslide-tsunami-1580-feet": "Alaska landslide tsunami Tracy Arm fjord",
    "alaska-landslide-tsunami-tracy-arm-1580-feet": "Alaska landslide tsunami Tracy Arm fjord",
    "molecule-quantum-fourier-limit-surface": "crystal surface microscopy",
    "dinosaur-antarctica-fossil-drawer-titanosaur": "Titanosaur vertebra fossil",
    "nightjar-migration-wings-sacrifice-efficiency": "European nightjar (Caprimulgus europaeus) flying",
    "el-nino-alters-weather-patterns-around-world": "El Nino Pacific Ocean satellite",
    "hurricane-simon-atmospheric-waves-nasa": "atmospheric gravity waves hurricane satellite",
    "williston-lake-floating-forest-canada": "floating forest",
    "quantum-limit-molecules-surface-science": "scanning tunneling microscope molecule",
    "quantum-highway-one-atom-superconductor": "superconductor quantum vortex",
    "2026-10-20-strange-surprising-lakes-around-world": "Lake Natron Tanzania flamingo pink",
    "cold-atoms-fractional-fermi-sea-new-quantum-state": "ultracold atom cloud magnetic trap",
    "uranium-cubes-nazi-nuclear-failure": "Haigerloch uranium cubes",
    "free-roaming-bison-american-prairie-1016": "Bison prairie Montana",
    "10-weird-lakes-nature-gets-strange": "Lake Natron flamingo pink",
    "2026-10-20-chandra-16-galaxies-galactic-gallery": "Chandra X-ray galaxy Messier 82",
    "10-times-animals-surprised-scientists": "orcas pilot whales",
    "10-sunken-villages-that-reappear": "submerged ruins",
    "movie-antagonists-who-deserved-sympathy": "movie villain character portrait",
    "10-wild-facts-about-bears": "brown bear",
    "history-made-up-facts": "historical manuscripts and artifacts",
    "sitcoms-launch-biggest-music-careers-century": "television studio recording microphone singer",
    "musicians-who-resent-their-biggest-hits": "singer microphone stage spotlight",
    "strawberry-soil-steam-cleanse-crop": "strawberry plant",
    "nobel-prize-optogenetics-brain-light-2026": "optogenetics neuron laser illumination microscopy",
    "magic-mushroom-compound-calms-aggressive-fish": "psilocybin mushroom",
    "pilot-whales-chase-orcas-mobbing": "orcas pilot whales",
    "sphinx-crocodile-skull-herugavialis-cairensis": "gharial fossil skull",
    "wasp-17b-lopsided-atmosphere-webb-telescope": "WASP-17b exoplanet artist impression",
    "japan-kikai-akahoya-volcanic-apocalypse-populations": "Kikai caldera eruption",
    "borneo-fires-peat-smoke-haze-science": "peat swamp fire Indonesia Borneo smoke",
    "worlds-oldest-shipwreck-kekova-turkey-amphorae": "ancient Greek amphora Bronze Age",
    "hurricane-warning-maps-improving": "hurricane forecast cone National Hurricane Center",
    "antarctica-sea-ice-third-lowest-2026": "Antarctic sea ice",
    "red-squirrels-thrive-jersey-england-refuge": "red squirrel UK",
    "canadian-tourist-stole-las-vegas-flamingo-convicted-animal-cruelty": "Chilean flamingo",
}

def ok_license(l):
    l = l.lower()
    return any(k in l for k in OK_LICENSE) and "nc" not in l and "nd" not in l


def curl_json(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for _ in range(3):
        p = subprocess.run(["curl", "-s", "--compressed", "--max-time", "30", "-A", UA, url],
                           capture_output=True, text=True)
        out = p.stdout.strip()
        if not out:
            time.sleep(8)
            continue
        try:
            d = json.loads(out)
            if "error" in d and "429" in str(d.get("error", {})):
                time.sleep(25)
                continue
            return d
        except Exception:
            time.sleep(8)
    return None


def down(url):
    return subprocess.run(["curl", "-s", "--compressed", "--max-time", "45", "-A", UA, url],
                          capture_output=True).stdout

hits = 0
for dirpath, _, files in os.walk("content"):
    for fn in files:
        if not fn.endswith(".md"):
            continue
        slug = fn[:-3]
        if slug not in QUERY:
            continue
        fp = os.path.join(dirpath, fn)
        t = io.open(fp, encoding="utf-8").read()
        if re.search(r"^image:", t, re.M):
            continue
        print("QUERY", QUERY[slug])
        data = curl_json({"action": "query", "format": "json", "generator": "search",
                          "gsrsearch": "file:" + QUERY[slug], "gsrnamespace": "6", "gsrlimit": "15",
                          "prop": "imageinfo", "iiprop": "url|mime|extmetadata", "iiurlwidth": "1200"})
        time.sleep(6)
        if not data:
            print("  GIVE UP", slug)
            continue
        pages = (data.get("query", {}) or {}).get("pages", {}) or {}
        chosen = None
        for pid, pg in pages.items():
            ii = (pg.get("imageinfo") or [{}])[0]
            mime = ii.get("mime", "")
            url = ii.get("thumburl") or ii.get("url", "")
            meta = ii.get("extmetadata", {}) or {}
            lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
            if mime not in OK_MIME:
                continue
            if any(url.lower().endswith(b) for b in BAD_EXT):
                continue
            if not ok_license(lic):
                continue
            chosen = (url, mime, lic)
            break
        if not chosen:
            print("  NO usable image for", slug)
            continue
        url, mime, lic = chosen
        ext = "jpg" if mime.endswith("jpeg") else "png" if mime.endswith("png") else "webp"
        out = os.path.join("assets/images", slug + "." + ext)
        img = down(url)
        if not img:
            print("  ERR download", slug)
            continue
        io.open(out, "wb").write(img)
        t2 = re.sub(r"^(time:\s*\S+)$", r"\1\nimage: " + out.replace("\\", "/") + "\nimage_caption: Photo: Wikimedia Commons",
                    t, count=1, flags=re.M)
        io.open(fp, "w", encoding="utf-8", newline="").write(t2)
        hits += 1
        print("  OK", out, len(img), lic)
print("FETCHED:", hits)

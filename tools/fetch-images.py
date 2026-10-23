import io, os, re, json, time, subprocess, urllib.parse

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".gz", ".webm", ".ogg", ".ogv", ".pdf")
OK_MIME = ("image/jpeg", "image/png", "image/webp")
OK_LICENSE = ("public domain", "cc0", "cc by")
QUERY = {
    "indonesia-halts-deforestation-saving-4-million-acres": "orangutan Borneo rainforest",
    "2026-10-22-honey-bees-bullying-wild-pollinators": "honey bee on flower bumble bee pollinator",
    "2026-10-22-venus-slides-past-sun": "Venus planet from space NASA Solar System",
    "2026-10-22-weight-loss-drugs-skin-science": "human skin collagen fiber structure microscopic diagram",
    "2026-10-22-spider-crater-wa-space-image": "Spider Crater Western Australia impact structure Landsat",
    "massive-asteroid-north-sea-tsunami-silverpit-crater": "asteroid impact crater",
    "how-does-exercise-keep-muscles-young": "human muscle tissue",
    "bear-bread-farmers-market-aspen": "black bear",
    "bronze-whaler-shark-busan-canal": "bronze whaler shark",
    "cheetah-cub-cam-five-cubs": "cheetah cub",
    "manhattan-barn-owls-water-tower": "barn owl",
    "nightjar-wings-trade-off-long-distance-migration": "European nightjar flying",
    "nasa-moon-base-cave-search": "moon",
    "orangutans-return-borneo-wild": "orangutan",
    "record-breaking-crayfish-tennessee": "crayfish",
    "roman-telescope-performs-better-than-expected": "Nancy Grace Roman Space Telescope",
    "roman-telescope-best-inventions-2026": "Roman Space Telescope",
    "nasa-roman-telescope-exceeds-expectations": "space telescope",
    "webb-brown-dwarf-weather": "brown dwarf",
    "bleached-corals-recover-by-touching": "bleached coral",
    "coral-reef-recovery-by-touch-stanford": "coral reef bleaching recovery Acropora",
    "mosasaurs-fast-sneaky-sea-hunters": "mosasaur fossil",
    "mmx-mars-phobos-sample": "Phobos",
    "japan-mmx-mars-phobos-sample-mission-launches": "Phobos Mars moon",
    "how-does-a-compass-work": "compass",
    "soy-salt-brain-compound": "soybeans",
    "forests-swallowing-methane-climate-shift": "forest floor leaf litter",
    "why-do-seeds-know-which-way-is-up": "plant seedling",
    "jersey-marine-reefs-protected-sea": "marine protected area Jersey",
    "colorado-wildlife-overpass-i25-collisions-down-91": "wildlife overpass",
    "wildlife-overpass-i25-collisions-down-91": "wildlife overpass bridge Colorado",
    "fin-whale-lunge-feeding-pembrokeshire": "fin whale lunge feeding",
    "coral-recovery-by-touch-stanford-7-weeks": "coral bleaching recovery",
    "green-star-white-dwarf-wdj1330-6435": "green star white dwarf artist impression",
    "ghostly-green-star-white-dwarf": "green star white dwarf artist impression",
    "spacex-crs35-jellyfish-launch": "SpaceX Falcon 9 launch jellyfish",
    "spacex-iss-strange-cargo-2026": "SpaceX Dragon cargo International Space Station",
    "masaya-volcano-hidden-magma": "Masaya volcano Nicaragua lava lake",
    "2026-10-20-sloth-bear-odum-julia-roberts-rescue": "sloth bear",
    "2026-10-22-acrylic-glass-recycling-eth-zurich": "acrylic glass plastic sheet",
    "big-bang-helium-first-five-minutes": "Big Bang nucleosynthesis helium",
    "2026-10-20-belemnite-squid-jurassic-wyoming": "belemnite fossil Jurassic squid",
    "ancient-peruvian-hairless-dogs-wari-huarmey": "Peruvian hairless dog",
    "2026-10-20-mount-mabu-butterfly-forest-protected": "African butterfly",
    "2026-10-23-2027-eclipse-egypt-temples": "total solar eclipse corona",
    "mozambique-mount-mabu-butterfly-forest-protected": "Mozambique butterfly",
    "bennu-boulders-hidden-cracks-osiris-rex": "asteroid Bennu OSIRIS-REx boulder",
    "nasa-simon-atmospheric-waves-above-hurricane": "atmospheric gravity waves hurricane satellite",
    "two-black-holes-hurtling-toward-cosmic-collision": "binary supermassive black hole galaxy jet",
    "mrk501-twin-black-holes-collide-100-years": "supermassive black hole galaxy jet",
    "hamburger-galaxy-ngc3628-edge-on-spiral": "NGC 3628 Hamburger Galaxy edge-on spiral",
    "webb-wasp-17b-lopsided-atmosphere": "exoplanet atmosphere",
    "2026-10-20-nasa-16-galaxies-cosmic-chaos": "galaxy Messier 82 Chandra X-ray",
    "dog-weighed-baby-hippo-sheds-pounds-rspca": "rescue dog",
    "brazil-ends-6-day-workweek-constitutional-amendment": "Brazilian National Congress",
    "amelia-earhart-taraia-object-trees": "Nikumaroro",
    "2026-10-20-dianjunus-rex-giant-fungus-china": "Xylaria fungus stroma",
    "d-rex-giant-fungus-king-of-dian-china": "Xylaria polymorpha dead man fingers",
    "swimmer-turbine-tidal-power-scotland": "tidal power turbine",
    "jurassic-squid-beast-wyoteuthis-linsterorum-found": "belemnite fossil Jurassic squid",
    "sr1-freedom-nuclear-spaceship-mars": "nuclear reactor space satellite",
    "jurassic-squid-butt-was-chunkiest-ever": "belemnite fossil Jurassic squid",
    "altermagnetism-third-magnetism-europhysics-prize": "altermagnetism magnetic crystal",
    "dussehra-india-good-over-evil": "Dussehra effigy burning India",
    "third-form-of-magnetism-altermagnetism-europhysics-prize": "altermagnetism magnetic crystal",
    "dussehra-festival-good-over-evil-celebrated-india": "Dussehra effigy burning India",
    "dussehra-effigies-india-good-over-evil": "Dussehra effigy burning India",
    "sgiath-sea-squirt-hunting-dog-animal-of-the-year": "Labrador retriever",
    "sea-vomit-detecting-dog-sgiath": "Labrador retriever",
    "aldebra-giant-tortoises-thrive-180000-survey": "Aldabra giant tortoise Seychelles",
    "math-geniuses-built-modern-world": "mathematical equation formula",
    "2026-10-20-wfp-cuts-gaza-food-aid-funding-shortfall": "World Food Programme food distribution",
    "2026-10-23-solar-orbiter-traces-magnetic-switchbacks-to-sun": "Solar Orbiter solar wind magnetic field switchback S-shaped",
    "musk-tesla-spacex-merger-considered": "Tesla Model S electric car",
    "tourist-guilty-stolen-las-vegas-flamingo": "Chilean flamingo",
    "alaska-tracy-arm-landslide-tsunami-1580-feet": "Alaska landslide tsunami Tracy Arm fjord",
    "nasa-amazon-fires-hidden-beneath-rainforest": "Amazon rainforest wildfire satellite infrared",
    "alaska-landslide-tsunami-tracy-arm-1580-feet": "Alaska landslide tsunami Tracy Arm fjord",
    "webb-stellar-jets-ngc7129-nebula": "NGC 7129 nebula James Webb stellar jets",
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
    "doomsday-prediction-1960-2026-failed-population-explosion": "population growth chart 1960s",
    "free-roaming-bison-american-prairie-1016": "Bison prairie Montana",
    "10-weird-lakes-nature-gets-strange": "Lake Natron flamingo pink",
    "2026-10-20-chandra-16-galaxies-galactic-gallery": "Chandra X-ray galaxy Messier 82",
    "10-times-animals-surprised-scientists": "orcas pilot whales",
    "10-sunken-villages-that-reappear": "submerged ruins",
    "movie-antagonists-who-deserved-sympathy": "movie villain character portrait",
    "10-wild-facts-about-bears": "brown bear",
    "sweeteners-gut-microbes-lab-test-39": "gut microbiome bacteria",
    "sitcoms-launch-biggest-music-careers-century": "television studio recording microphone singer",
    "musicians-who-resent-their-biggest-hits": "singer microphone stage spotlight",
    "astronaut-tim-peake-surprise-video-plymouth-school": "Tim Peake space suit astronaut",
    "strawberry-soil-steam-cleanse-crop": "strawberry plant",
    "nobel-prize-optogenetics-brain-light-2026": "optogenetics neuron laser illumination microscopy",
    "magic-mushroom-compound-calms-aggressive-fish": "psilocybin mushroom",
    "pilot-whales-chase-orcas-mobbing": "orcas pilot whales",
    "sphinx-crocodile-skull-herugavialis-cairensis": "gharial fossil skull",
    "texas-man-builds-62-foot-boat-since-1987": "steel fishing boat",
    "wasp-17b-lopsided-atmosphere-webb-telescope": "WASP-17b exoplanet artist impression",
    "japan-kikai-akahoya-volcanic-apocalypse-populations": "Kikai caldera eruption",
    "borneo-fires-peat-smoke-haze-science": "peat swamp fire Indonesia Borneo smoke",
    "why-are-peat-fires-so-bad": "peat swamp fire Indonesia smoke haze",
    "2026-10-22-peat-fires-indonesia-dangerous": "Indonesian forest fire peat swamp burning",
    "worlds-oldest-shipwreck-kekova-turkey-amphorae": "ancient Greek amphora Bronze Age",
    "us-green-card-wait-what-indians-are-facing": "world map showing country connections people migration",
    "hurricane-warning-maps-improving": "hurricane forecast cone National Hurricane Center",
    "antarctica-sea-ice-third-lowest-2026": "Antarctic sea ice",
    "rna-overload-starves-cells-of-energy": "cellular respiration mitochondria ATP",
    "blueberries-mood-gut-brain-link": "wild blueberries on bush",
    "red-squirrels-thrive-jersey-england-refuge": "red squirrel UK",
    "canadian-tourist-stole-las-vegas-flamingo-convicted-animal-cruelty": "Chilean flamingo",
    "canada-military-base-fire-alberta-wind-spread": "Canadian military parade ground",
    "jwst-orion-stellar-nursery-omc2": "Orion Nebula JWST infrared protostar",
    "nightjar-upstroke-thrust-long-distance-flight": "Caprimulgus europaeus",
    "capybara-pups-manx-wetlands": "capybara",
    "chiron-first-centaur-discovered-1977": "2060 Chiron",
    "cleaning-air-lifts-aerosol-cooling-unmasks-warming": "coal power plant",
    "windermere-sewage-cleanup-tunnel": "Windermere Lake District England",
    "el-nino-global-weather-impacts": "Pacific Ocean storm satellite weather",
    "how-does-sleep-build-muscle-burn-fat-brain": "hypothalamus brain neurons",
    "sleep-growth-hormone-brain-circuit": "neurons synapse illustration",
    "tree-thirsty-berlin-app": "Berlin street tree watering app",
    "arctic-sea-ice-satellite-record-low-2026": "Arctic sea ice satellite",
    "italian-biomethane-plant-turns-farm-waste-into-clean-gas": "biomethane plant Italy agricultural waste",
    "wimpole-estate-5242-species-despite-drought": "great crested newt",
    "farmer-lost-sfi26-wildlife-funding": "barn owl",
    "wasps-nest-took-over-wildlife-office-norfolk": "paper wasp nest",
    "david-bushnell-turtle-secret-submarine-1776": "David Bushnell Turtle submarine",
    "aging-brain-memory-meaning": "brain anatomy diagram hippocampus",
    "roman-temple-germany-frankfurt-limes": "Roman limes archaeological site Germany",
    "mars-helicopter-blade-designs-18km-flight": "Ingenuity Mars helicopter rotor",
    "stanford-microscope-seeing-living-cells": "optical microscopy biological cell",
    "stanford-microscope-seeing-cells-without-labels": "optical microscopy biological cell",
    "moon-base-rover-progress-update-nasa": "lunar rover moon surface",
    "river-taff-fuel-leak-kills-fish": "river pollution foam",
    "six-ways-magic-protected-homes-from-witch-bottles-to-symbols": "witch bottle",
    "ghostly-eyeless-cave-snail-china": "freshwater gastropod cave",
    "lost-dog-survived-month-yellowstone-luna": "Jack Russell terrier",
    "ultra-processed-food-colorectal-cancer-study": "epidemiology study researcher analyzing questionnaire data",
    "neu5gc-red-meat-sugar-diabetes-link": "beef butcher shop raw meat",
    "perseverance-mars-rover-driving-record": "Perseverance rover Mars surface",
    "astronauts-hearts-mars-spaceflight-test": "astronaut exercise ISS treadmill",
    "atlantic-current-amoc-climate-weather": "Gulf Stream ocean current satellite sea surface temperature",
    "silverpit-crater-asteroid-tsunami": "Silverpit Crater",
    "nasa-farmflux-low-altitude-flights-amarillo-texas": "agricultural aircraft flying low over farmland",
    "kew-palm-house-plant-relocation-2027": "Kew Palm House glasshouse",
    "uzbekistan-77th-artemis-accords-signatory": "Artemis Accords space cooperation",
    "skin-cells-play-different-rules-boys-vs-girls-mice-study": "skin stem cell biological sex",
    "sentinel-3c-satellite-first-images-italy-arctic": "Earth observation satellite",
    "why-universe-laws-tuned-for-life-water-flow": "water droplet viscosity macro",
    "casals-lidar-earth-3d-maps": "space lidar instrument",
    "oldest-wing-walker-99-helga-duffy": "biplane",
    "daily-4-minute-strength-after-65": "human muscle exercise fitness",
    "why-do-tropical-trees-breathe-at-night": "CAM photosynthesis tropical tree",
    "reverse-cellular-aging-epigenetic-clock-60-years": "DNA methylation cell",
    "jpl-90th-anniversary-future-missions": "Jet Propulsion Laboratory Pasadena rocket",
    "pupils-space-badge-meet-astronaut-rubio": "International Space Station school lesson astronaut",
    "eclipse-predictors-chinese-astronomers": "total solar eclipse",
    "perseverance-autonav-road-to-mars-record": "Mars rover Perseverance driving",
    "sherlock-holmes-joseph-bell-real-surgeon": "Sidney Paget Sherlock Holmes",
    "cumbria-uplands-lab-nature-recovery-science": "English Lake District",
    "cumbria-uplands-lab-studies-peat-carbon": "Lake District peat bog",
    "rs25-engine-test-artemis-moon-rocket": "NASA RS-25 rocket engine test fire",
    "kitten-stuck-car-engine-sandy-springs": "kitten cat",
    "jessica-watkins-iss-science-kibo": "International Space Station Kibo laboratory module interior",
    "japan-nagoya-asian-games-accommodation-chaos": "Japanese athlete Olympic village",
    "ten-diets-slower-biological-aging": "fruits and vegetables healthy food",
    "extratropical-cyclone-iceland-isaias": "Classic Comma Mid-Latitude Cyclone",
    "how-did-america-get-its-name": "1776 Declaration of Independence parchment signing",
    "storm-austen-uk-severe-gales": "isobars weather map storm",
    "plant-armor-strawberry-fabric-triples-yields": "strawberry plant",
    "jwst-orion-stellar-nursery-protostars": "JWST Orion Nebula infrared protostars",
    "how-queen-caroline-used-king-arthur": "King Arthur medieval manuscript illustration",
    "why-do-cave-paintings-seem-to-move-in-torchlight": "Lascaux cave painting bison",
    "nasa-football-flyover-inspiration-tour": "NASA F-5 flyover",
    "uk-extreme-heat-air-conditioning": "urban heat island city street",
    "new-guinea-drought-fires-el-nino": "New Guinea wildfire satellite smoke",
    "judi-dench-legend-of-m": "Judi Dench portrait",
    "anticrepuscular-rainbow-fan": "anticrepuscular rays rainbow sunset",
    "who-wrote-elizabeth-i-letters": "Elizabeth I Darnley portrait",
    "elwha-river-tribe-salmon-1100-acres-restored": "Chinook salmon spawning",
    "2026-10-22-moon-still-shrinking-cools": "Moon surface cliff fault scarp lobate thrust fault Lunar Reconnaissance Orbiter",
    "new-penguin-species-kerguelen-islands-genetics": "Gentoo penguin swimming",
    "why-does-your-brain-always-predict-everything": "neurons brain illustration drawing",
    "2026-10-22-octopus-dna-fold-intelligence": "octopus intelligence brain neurons",
    "period-drama-details-historically-accurate": "period drama Regency era costume historical artifacts",
    "2026-10-22-meta-fined-25b-data-privacy": "computer server data center racks",
    "uk-jackdaw-gas-field-what-is-it": "North Sea gas platform jackdaw bird",
    "samoa-island-wildlife-recovery-after-rat-pig-removal": "native bird",
    "zoo-lion-feeding-wild-behavior-carcass-study": "African lion eating meat",
    "airbnb-hosts-no-longer-ask-guests-to-clean": "cleaning supplies sponge and cloth",
    "solar-orbiter-switchback-traced-to-sun": "Solar Orbiter spacecraft solar wind magnetic field switchback",
    "2026-10-22-curiosity-rover-mars-mystery-cliffs": "Mars rover Curiosity Mastcam panorama Mount Sharp yardang",
    "2026-10-22-silverpit-asteroid-crater-north-sea": "Silverpit Crater",
    "2026-10-22-mars-arsia-mons-mysterious-cloud": "Arsia Mons Mars cloud",
    "2026-10-22-hailstone-science-explainer": "hailstones on ground",
    "2026-10-22-virus-particles-self-assemble-without-a-blueprint": "virus capsid protein self-assembly microscopic",
    "2026-10-22-why-marmoset-brains-are-smooth": "common marmoset monkey Callithrix jacchus",
    "2026-10-22-how-did-a-rock-travel-90-km-into-earth": "subduction zone cross section Earth mantle eclogite",
    "ai-found-php-security-flaw-internet": "data center computer server rack illuminated",
    "2026-10-22-giant-scorpion-praearcturus-gigas": "fossil scorpion Praearcturus",
    "2026-10-22-iguazu-falls-super-el-nino-near-record-flows": "Iguazu Falls waterfall Argentina Brazil",
    "2026-10-22-van-gogh-starry-night-real-sky": "Van Gogh The Starry Night 1889 painting Saint-Remy sky",
    "2026-10-22-earth-oxygen-phosphorus-cycle-habitability": "cyanobacteria stromatolite rock",
    "2026-10-23-coconut-oil-jet-fuel": "coconut oil biofuel jet engine laboratory experiment",
    "starbucks-china-purchase-to-sit-policy": "Starbucks coffee shop interior China",
    "hubble-roman-gravitational-lenses": "gravitational lens galaxy Hubble Space Telescope arc",
    "2026-10-22-vasuki-indicus-giant-prehistoric-snake-india": "prehistoric snake fossil skeleton",
    "2026-10-22-milky-way-disk-two-stage-settling-gaia": "Milky Way galaxy disk spiral arms stars Gaia satellite",
    "2026-10-23-shark-hears-250-feet-underwater-sound": "blacktip shark Carcharhinus limbatus swimming ocean",
    "2026-10-23-teesdale-arctic-alpine-plants-seeds-fells": "arctic-alpine wildflowers Teesdale Spring Gentian Bird's-eye primrose",
    "rubin-observatory-test-camera-seagull-nebula": "Seagull Nebula IC 2177 ESO",
    "2026-10-23-webb-ngc-7129-stellar-nursery": "NGC 7129 nebula James Webb stellar jets",
    "2026-10-22-mit-black-hole-xray-reverberation": "supermassive black hole accretion disk coronagrapher X-ray Chandra",
    "soy-compound-salt-brain-health-mice": "soybeans in pod",
    "2026-10-23-euclid-discovers-comet-c2026-s1": "Euclid space telescope comet C/2026 S1",
    "2026-10-23-recoiling-black-holes-pendulum-evidence": "supermassive black hole merger gravitational wave kick artist impression",
    "2026-10-23-exploding-stars-dark-energy-changing": "Type Ia supernova exploding star white dwarf standard candle",
    "2026-10-23-supernova-explosions-first-aided-then-later-impeded-epoch-of-reionization": "Hubble Deep Field galaxies gravitational lensing",
    "mother-bats-hearts-babies-cries": "Japanese house bat mother pup echolocation cave roost",
    "2026-10-23-grid-operator-lights-winter-supply": "electricity transmission towers substation",
    "2026-10-23-how-citizen-science-tracks-shoreline-changes": "beach sand shoreline coast",
    "2026-10-23-neutrinos-matter-asymmetry-key": "neutrino detector tank water Cherenkov",
}

def ok_license(l):
    l = l.lower()
    return any(k in l for k in OK_LICENSE) and "nc" not in l and "nd" not in l


def curl_json(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for _ in range(3):
        p = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url],
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
    return subprocess.run(["curl", "-s", "--max-time", "45", "-A", UA, url],
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

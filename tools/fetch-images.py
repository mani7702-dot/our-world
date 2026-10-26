import io, os, re, json, time, subprocess, urllib.parse

API = "https://commons.wikimedia.org/w/api.php"
UA = "OurWorldSite/1.0 (contact: andugulamani722@gmail.com)"
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".gz", ".webm", ".ogg", ".ogv", ".pdf")
OK_MIME = ("image/jpeg", "image/png", "image/webp")
OK_LICENSE = ("public domain", "cc0", "cc by")
QUERY = {
    "2026-10-26-could-satellite-deorbit-bonds-prevent-space-junk-disaster": "space debris satellite orbital junk low earth orbit Kessler syndrome artist concept",
    "2026-10-25-antarctic-postmaster-penguins": "Port Lockroy Antarctic post office gentoo penguin historic hut",
    "2026-10-25-brown-bears-bu-tyapa-rescued-to-ireland-sanctuary": "brown bear walking forest Ireland Donegal wildlife sanctuary Wild Ireland",
    "2026-10-26-three-black-holes-dawn-of-time": "supermassive black hole galaxy JWST James Webb telescope artist impression",
    "2026-10-24-nasa-wildflower-bloom-australia-outback": "wildflower desert Australia Landsat bloom",
    "2026-10-25-seabirds-isle-of-man-biosphere-conservation": "Manx shearwater burrow seabird cliff coastline",
    "2026-10-24-rewilded-gorilla-lulingu-birth-virunga": "eastern lowland gorilla infant Virunga national park",
    "2026-10-24-suns-hidden-magnetic-web": "Sunrise-III balloon telescope solar chromosphere magnetic canopy thread-like magnetic field lines Sun",
    "2026-10-24-nasa-artemis-3-moon-lander-test": "NASA Orion spacecraft approaching International Space Station concept Artemis",
    "2026-10-26-nasa-lunar-lander-race-moon": "SpaceX Starship lunar lander concept NASA Blue Origin Blue Moon Moon landing",
    "2026-10-24-eagles-nest-fire-bavaria": "Eagle's Nest Kehlsteinhaus Berchtesgaden mountain building",
    "private-griffin-moon-lander-gets-put-to-the-test": "Griffin-1 lunar lander NASA JPL space simulator testing",
    "fish-oil-brain-health-no-benefit-study": "omega-3 DHA molecule structure fish oil capsule",
    "2026-10-23-blue-planet-iii-octopus-escape": "octopus swimming colour change camouflage",
    "indonesia-halts-deforestation-saving-4-million-acres": "orangutan Borneo rainforest",
    "2026-10-22-honey-bees-bullying-wild-pollinators": "honey bee on flower bumble bee pollinator",
    "2026-10-22-venus-slides-past-sun": "Venus planet from space NASA Solar System",
    "2026-10-22-weight-loss-drugs-skin-science": "human skin collagen fiber structure microscopic diagram",
    "2026-10-22-spider-crater-wa-space-image": "Spider Crater Western Australia impact structure Landsat",
    "humpback-whale-mourned-stillborn-calf": "humpback whale mother calf Australia ocean",
    "massive-asteroid-north-sea-tsunami-silverpit-crater": "asteroid impact crater",
    "how-does-exercise-keep-muscles-young": "human muscle tissue",
    "bear-bread-farmers-market-aspen": "black bear",
    "bronze-whaler-shark-busan-canal": "bronze whaler shark",
    "cheetah-cub-cam-five-cubs": "cheetah cub",
    "manhattan-barn-owls-water-tower": "barn owl",
    "2026-10-25-narwhal-tusk-double-helix": "narwhal tusk Arctic whale",
    "nightjar-wings-trade-off-long-distance-migration": "European nightjar flying",
    "nasa-moon-base-cave-search": "moon",
    "orangutans-return-borneo-wild": "orangutan",
    "record-breaking-crayfish-tennessee": "crayfish",
    "roman-telescope-performs-better-than-expected": "Nancy Grace Roman Space Telescope",
    "roman-telescope-best-inventions-2026": "Roman Space Telescope",
    "nasa-roman-telescope-exceeds-expectations": "space telescope",
    "webb-brown-dwarf-weather": "brown dwarf",
    "2026-10-19-brown-dwarfs-spherex-goth-atmospheres": "brown dwarf artist impression NASA SPHEREx telescope space infrared spectrum",
    "bleached-corals-recover-by-touching": "bleached coral",
    "coral-reef-recovery-by-touch-stanford": "coral reef bleaching recovery Acropora",
    "mosasaurs-fast-sneaky-sea-hunters": "mosasaur fossil",
    "mmx-mars-phobos-sample": "Phobos",
    "japan-mmx-mars-phobos-sample-mission-launches": "Phobos Mars moon",
    "japan-mars-moon-samples": "Phobos Mars moon spacecraft MMX",
    "how-does-a-compass-work": "compass",
    "soy-salt-brain-compound": "soybeans",
    "forests-swallowing-methane-climate-shift": "forest floor leaf litter",
    "why-do-seeds-know-which-way-is-up": "plant seedling",
    "jersey-marine-reefs-protected-sea": "marine protected area Jersey",
    "2026-10-26-wildlife-overpass-i25-collisions": "wildlife overpass Colorado Interstate 25 bridge Banff elk deer pronghorn wildlife crossing",
    "wildlife-overpass-i25-collisions-down-91": "wildlife overpass bridge Colorado",
    "fin-whale-lunge-feeding-pembrokeshire": "fin whale lunge feeding",
    "coral-recovery-by-touch-stanford-7-weeks": "coral bleaching recovery",
    "green-star-white-dwarf-wdj1330-6435": "green star white dwarf artist impression",
    "ghostly-green-star-white-dwarf": "green star white dwarf artist impression",
    "2026-10-24-spacex-double-starship-catch": "SpaceX Starship chopstick tower catch Super Heavy booster upper stage",
    "spacex-crs35-jellyfish-launch": "SpaceX Falcon 9 launch jellyfish",
    "spacex-iss-strange-cargo-2026": "SpaceX Dragon cargo International Space Station",
    "masaya-volcano-hidden-magma": "Masaya volcano Nicaragua lava lake",
    "2026-10-25-amazon-forest-protection-strategies": "Amazon rainforest canopy aerial NASA satellite view",
    "2026-10-20-sloth-bear-odum-julia-roberts-rescue": "sloth bear",
    "2026-10-22-acrylic-glass-recycling-eth-zurich": "acrylic glass plastic sheet",
    "big-bang-helium-first-five-minutes": "Big Bang nucleosynthesis helium",
    "2026-10-20-belemnite-squid-jurassic-wyoming": "belemnite fossil Jurassic squid",
    "ancient-peruvian-hairless-dogs-wari-huarmey": "Peruvian hairless dog",
    "2026-10-20-mount-mabu-butterfly-forest-protected": "African butterfly",
    "2026-10-23-lazuli-space-telescope-27-exoplanet-targets": "Lazuli Space Telescope exoplanet coronagraph artist impression",
    "2026-10-23-2027-eclipse-egypt-temples": "total solar eclipse corona ancient Egyptian temple",
    "mozambique-mount-mabu-butterfly-forest-protected": "Mozambique butterfly",
    "bennu-boulders-hidden-cracks-osiris-rex": "asteroid Bennu OSIRIS-REx boulder",
    "nasa-simon-atmospheric-waves-above-hurricane": "atmospheric gravity waves hurricane satellite",
    "two-black-holes-hurtling-toward-cosmic-collision": "binary supermassive black hole galaxy jet",
    "mrk501-twin-black-holes-collide-100-years": "supermassive black hole galaxy jet",
    "hamburger-galaxy-ngc3628-edge-on-spiral": "NGC 3628 Hamburger Galaxy edge-on spiral",
    "webb-wasp-17b-lopsided-atmosphere": "exoplanet atmosphere",
    "2026-10-20-nasa-16-galaxies-cosmic-chaos": "galaxy Messier 82 Chandra X-ray",
    "walrus-calf-annautaq-rescue": "Pacific walrus calf",
    "dog-weighed-baby-hippo-sheds-pounds-rspca": "rescue dog",
    "brazil-ends-6-day-workweek-constitutional-amendment": "Brazilian National Congress",
    "amelia-earhart-taraia-object-trees": "Nikumaroro",
    "2026-10-20-dianjunus-rex-giant-fungus-china": "Xylaria fungus stroma",
    "d-rex-giant-fungus-king-of-dian-china": "Xylaria polymorpha dead man fingers",
    "zhu-xi-song-dynasty-confucian-exam": "Zhu Xi Song Dynasty Chinese philosopher portrait",
    "swimmer-turbine-tidal-power-scotland": "tidal power turbine",
    "jurassic-squid-beast-wyoteuthis-linsterorum-found": "belemnite fossil Jurassic squid",
    "sr1-freedom-nuclear-spaceship-mars": "nuclear reactor space satellite",
    "jurassic-squid-butt-was-chunkiest-ever": "belemnite fossil Jurassic squid",
    "altermagnetism-third-magnetism-europhysics-prize": "altermagnetism magnetic crystal",
    "2026-10-24-jurassic-bird-lost-flight-dinosaur-features": "Yuezhuornis Jurassic bird dinosaur teeth sickle claw fossil",
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
    "2026-10-23-swiss-glaciers-melting-fast": "Swiss Alps glacier ice mountain snow",
    "swiss-glaciers-vanish-20-percent-ice-loss": "Aletsch Glacier Swiss Alps ice mountain snow melt",
    "alaska-landslide-tsunami-tracy-arm-1580-feet": "Alaska landslide tsunami Tracy Arm fjord",
    "2026-10-23-saudi-arabia-joins-search-for-alien-civilizations": "LaserSETI optical detector telescope Saudi Arabia AlUla SETI sky watcher",
    "webb-stellar-jets-ngc7129-nebula": "NGC 7129 nebula James Webb stellar jets",
    "2026-10-25-webb-stellar-nursery-ngc-7129": "NGC 7129 stellar nursery Cepheus James Webb telescope baby stars protostars infrared",
    "2026-10-24-sparkling-spiral-galaxy-ngc-1827": "NGC 1827 spiral galaxy Hubble edge-on",
    "molecule-quantum-fourier-limit-surface": "crystal surface microscopy",
    "dinosaur-antarctica-fossil-drawer-titanosaur": "Titanosaur vertebra fossil",
    "nightjar-migration-wings-sacrifice-efficiency": "European nightjar (Caprimulgus europaeus) flying",
    "el-nino-alters-weather-patterns-around-world": "El Nino Pacific Ocean satellite",
    "hurricane-simon-atmospheric-waves-nasa": "atmospheric gravity waves hurricane satellite",
    "williston-lake-floating-forest-canada": "floating forest",
    "quantum-limit-molecules-surface-science": "scanning tunneling microscope molecule",
    "2026-10-23-mit-paper-thin-muscle-robot-swims-through-water": "biohybrid robot swimming muscle cells MIT gel fin",
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
    "2026-10-24-flip-rover-supercomputer-moon": "Astrolab FLIP rover lunar surface moon HPE Spaceborne Computer-4",
    "wimpole-estate-5242-species-despite-drought": "great crested newt",
    "farmer-lost-sfi26-wildlife-funding": "barn owl",
    "wasps-nest-took-over-wildlife-office-norfolk": "paper wasp nest",
    "david-bushnell-turtle-secret-submarine-1776": "David Bushnell Turtle submarine",
    "aging-brain-memory-meaning": "brain anatomy diagram hippocampus",
    "2026-10-24-aging-brain-trades-memory-for-wisdom": "hippocampus brain anatomy frontal cortex neuron memory meaning wisdom",
    "roman-temple-germany-frankfurt-limes": "Roman limes archaeological site Germany",
    "mars-helicopter-blade-designs-18km-flight": "Ingenuity Mars helicopter rotor",
    "stanford-microscope-seeing-living-cells": "optical microscopy biological cell",
    "stanford-microscope-seeing-cells-without-labels": "optical microscopy biological cell",
    "moon-base-rover-progress-update-nasa": "lunar rover moon surface",
    "river-taff-fuel-leak-kills-fish": "river pollution foam",
    "six-ways-magic-protected-homes-from-witch-bottles-to-symbols": "witch bottle",
    "2026-10-24-ghostly-eyeless-snail-chinese-cave": "cave snail eyeless freshwater gastropod China Erhaia",
    "lost-dog-survived-month-yellowstone-luna": "Labrador retriever",
    "ultra-processed-food-colorectal-cancer-study": "epidemiology study researcher analyzing questionnaire data",
    "neu5gc-red-meat-sugar-diabetes-link": "beef butcher shop raw meat",
    "perseverance-mars-rover-driving-record": "Perseverance rover Mars surface",
    "astronauts-hearts-mars-spaceflight-test": "astronaut exercise ISS treadmill",
    "2026-10-25-dinosaur-teeth-jurassic-bird-yuezhuornis": "Yuezhuornis fossil dinosaur teeth bird Jurassic China claw",
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
    "2026-10-26-four-minute-strength-training-older-adults": "older adult exercise strength training resistance band elastic band muscle fitness",
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
    "2026-10-23-aussie-bird-count-takes-flight-2026": "Australian magpie rainbow lorikeet noisy miner bird counting Australia wildlife",
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
    "2026-10-23-hunters-moon-why-octobers-brightest": "full Moon near horizon orange colour Moon Illusion",
    "2026-10-23-neutrinos-matter-asymmetry-key": "neutrino detector tank water Cherenkov",
    "2026-10-23-tongue-eating-louse-real-living-tongue": "Cymothoa exigua tongue-eating louse parasitic isopod fish",
    "2026-10-23-two-disks-accretion-jet": "accretion disk black hole jet 3C 120",
    "how-does-your-body-clock-know-day-from-night": "alarm clock sunrise clock face time",
    "2026-10-23-forgotten-math-geniuses-modern-world": "mathematical equation formula graph chart",
    "2026-10-23-earths-center-of-mass-keeps-shifting": "Earth planet from space NASA satellite view",
    "2026-10-23-denmark-bans-mink-farming": "mink animal farm enclosure denmark",
    "2026-10-23-why-should-i-stockpile-and-what-will-i-need": "emergency supply kit backpack water food flashlight",
    "2026-10-23-rubio-india-jamnagar-refinery-energy": "Jamnagar Refinery Reliance Industries oil refinery Gujarat India",
    "2026-10-23-nurdles-from-tyne-spill-wash-up-in-denmark": "plastic nurdles pellets beach microplastic pollution",
    "2026-10-25-rare-lunar-meteorites-fill-gaps-moon-evolution": "lunar meteorite Moon rock NASA Apollo",
    "2026-10-25-hidden-protein-switch-fat-burning-cells": "mitochondria muscle cell fat burning metabolism MTCH2 protein",
    "2026-10-25-zebra-shark-rewilding-indonesia": "zebra shark pup swimming underwater",
    "2026-10-25-spinosaurus-underwater-hunter": "Spinosaurus dinosaur swimming underwater paleoart sail back Nile river",
    "jwst-reveals-lopsided-alien-world-wind": "WASP-17b exoplanet artist impression hot Jupiter space telescope",
    "2026-10-23-typhoon-champi-strongest-storm-of-year-el-nino": "typhoon aerial view spiral satellite storm clouds Pacific Ocean",
    "2026-10-23-dragonfly-first-simulated-flight": "NASA Dragonfly Titan rotorcraft drone landing simulation",
    "2026-10-24-masaya-volcano-beneath-strange-dance": "Masaya volcano Nicaragua Santiago crater lava lake sulfur gas",
    "2026-10-24-mars-valles-marineris-tectonically-active": "Valles Marineris Mars canyon NASA THEMIS visible",
    "2026-10-24-crystal-defect-quantum-surprise": "diamond silicon carbide crystal lattice spin defect quantum atom",
    "2026-10-24-spider-catapult-catches-ants": "spider web silk catapult trap spring mechanism ant",
    "2026-10-23-uae-oil-spill-tanker-hormuz-beaches": "crude oil spill at sea tanker",
    "2026-10-23-forgotten-fossil-fearsome-dinosaur-giant-claws": "Invictibellatrix amberina feathered dinosaur fossil megaraptoran claws",
    "2026-10-20-solar-storm-train-delay-1848-mystery": "Carrington Event 1859 aurora telegraph interference historical illustration",
    "a-tiny-defect-in-a-crystal-reveals-a-big-quantum-surprise": "diamond silicon carbide crystal lattice spin defect quantum atom",
    "cambridge-10-dollar-chip-sensor-wearable": "optical spectrometer sensor chip wearable device silicon photonic",
    "2026-10-24-halloween-skywatching-spooky-targets": "Algol Demon Star Perseus variable star eclipse Pleiades M45 Taurus Cetus constellation sea monster Tycho crater Moon spiderweb rays Taurid meteor shower fireball comet Encke October sky",
    "2026-10-24-lazuli-private-space-telescope-exoplanet-targets": "space telescope coronagraph exoplanet artist impression",
    "2026-10-24-white-dwarfs-yellow-green-pink-purple": "white dwarf star colorful pink yellow green blue artist impression stellar remnant",
    "2026-10-25-oklahoma-meteor-crater-100-million-years-younger": "Ames Crater Oklahoma meteorite impact structure geological zircon crystal USGS",
    "2026-10-24-tiny-snakes-roll-four-times-faster-than-they-slither": "dwarf reedsnake Pseudorabdion saravacense Southeast Asia rolling snake",
    "2026-10-24-nasa-asteroid-bennu-samples-reveal-45-billion-year-old-secret": "asteroid Bennu sample return OSIRIS-REx NASA Solar System dust",
    "2026-10-24-nairobi-building-collapse-rescue": "construction site safety rescue workers emergency services Kenya",
    "2026-10-24-nasa-asteroid-bennu-samples-solar-system-secret": "asteroid Bennu OSIRIS-REx sample return NASA Solar System dust",
    "2026-10-24-halleys-comet-orionid-meteor-shower": "Halley's Comet Giotto 1986 nucleus dust trail meteor shower",
    "2026-10-24-marmoset-brain-smooth-folds": "marmoset monkey brain anatomy neurons synapse",
    "2026-10-24-magnetic-web-above-sun": "Sunrise-III balloon telescope solar magnetic field chromosphere Sun surface",
    "2026-10-24-ukraine-starlink-connection-now-stable-after-network-limits": "Starlink satellite constellation SpaceX low Earth orbit satellite internet user terminal Dish",
    "2026-10-24-ukraine-starlink-stable-connection-after-network-limits": "Starlink satellite constellation SpaceX low Earth orbit satellite internet user terminal Dish",
    "2026-10-24-spacex-starlink-california-launch-cadence-slows": "SpaceX Falcon 9 Starlink launch Vandenberg droneship landing booster landing",
    "2026-10-24-hidden-brain-messages-locus-coeruleus": "locus coeruleus brainstem neuron norepinephrine brain anatomy diagram",
    "2026-10-24-hidden-safety-bias-human-language": "human language word meaning safety bias brain neural network communication",
    "2026-10-24-mit-muscle-robot-swims": "biohybrid robot swimming muscle cells MIT gel fin optogenetics",
    "2026-10-24-how-to-detect-mirror-life": "chirality molecule handedness left right mirror",
    "2026-10-24-on-this-day-v-2-rocket-earth-photos": "V-2 rocket launch White Sands 1946 first photo Earth from space 35mm camera",
    "2026-10-25-chiricahua-national-park-arizona": "Chiricahua National Park Arizona hoodoo rock spires volcanic tuff",
    "2026-10-25-rocket-lab-hawk-satellites-signals-intelligence": "Rocket Lab Electron rocket launch satellite constellation low Earth orbit",
    "2026-10-25-ai-reads-social-media-drug-side-effects": "artificial intelligence AI machine learning large language model reading social media posts computer screen data analysis visualization",
    "2026-10-25-spacex-starfall-second-flight-bandwagon-5": "SpaceX Falcon 9 Starfall capsule return vehicle mini-factory microgravity varda",
    "2026-10-25-quantum-limit-molecules-surface": "crystal surface quantum coherence molecule microscope",
    "2026-10-25-how-cryo-em-revealed-why-statins-cause-muscle-pain": "cryo-electron microscopy protein structure channel membrane RyR1",
    "2026-10-26-brown-bears-rescued-from-russian-cages": "brown bear walking forest wild",
    "2026-10-26-world-kangaroo-day-climate-conservation": "red kangaroo hopping Australian desert macropod",
    "2026-10-25-kill-gut-bacteria-without-harming-good": "myxobacteria soil bacteria argyrin compound antibiotic natural product",
    "carpal-tunnel-15-minute-hydrodissection-procedure": "wrist hand anatomy",
    "2026-10-25-tropical-trees-breathe-at-night-cam-photosynthesis": "Clusia plant tropical tree CAM photosynthesis leaves",
    "2026-10-25-on-this-day-india-launches-chandrayaan-1-first-moon-mission": "Chandrayaan-1 PSLV-XL launch ISRO moon mission India",
    "2026-10-26-googly-eyed-buoys-seabirds-fishing-nets": "seabird common murre guillemot razorbill gillnet fishing net deterrent buoy",
    "2026-10-25-russian-spy-satellite-shadows-us-earth-observing-craft": "satellite in low Earth orbit artist impression Earth below space surveillance",
    "2026-10-26-europe-satellite-starlink-alternative": "Starlink satellite constellation SpaceX low Earth orbit satellite internet user terminal Dish IRIS2 artist impression",
    "2026-10-26-us-sloths-act-import-ban": "three-toed sloth Bradypus hanging from tree branch rainforest canopy",
    "2026-10-25-cassini-discovers-iapetus-yin-yang-moon": "Iapetus moon Saturn two-tone yin-yang dark bright hemisphere Cassini spacecraft",
    "2026-10-26-mysterious-mushroom-makes-people-see-tiny-humans": "Lanmaoa asiatica bolete mushroom fungus mycology brown red pores",
    "2026-10-26-stupendous-black-holes-not-dark-matter": "supermassive black hole dark matter artist impression cosmic space galaxy",
    "2026-10-25-artemis-ii-cabin-leak-warning-tli-burn": "NASA Orion spacecraft Artemis II Trans-Lunar Injection moon artist concept",
    "2026-10-26-plastic-eating-pac-man-enzyme-fights-pollution": "plastic eating enzyme Pac-Man esterase biodegradable bioplastic polymer bacteria microbe",
    "2026-10-26-how-did-scientists-prove-asteroid-hit-north-sea": "Silverpit Crater asteroid impact north sea tsunami shock metamorphism mineral",
    "2026-10-26-did-giant-object-collide-earth-to-form-moon": "Theia protoplanet collision Earth Moon formation giant impact hypothesis artist impression Mars-sized object",
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
                          "gsrsearch": QUERY[slug], "gsrnamespace": "6", "gsrlimit": "15",
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

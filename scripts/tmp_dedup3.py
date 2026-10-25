import subprocess
checks = {
    "gut bacteria without killing good": "gut bacteria.*good|gut.*good.*bacteria|c diff",
    "3000 steps alzheimer": "3000.*step.*alzheim|3000.*step.*slow|steps.*slow.*alzheim",
    "revolutionary microscope hidden machinery": "revolutionary.*microscope|microscope.*hidden.*machinery|microscope.*machinery.*life",
    "why people escape alzheimers high risk gene": "escape.*alzheim|alzheim.*gene.*protect|high.*risk.*gene.*alzheim|alzheim.*risk.*sharp",
    "ghostly eyeless creature chinese cave": "ghostly.*eyeless|eyeless.*creature|eyeless.*cave|ghostly.*cave",
    "beneath masaya volcano magma": "masaya.*magma|masaya.*volcano.*shift|magma.*shift.*masaya|masaya.*ground.*movement",
    "quantum limit surface molecules": "quantum limit.*surface|ultimate.*quantum.*surface|surface.*quantum.*limit",
    "universe first five minutes helium": "first five minutes.*helium|helium.*first five|big bang.*helium",
    "aging brain trades memory for wisdom": "aging brain.*trading|brain.*trading.*memory|trading.*memory.*wisdom|memory.*wisdom.*brain",
    "university study diets slower aging": "10.*diet.*aging|diet.*slower.*aging|ten.*diet",
    "why painful arthritis cancer treatment": "arthritic.*immunotherapy|arthritis.*cancer.*treatment",
    "scientists find 10 diets slower aging": "10.*diet.*aging|ten.*diet.*aging|diet.*slower.*aging",
}
for label, pattern in checks.items():
    result = subprocess.run(["grep", "-rilE", pattern, "content/news/"], capture_output=True, text=True)
    files = result.stdout.strip().replace('\n', ', ') if result.stdout.strip() else "NONE"
    print(f"{label}: {files}")

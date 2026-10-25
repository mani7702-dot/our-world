import subprocess
checks = {
    "quantum limit surface molecules clean": "ultimate quantum limit.*surface|quantum.*fundamental.*limit|molecules.*quantum.*properties|ultra-clean.*surface.*quantum",
    "nasa 16 galaxies cosmic chaos": "16.*galaxy.*chaos|16.*stunning.*galaxies|cosmic.*chaos.*galaxy",
    "alaska landslide tsunami 1580 feet": "alaska.*landslide.*tsunami|alaska.*1580.*mountain|alaska.*monster.*tsunami",
    "carpal tunnel 15 minute": "carpal tunnel.*15.*min|15.*minute.*carpal|carpal.*hydrodissection",
    "weight loss drug ai retatrutide": "retatrutide|unapproved.*weight.*loss|ai.*weight.*loss",
    "mars perchance cliffs mystery": "curiosity.*mars.*cliff|curiosity.*mystery.*horizon|mars.*spectacular",
    "fish oil brain health no benefit": "fish oil.*brain.*benefit|omega.*brain.*no.*benefit|fish oil.*alzheim",
    "dna reverse aging": "reverse.*60.*aging|reverse.*aging.*cell|epigenetic.*clock.*65",
    "ultra processed food cancer": "ultra-processed.*cancer|460.*000.*cancer|processed.*colorectal",
}
for label, pattern in checks.items():
    result = subprocess.run(["grep", "-rilE", pattern, "content/news/"], capture_output=True, text=True)
    files = result.stdout.strip().replace('\n', ', ') if result.stdout.strip() else "NONE"
    print(f"{label}: {files}")

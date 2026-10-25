import subprocess
checks = {
    "viruses build without blueprint": "virus.*build|build.*without.*blueprint",
    "birds afraid women men": "bird.*afraid.*woman|bird.*fear.*woman|afraid.*women.*men",
    "coffee calories jumped": "coffee.*calor|cream.*coffee",
    "hidden messaging brain": "messaging.*deep.*brain|hidden.*messaging.*brain|locus.*coeruleus",
    "crystal defect quantum": "crystal.*defect.*quantum|quantum.*defect.*crystal",
    "tiny defect crystal quantum": "tiny defect.*crystal|quantum.*surprise.*crystal|silicon carbide.*defect",
    "curiosity rover mars cliffs": "curiosity.*mars.*cliff|mars.*mystery.*cliff|valles.*marineris",
    "2884 exploding stars": "exploding.*star.*universe|2884.*exploding|dark.*energy.*chang",
    "brain wrinkles marmoset": "brain.*wrinkle|marmoset.*brain|smooth.*brain",
    "hidden immune weapon lung cancer": "lung cancer.*immune|immune.*lung",
}
for label, pattern in checks.items():
    result = subprocess.run(["grep", "-rilE", pattern, "content/news/"], capture_output=True, text=True)
    files = result.stdout.strip().replace('\n', ', ') if result.stdout.strip() else "NONE"
    print(f"{label}: {files}")

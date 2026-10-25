import subprocess

candidates = {
    "arctic sea ice moves strangely": "arctic sea ice move|sea ice move|ice floe.*collid|ice.*energy.*transfer|strange.*arctic.*ice|arctic.*sea.*ice.*move",
    "tropical trees breathe at night": "tropical tree.*breath|tree.*breathe.*night|camera.*night|drought.*survive|CAM photosynthes",
    "seawater to fresh water": "seawater.*fresh.*water|desalinat|salt.*water.*fresh|brine.*salt",
    "meteor oklahoma younger": "meteor.*oklahoma|ames.*impact|oklahoma.*crater.*370|zircon.*crystal.*meteor",
    "ghostly eyeless snail": "ghostly.*eyeless|eyeless.*snail|blind.*cave.*snail|china.*cave.*snail",
    "golden tree coral costa rica": "golden tree.*coral|coral.*costa.*rica|yellow.*coral.*family|new family.*coral",
}

for label, pattern in candidates.items():
    result = subprocess.run(["grep", "-rilE", pattern, "content/news/"], capture_output=True, text=True)
    files = result.stdout.strip().replace('\n', ', ') if result.stdout.strip() else "NONE"
    print(f"{label}: {files}")

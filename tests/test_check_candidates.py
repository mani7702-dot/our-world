import os

# List all content article slugs
slugs = set()
for d in ['content/news', 'content/explainers', 'content/blog']:
    if os.path.exists(d):
        for fn in os.listdir(d):
            if fn.endswith('.md'):
                slugs.add(fn[:-3].lower())

# New candidates to check
candidates = [
    'one-of-earths-most-powerful-supervolcanoes-is-refilling',
    'nearly-20-of-switzerlands-glacier-ice-has-vanished',
    'dental-implants-can-hijack-your-immune-system',
    'cambridge-chip-wearable-lab-on-wrist',
    'ptsd-treatment-68-percent-remission',
    'mit-tiny-robot-swims-using-living-muscle-cells',
    'exercise-parkinsons-brain-benefit',
    'hidden-messaging-system-brain',
    'tiny-defect-crystal-quantum-surprise',
    'birds-afraid-of-women-scientists-discover',
    'oxford-viruses-build-without-blueprint',
    'three-thousand-exploding-stars-dark-energy',
    'chernobyl-nuclear-fallout-four-decades',
    'curiosity-rover-mars-mystery-horizon',
    'marmoset-brain-wrinkles-smooth',
]

keywords_map = {
    'supervolcano': 'supervolcano',
    'glacier': 'glacier',
    'dental': 'dental',
    'chip': 'chip',
    'ptsd': 'ptsd',
    'muscle-robot': 'muscle-robot',
    'parkinson': 'parkinson',
    'messaging': 'messaging',
    'defect': 'defect',
    'bird': 'bird',
    'virus': 'virus',
    'dark_energy': 'supernova',
    'chernobyl': 'chernobyl',
    'curiosity': 'curiosity',
    'marmoset': 'marmoset',
}

for c in candidates:
    found = False
    for key, kw in keywords_map.items():
        if key in c.lower():
            for s in slugs:
                if kw in s.lower():
                    found = True
                    print(f'{c} -> EXISTS: {s}')
                    break
            if found:
                break
    if not found:
        print(f'{c} -> NEW!')

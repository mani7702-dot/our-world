import os

existing = set()
for root, dirs, files in os.walk('content'):
    for fn in files:
        if fn.endswith('.md'):
            existing.add(fn[:-3])

# Remaining candidates that might be fresh
remaining = [
    "How Jackdaw ignites row over climate and costs",
    "10 Period-Drama Details That Look Fake but Are Historically Accurate",
]

for title in remaining:
    found = False
    for ex in existing:
        if title[:30].lower() in ex.lower() or ex.lower() in title[:30].lower():
            found = True
            print(f'[WRITTEN] {title} -> matches {ex}')
            break
    if not found:
        print(f'[NOT WRITTEN] {title}')

# Also check for block keywords
block = ['war', 'attack', 'death', 'killed', 'murder', 'court', 'lawsuit', 'politic', 'terror', 'bomb', 'shooting', 'climate']
for title in remaining:
    blocked = any(b in title.lower() for b in block)
    print(f'  Block check: {title} -> {"BLOCKED" if blocked else "ok"}')

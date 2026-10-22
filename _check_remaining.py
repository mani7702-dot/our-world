#!/usr/bin/env python3
import os, glob, re

# Let me check the BBC science candidates that weren't marked as already written
# From the BBC output:
# "How to move 1,300 plants for Kew's Palm House mega makeover" - new?
# "First dinosaur bone from Antarctica found in a drawer" - need to check
# "How cleaning up the air is speeding up global warming" - exists as cleaning-air-lifts
# "How the UK's extreme heat is shifting the conversation about air-con" - new?
# "The hidden cost of the night shift and how to sleep it off" - new?
# "After record heat, could the Atlantic make Britain's weather even more extreme?" - new?
# "Why cheap power could matter more than clean power in the push for net zero" - new?

candidates = {
    'kew plants palm house': ['kew', 'palm house', '1300 plant'],
    'extreme heat air con': ['air.con', 'air conditioning', 'extreme heat', 'britain.*weather'],
    'night shift sleep': ['night shift', 'sleep it off'],
    'atlantic extreme weather': ['atlantic.*extreme', 'britain.*weather.*extreme'],
    'cheap power net zero': ['cheap power', 'net zero'],
    'dinosaur antarctica drawer': ['dinosaur.*antarctica', 'antarctica.*dinosaur', 'drawer'],
}

for d in ['content/news', 'content/blog']:
    for f in glob.glob(f'{d}/*.md'):
        with open(f) as fh:
            content = fh.read().lower()
        fname = os.path.basename(f)
        for key, patterns in candidates.items():
            for pat in patterns:
                if re.search(pat, content):
                    print(f"EXISTS: {key} -> found '{pat}' match in {d}/{fname}")
                    break

# Also check for the Mars mission story more carefully - is the BBC story about a DIFFERENT mission?
print("\n=== Check for any Oct 2026 Mars mission ===")
for f in glob.glob('content/news/*.md') + glob.glob('content/blog/*.md'):
    with open(f) as fh:
        content = fh.read()
    # look for articles about Oct 2026 Mars launches (not MMX/Phobos)
    if 'mars' in content.lower() and ('launch' in content.lower() or 'blast' in content.lower()):
        for line in content.split('\n')[:5]:
            if line.startswith('title:'):
                print(f"  {fname if False else os.path.basename(f)}: {line.strip()}")
                break

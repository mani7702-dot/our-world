#!/usr/bin/env python3
# Dedup check: confirm candidate topics not already published in content/.
import subprocess
terms = ["hidden bias language", "microscope hidden machinery",
         "rolling snake faster", "universe first five minutes",
         "magnetic web above Sun", "Bennu samples reveal",
         "16 galaxies cosmic chaos", "eyeless creature Chinese cave",
         "messaging system brain", "surprising double benefit exercise",
         "ghostly eyeless creature"]
for t in terms:
    r = subprocess.run(["grep", "-ril", t, "/home/ubuntu/our-world/content"],
                       capture_output=True, text=True)
    count = len([l for l in r.stdout.strip().split("\n") if l])
    print(f"{count}  --  {t}")

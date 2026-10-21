import sys
from datetime import datetime
# Read UTC time piped from stdin (via a temp file, not a pipe)
import os
utc_str = sys.argv[1] if len(sys.argv) > 1 else ""
if not utc_str:
    utc_str = open("/tmp/_cron_utc.txt").read().strip()
h, mo = utc_str.split(":")
hi = int(h) + 5
mi = int(mo) + 30
if mi >= 60:
    mi -= 60
    hi += 1
hi %= 24
print(f"{hi:02d}:{mi:02d}")

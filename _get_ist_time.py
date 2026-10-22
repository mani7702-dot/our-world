#!/usr/bin/env python3
"""Get current IST time for the article."""
from datetime import datetime
now = datetime.now()
ist_offset = 5*60 + 30  # IST is UTC+5:30
ist_now = now.timestamp() + ist_offset*60
ist_dt = datetime.fromtimestamp(ist_now)
print(f"IST time: {ist_dt.strftime('%H:%M')}")

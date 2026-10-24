#!/usr/bin/env python3
from datetime import datetime, timezone, timedelta
ist = timezone(timedelta(hours=5, minutes=30))
print(datetime.now(ist).strftime('%H:%M'))

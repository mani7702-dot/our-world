import datetime

# Get current IST time
# IST is UTC+5:30
utc_now = datetime.datetime.utcnow()
ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
print(f"Current IST time: {ist_now.strftime('%H:%M')} IST")
print(f"Current IST date: {ist_now.strftime('%Y-%m-%d')}")

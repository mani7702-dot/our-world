import re
raw = open("/tmp/ipcc.html","wb").read().decode("utf-8","replace") if __import__("os").path.exists("/tmp/ipcc.html") else ""
# already fetched ipcc.ch/report/ar6/wg1 earlier as 350547 bytes; refetch cleanly
import subprocess
UA="Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
h = subprocess.run(["curl","-s","--compressed","--max-time","20","-A",UA,"https://www.ipcc.ch/report/ar6/wg1/"],
                   capture_output=True,text=True).stdout
open("/tmp/ipcc.html","w").write(h)
t=re.search(r"<title>(.*?)</title>",h,re.S|re.I)
print("TITLE:",(t.group(1).strip()[:140] if t else "(none)"))
# search for aerosol / sulphate / cooling mention
for kw in ["aerosol","sulphate","aerosols have","shorten","cooling","anthropogenic aerosol"]:
    idx = h.lower().find(kw.lower())
    if idx>=0:
        seg = re.sub(r"<[^>]+>"," ",h)[max(0,idx-60):idx+140].strip()
        print(f"[{kw}]: ...{seg}...")

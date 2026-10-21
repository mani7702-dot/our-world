import subprocess, sys, os

url = sys.argv[1]
dest = sys.argv[2]
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, url, "-o", dest], check=True)
print("Downloaded:", dest, "size:", os.path.getsize(dest))

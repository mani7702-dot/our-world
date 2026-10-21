import subprocess, sys

url = sys.argv[1]
dest = sys.argv[2] if len(sys.argv) > 2 else '/tmp/feed.xml'
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
subprocess.run(["curl", "-s", "--compressed", "--max-time", "25", "-A", UA, url, "-o", dest], check=True)
print("Downloaded:", dest)

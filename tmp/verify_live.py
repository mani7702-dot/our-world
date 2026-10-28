import subprocess, time

url = "https://mani7702-dot.github.io/our-world/news/2026-10-28-mysterious-dwarf-planet-candidate-beyond-neptune.html"

for i in range(6):
    code = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True, text=True, timeout=20
    ).stdout.strip()
    print(f"Attempt {i+1}: HTTP {code} for {url}", flush=True)
    if code == "200":
        print("SUCCESS: Article is live!")
        break
    time.sleep(20)

# Also check blog path
blog_url = "https://mani7702-dot.github.io/our-world/blog/2026-10-28-mysterious-dwarf-planet-candidate-beyond-neptune.html"
blog_code = subprocess.run(
    ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", blog_url],
    capture_output=True, text=True, timeout=20
).stdout.strip()
print(f"Blog path: HTTP {blog_code} for {blog_url}")
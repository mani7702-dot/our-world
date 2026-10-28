import subprocess, time

url = "https://mani7702-dot.github.io/our-world/news/2026-10-28-mysterious-dwarf-planet-candidate-beyond-neptune.html"

# Wait 60 more seconds then check
time.sleep(60)
for i in range(4):
    code = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True, text=True, timeout=20
    ).stdout.strip()
    print(f"Attempt {i+1}: HTTP {code}", flush=True)
    if code == "200":
        print("SUCCESS!")
        break
    time.sleep(15)
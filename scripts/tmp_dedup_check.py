import subprocess, sys, re

checks = {
    "hidden bias human language": "hidden bias in human language",
    "hidden switch burns fat": "hidden switch.*fat",
    "tiny snakes roll": "tiny snake.*roll|roll.*faster.*slither",
    "rock plunged 90 km": "rock.*plunged.*90.*km|plunged.*into.*earth",
    "switzerland glacier ice vanished": "swiss.*glacier|switzerland.*glacier|glacier.*ice.*vanish",
    "dental implants immune": "dental implant",
    "mit tiny robot muscle": "tiny robot.*muscle|living muscle robot",
    "ptsd remission": "ptsd.*remiss|remission.*ptsd",
    "astronauts hearts mars": "astronaut.*heart.*mar|heart.*mars",
}

for label, pattern in checks.items():
    result = subprocess.run(
        ["grep", "-rilE", pattern, "content/news/"],
        capture_output=True, text=True
    )
    files = result.stdout.strip() if result.stdout.strip() else "NONE"
    print(f"{label}: {files}")

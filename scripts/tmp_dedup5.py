import subprocess

# Check both fresh candidates against ALL content/news/ files with broad keywords
candidates = {
    "curiosity mars mystery horizon": "curiosity.*mars.*myster|mars.*mystery.*horizon|curiosity.*spectacular.*view|mars.*spectacular.*cliff|wind.*carved.*cliff|curiosity.*approach.*cliff|valles.*marineris",
    "perseverance driving record": "perseverance.*record|perseverance.*driv|off-world.*driv|all-time.*driving|perseverance.*shatter|oppor.*driving record|self-driving.*mars",
}

for label, pattern in candidates.items():
    result = subprocess.run(["grep", "-rilE", pattern, "content/news/"], capture_output=True, text=True)
    files = result.stdout.strip() if result.stdout.strip() else "NONE"
    print(f"{label}: {files}")

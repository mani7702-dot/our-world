import subprocess
result = subprocess.run(
    ["curl", "-s", "--max-time", "25", "-H", "User-Agent: Mozilla/5.0",
     "https://r.jina.ai/https://www.sciencedaily.com/releases/2026/09/260922005712.htm"],
    capture_output=True, text=True, timeout=30
)
print(result.stdout[:3000])

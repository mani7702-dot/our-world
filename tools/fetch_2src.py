#!/usr/bin/env python3
import subprocess
UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"
def jina(url):
    r = subprocess.run(["curl", "-s", "--max-time", "60", "-A", UA, "https://r.jina.ai/" + url],
                       capture_output=True, text=True)
    return r.stdout
nao = jina("https://www.nao.ac.jp/en/news/science/2026/20260930-sso.html")
arxiv = jina("https://arxiv.org/abs/2607.26353")
with open("tools/_nao.txt", "w") as f:
    f.write(nao)
with open("tools/_arxiv.txt", "w") as f:
    f.write(arxiv)
print("NAOJ len:", len(nao))
print("arxiv len:", len(arxiv))
print("NAOJ title line:", [l for l in nao.splitlines() if l.startswith("Title")][:1])

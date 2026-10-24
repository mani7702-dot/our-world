#!/usr/bin/env python3
# Fetch a ScienceDaily release article via Jina Reader proxy using terminal curl
# (browser stack is down; per runbook, curl -> Jina is the documented fallback).
import subprocess, sys, os

UA = "Mozilla/5.0 (OurWorld picker; contact andugulamani722@gmail.com)"

def jina(url):
    proxy = "https://r.jina.ai/" + url
    r = subprocess.run(["curl", "-s", "--max-time", "45", "-A", UA, proxy],
                       capture_output=True, text=True)
    return r.stdout

if __name__ == "__main__":
    for url in sys.argv[1:]:
        print("====", url)
        print(jina(url)[:4000])
        print("...[truncated]", len(jina(url)), "chars")

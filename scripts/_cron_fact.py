#!/usr/bin/env python3
"""Tirith-safe fact extractor: read saved HTML, print context around key terms."""
import sys, re

def main():
    path = sys.argv[1]
    key = sys.argv[2] if len(sys.argv) > 2 else "joseph bell"
    t = open(path, errors="replace").read().lower()
    print(f"file={path} bytes={len(t)} key={key}")
    idx = t.find(key.lower())
    print(f"first '{key}' at index: {idx}")
    if idx >= 0:
        s = max(0, idx-300); e = min(len(t), idx+700)
        print(repr(t[s:e].replace("\n", " ")))
    # second source hits
    for term in ["conan doyle", "sherlock holmes", "edinburgh", "royal infirmary",
                 "surgical", "deduction", "forensic", "inspired", "model", "student"]:
        c = t.count(term)
        print(f"  count '{term}': {c}")

if __name__ == "__main__":
    main()

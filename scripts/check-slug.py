import io, os, re

fn = "content/news/2026-10-20-strange-surprising-lakes-around-world.md"
t = io.open(fn, encoding="utf-8").read()
print("Has image line:", bool(re.search(r"^image:", t, re.M)))
print("First 5 lines:")
for line in t.split("\n")[:6]:
    print(repr(line))

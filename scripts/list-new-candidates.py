import re, sys

raw_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/raw-candidates.tsv"

# Read raw candidates
with open(raw_path, "r", errors="replace") as f:
    lines = f.readlines()

# Read existing content SD IDs
existing = set()
import glob
for path in glob.glob("content/news/*.md") + glob.glob("content/blog/*.md"):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        for m in re.finditer(r'/releases/(\d{4}/\d+/\d+)\.htm', content):
            existing.add(m.group(1))
    except:
        pass

print("=== NEW (not yet published) candidates ===")
for line in lines:
    m = re.search(r'/releases/(\d{4}/\d+/\d+)\.htm', line)
    if m:
        sd_id = m.group(1)
        if sd_id not in existing:
            title = line.split('\t')[0]
            # Get description
            parts = line.split('\t')
            desc = parts[2][:150] if len(parts) > 2 else ""
            print(f"  [{sd_id}] {title}")
            print(f"    desc: {desc}")
            print()
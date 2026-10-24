import re

with open('/home/ubuntu/our-world/content/news/2026-10-24-crystal-defect-quantum-surprise.md', 'r') as f:
    text = f.read()

# Remove frontmatter
parts = text.split('---', 2)
if len(parts) >= 3:
    body = parts[2].strip()
else:
    body = text

# Count words in body only
words = body.split()
print(f"Body word count: {len(words)}")

# Check for required elements
print(f"Has 'Try this at home': {'Try this at home' in body}")
print(f"Has 'Fun Fact': {'Fun Fact' in body}")
print(f"Has 'for-grownups': {'for-grownups' in body or 'For the grown-ups' in body}")
print(f"Has 'Sources': {'Sources' in body}")
print(f"Has image: {'image:' in text}")
print(f"Has time: {'time:' in text}")
print(f"Has date: {'date:' in text}")

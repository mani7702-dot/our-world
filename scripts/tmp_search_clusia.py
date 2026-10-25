import sys
sys.path.insert(0, '/home/ubuntu/our-world/scripts')
from commons_fallback_query import search_commons
import time

# Try broadened keyword variants
queries = [
    ["Clusia", "plant", "tropical", "tree", "leaves"],
    ["Clusia", "plant", "leaves", "tropical tree"],
    ["Clusia", "plant", "Costa Rica", "leaves"],
    ["Clusia rosea", "plant", "red", "leaves"],
    ["CAM", "photosynthesis", "plant", "leaves"],
    ["tropical plant", "rainforest", "leaves"],
]

for i, q in enumerate(queries):
    print(f"\n=== Query {i+1}: {q} ===")
    results = search_commons(q, limit=8)
    for j, r in enumerate(results[:5]):
        lic_ok = "public domain" in r['license'].lower() or "cc0" in r['license'].lower() or "cc by" in r['license'].lower()
        print(f"  {j+1}. {r['title']} | License: {r['license']} | OK={lic_ok}")
        print(f"     Artist: {r['artist'][:80]}")
        print(f"     Thumb: {r['thumb']}")
    time.sleep(1.5)

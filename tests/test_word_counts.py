import os, re

# Check word counts of existing articles
content_dir = '/home/ubuntu/our-world/content/news'
results = []
for fn in sorted(os.listdir(content_dir)):
    if fn.endswith('.md'):
        with open(os.path.join(content_dir, fn), 'r') as f:
            text = f.read()
        parts = text.split('---', 2)
        if len(parts) >= 3:
            body = parts[2].strip()
        else:
            body = text
        words = len(body.split())
        results.append((words, fn))

# Show some examples
for w, fn in sorted(results, key=lambda x: x[0])[:10]:
    print(f'{w:4d} words: {fn}')
print('...')
for w, fn in sorted(results, key=lambda x: x[0])[-10:]:
    print(f'{w:4d} words: {fn}')
print(f'\nTotal articles: {len(results)}')
print(f'Min: {min(r[0] for r in results)}')
print(f'Max: {max(r[0] for r in results)}')
print(f'Avg: {sum(r[0] for r in results)//len(results)}')

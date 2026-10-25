#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, subprocess
result = subprocess.run(["python3", "scripts/sd-top-fallback.py"], capture_output=True, text=True, cwd="/home/ubuntu/our-world")
for line in result.stdout.strip().splitlines():
    try:
        r = json.loads(line)
        print(r['tag'], '|', r['title'], '|', r['url'])
    except:
        pass

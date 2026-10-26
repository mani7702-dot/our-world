#!/usr/bin/env python3
"""Run _commons_progressive_search.py with proper args for wildflower meadow."""
import subprocess, sys
os_result = subprocess.run([sys.executable, "scripts/_commons_progressive_search.py",
    "--slug", "2026-10-26-kings-lynn-wildflower-meadow-buzzing-with-life",
    "--out", "assets/images/2026-10-26-kings-lynn-wildflower-meadow-buzzing-with-life.jpg",
    "--query", "wildflower meadow native England",
    "--query", "wildflower meadow England bee butterfly pollinator",
    "--query", "meadow wildflowers native plants UK",
    "--verify-kw", "meadow",
], capture_output=True, text=True, timeout=90)
print("STDOUT:", os_result.stdout)
print("STDERR:", os_result.stderr[-500:] if os_result.stderr else "")
print("RC:", os_result.returncode)
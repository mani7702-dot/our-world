#!/usr/bin/env python3
import re
line = "- ScienceDaily (2026-10-18): https://www.sciencedaily.com/releases/2026/10/261018205053.htm"
print("len digits:", len(re.findall(r"\d", "261018205053")))
print("digits:", re.findall(r"\d", "261018205053"))
print("14d match:", re.findall(r"(\d{14})\.htm", line))
print("13d match:", re.findall(r"(\d{13})\.htm", line))
print("end of line repr:", repr(line[-5:]))

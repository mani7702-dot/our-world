#!/usr/bin/env python3
"""Search raw SD feed for ALL titles containing antarctica/dinosaur/fossil, print title+link."""
import re, html
from xml.etree import ElementTree as ET
tree=ET.parse("/tmp/owraw/sciencedaily_top.xml")
print("=== ALL SD-top titles mentioning antarctica OR dinosaur OR fossil ===")
for it in tree.getroot().iter("item"):
    t=html.unescape(it.findtext("title","")).strip().lower()
    if "antarctica" in t or "dinosaur" in t or "fossil" in t:
        print("TITLE:", html.unescape(it.findtext("title","")).strip())
        print("  LINK:", it.findtext("link"))
print("\n=== ALL SD-top titles mentioning brain OR organoid OR neuron ===")
for it in tree.getroot().iter("item"):
    t=html.unescape(it.findtext("title","")).strip().lower()
    if "brain" in t or "organoid" in t or "neuro" in t:
        print("TITLE:", html.unescape(it.findtext("title","")).strip())
        print("  LINK:", it.findtext("link"))

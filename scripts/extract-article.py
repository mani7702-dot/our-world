#!/usr/bin/env python3
"""File-based HTML article extractor for Our World cron (Tirith-safe).
Usage: python3 scripts/extract-article.py <file.html>
Prints TITLE + body paragraphs + KEYWORD COUNTS.
Never inline with backslash-heavy logic; never name `inspect.py`."""
import sys, html
from html.parser import HTMLParser


class ParaExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_p = False
        self.in_title = False
        self.parts = []
        self.cur = ""
        self.title = ""

    def handle_starttag(self, t, a):
        if t == "p":
            self.in_p = True
        if t == "title":
            self.in_title = True

    def handle_endtag(self, t):
        if t == "p" and self.in_p:
            tx = html.unescape(self.cur).strip()
            if len(tx) > 40:
                self.parts.append(tx)
            self.cur = ""
            self.in_p = False
        if t == "title":
            self.in_title = False

    def handle_data(self, d):
        if self.in_p:
            self.cur += d
        if self.in_title:
            self.title += d


def extract(path):
    t = open(path, encoding="utf-8").read()
    p = ParaExtractor()
    p.feed(t)
    return p.title, p.parts


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: extract-article.py <file.html>")
        sys.exit(2)
    title, paras = extract(sys.argv[1])
    print("TITLE:", title)
    print("--- %d paragraphs ---" % len(paras))
    # Print paragraphs 5..end (skip the first boilerplate)
    for para in paras[4:]:
        print(para)
        print()

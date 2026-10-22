---
title: How did AI find a hidden 'secret door' in 70% of the world's websites — and fix it before hackers could?
date: 2026-10-22
time: 23:19
category: World
read: 4 min
excerpt: An AI system spotted critical security bugs in PHP — the language behind 7 in 10 websites — that had been hiding for over a decade. Security teams raced to patch them before bad actors could exploit them.
tags: world, technology, computers, internet, ai, cybersecurity
sample: false
for-grownups: An AI system discovered two critical zero-day vulnerabilities (CVE-2026-109618 and CVE-2026-109619) in PHP, a programming language powering ~70% of websites including Wikipedia. The flaws, named "php2shell," allowed unauthenticated remote code execution — meaning a hacker could take over a server without any password. The discoveries were made by cybersecurity firms Wiz and Calif with AI assistance, and the PHP Foundation released emergency patches on October 22, 2026. Major organizations including Wikimedia, the BBC, and various government portals temporarily took systems offline as a precaution. The US NSA, UK NCSC, and counterparts in the EU, Singapore, and Australia issued urgent advisories telling organizations to patch immediately or take systems offline.
sources:
  - https://www.bbc.co.uk/news/videos/cq0ld7e0jg2eo
  - https://www.bbc.co.uk/news/articles/c3qjnwye0ep5o
  - https://www.php.net/
  - https://calif.io/blog/php2shell
---

# How did AI find a secret door in 70% of the internet — and close it before anyone got hurt?

## The invisible language powering your favorite websites

Imagine if 7 out of every 10 websites you visit — including Wikipedia, online stores, and your school's portal — were all built using the same invisible brain. That brain is called **PHP**, a special language programmers use to make websites dynamic and interactive.

You have probably used PHP-powered sites without even knowing it. When you search for something on Wikipedia, post a comment, or add items to an online shopping cart — PHP is the behind-the-scenes helper making it all work.

## The hidden cracks in the code

For more than a decade, two tiny cracks had been hiding inside PHP's code — like secret doors that only the right key could open. These cracks were so well-hidden that even expert programmers had not noticed them. They were called **zero-day vulnerabilities**, meaning no one knew they existed until they were just discovered.

Worse yet, these secret doors were *especially dangerous*: they would let a hacker take full control of any website built with PHP — all without needing a password or special key. Security researchers called this flaw **php2shell**.

## How AI became the detective

Normally, finding bugs that have been hiding for years is like looking for a single typo in a massive library. But this time, the detectives had a powerful new partner: **artificial intelligence**.

Cybersecurity companies **Wiz** and **Calif** used AI to scan through millions of lines of PHP code, looking for patterns that human eyes might miss. The AI spotted the two hidden cracks and raised the alarm.

When that happened, something amazing occurred. Around the world, website operators, government agencies, and tech teams all dropped what they were doing and rushed to fix the problem — because the AI had found the cracks *before* hackers could use them.

## Fixing the internet in record time

The team that maintains PHP (called the **PHP Foundation**) worked around the clock and released emergency fixes — called **patches** — on October 22, 2026.

Major organizations took extra precautions too. **Wikimedia** (the group behind Wikipedia) temporarily took some systems offline. The **BBC**, government websites in the UK, Finland, and Scotland, and many others did the same — just to be safe.

Security agencies in the US, UK, EU, Singapore, and Australia all sent out urgent warnings: "Update your systems right away, or take them offline until you can."

## Why this is good news

Even though the story sounds scary, the ending is actually a victory. Thanks to AI, a potentially dangerous flaw was found and fixed quickly. Millions of websites are now safer because of it.

It shows how technology and human teamwork can solve big problems together — and how sometimes, the good guys find the crack before the bad guys even know it's there.

## Try this at home

You can be a code detective too! Ask a grown-up to help you visit [scratch.mit.edu](https://scratch.mit.edu) — a website where you can write simple programs. Look at how a tiny typo in your code (like writing "lool" instead of "loop") can break your whole project. That is a very small version of the kind of mistake the AI found — except in this case, the mistake was hiding in code that powers the internet!

## Fun Fact

The word "PHP" originally stood for "Personal Home Page" — but it was later changed to "PHP: Hypertext Preprocessor." The new name is like a secret code inside a secret code!

For-grownups: This article was written based on BBC News reporting (Joe Tidy, Technology Correspondent) and verified against the official PHP.net advisory (October 22, 2026), which confirms releases 8.5.12, 8.4.27, 8.3.36, and 8.2.35 fix two critical remote code execution vulnerabilities (CVE-2026-109618 and CVE-2026-109619, branded "php2shell"). The Calif cybersecurity firm's blog post confirms their role in the discovery alongside Wiz. No speculative technical details beyond what the official sources confirm are included.

## Sources

- [BBC News — How did AI discover the internet's massive cyber-security risk?](https://www.bbc.co.uk/news/videos/cq0ld7e0jg2eo)
- [BBC News — What is PHP and why did it spark a global cyber-security scramble?](https://www.bbc.co.uk/news/articles/c3qjnwye0ep5o)
- [PHP.net — Official security advisory, October 22, 2026](https://www.php.net/)
- [Calif — php2shell discovery blog post](https://calif.io/blog/php2shell)

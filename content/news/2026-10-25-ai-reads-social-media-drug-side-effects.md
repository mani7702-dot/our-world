---
title: "How did AI read millions of Reddit posts to find hidden drug side effects?"
date: 2026-10-25
time: 03:02
image: assets/images/2026-10-25-ai-reads-social-media-drug-side-effects.png
image_caption: "Liam Huang / CC BY 2.0 / Wikimedia Commons"
category: Science
read: 3 min
excerpt: "Scientists taught an AI to scan nearly 150,000 Reddit posts from people taking an unapproved weight-loss drug. The AI found something surprising: users reported increased appetite — the opposite of what the drug is supposed to do."
tags: science, AI, machine learning, social media, drugs, healthcare, retatrutide, explainers
sample: false
for-grownups: "Researchers at the University of Pennsylvania used large language models (LLMs) to analyze 148,442 Reddit posts and comments from about 37,000 users who claimed to be taking retatrutide, an experimental triple-agonist drug (GLP-1/GIP/glucagon receptor agonist) developed by Eli Lilly that has not yet received regulatory approval. After filtering for posts describing personal use of the unapproved drug, the AI extracted 7,823 users who reported at least one medically classifiable symptom. The AI system translated users' symptom descriptions into standardized medical terminology, enabling pattern detection across different self-reported terms. Among users whose symptoms could be classified, increased appetite was the most common complaint — surprising because retatrutide is designed to suppress hunger and its Phase 2 clinical trials primarily identified gastrointestinal effects. The study, titled \"Self-Reported Adverse Effects Among Social Media Users Taking Nonapproved Retatrutide,\" was published in JAMA Network Open (Oct 1, 2026, PMID 42873503) by Sehgal NKR, Tronieri JS, Rader B, Ungar L, Guntuku SC. Retatrutide is a peptide that agonizes three receptors: GLP-1 (satiety and insulin sensitivity), GIP, and glucagon (energy expenditure). Unlike semaglutide (one receptor) or tirzepatide (two receptors), retatrutide targets three, potentially producing a different side-effect profile. The researchers emphasized that Reddit reports cannot establish causation — users obtaining unapproved drugs from gray-market sources may not be receiving genuine retatrutide, and their experiences cannot replace regulated clinical trial data. However, the AI approach demonstrates how social media can surface hypotheses for further investigation, identifying patterns that traditional pharmacovigilance systems might miss. This builds on the team's earlier work analyzing 400,000+ Reddit posts about semaglutide and tirzepatide, where they identified reports of menstrual irregularities that were later confirmed in FDA adverse-event databases."
sources:
  - name: ScienceDaily — University of Pennsylvania
    url: https://www.sciencedaily.com/releases/2026/10/261020085018.htm
  - name: JAMA Network Open — "Self-Reported Adverse Effects Among Social Media Users Taking Nonapproved Retatrutide"
    url: https://pubmed.ncbi.nlm.nih.gov/42873503/
  - name: Wikipedia — Retatrutide (triple hormone receptor agonist, GLP-1/GIP/glucagon)
    url: https://en.wikipedia.org/wiki/Retatrutide
  - name: Wikipedia — Large language model (AI text analysis, transformer architecture)
    url: https://en.wikipedia.org/wiki/Large_language_model
---

# How did AI read millions of Reddit posts to find hidden drug side effects?

## The social media detective story

Imagine you are a detective, but instead of crime scenes you are investigating a massive online conversation. That is exactly what happened when scientists decided to use **artificial intelligence** to scan hundreds of thousands of posts from people talking about an experimental weight-loss drug on Reddit.

The drug is called **retatrutide**. It is an experimental medicine made by Eli Lilly that is **not yet approved** by health regulators. Despite that, people around the world are ordering it through online "gray market" websites and sharing their experiences on social media. Scientists at the **University of Pennsylvania** wondered: could an AI read all those posts and spot patterns that human eyes might miss?

## Teaching AI to understand symptoms

The researchers faced a big challenge. Across nearly **150,000 Reddit posts** from about 37,000 users, people described their symptoms in all sorts of ways — some said "I feel hungrier," others wrote "my appetite is ravenous," and many did not even mention appetite at all.

Instead of reading every post by hand (which would take years), the team used a **large language model** — the same type of AI that powers modern chatbots. This AI was trained on vast amounts of text and could understand what different people meant even when they used different words. It pulled out descriptions of symptoms and converted them into standardized medical terms so the researchers could count and compare them.

The AI then filtered the posts to find only those where users clearly described **actually taking the unapproved drug**, not just reading about it. From that pool, it identified **7,823 users** who reported at least one symptom they could classify medically.

## A surprising discovery

After the AI did its sorting, one result stood out. Among users whose symptoms could be classified, the most common complaint was **increased appetite**.

That surprised everyone. Here is why: retatrutide is designed to make you feel *less* hungry, not more. In the drug's clinical trials, participants mostly reported stomach-related side effects like nausea — exactly what doctors expected.

But on Reddit, the pattern was different. People taking the unapproved version often said they felt *hungrier*. Scientists had two main explanations:
- The drug works differently from what early trials showed, affecting multiple hormone pathways (retatrutide targets three receptors, compared to one or two for older drugs).
- The people on Reddit may not actually be getting real retatrutide — gray-market products can vary wildly in quality and ingredients.

The researchers published their findings in **JAMA Network Open** (PMID 42873503), showing not just *what* people experienced, but *how* AI made it possible to find patterns hidden in a massive pile of messy real-world data.

## Why this matters for the future of medicine

This is not just about one weight-loss drug. It is a preview of how AI might one day help doctors and scientists listen to patients in a whole new way.

Traditional drug safety systems rely on doctors and patients reporting problems after a drug is approved. But what if AI could scan social media, forums, and other online spaces continuously, flagging unusual patterns years earlier?

The same research team had already used this approach for two other weight-loss drugs — **semaglutide** and **tirzepatide** — where their AI spotted reports of menstrual irregularity that were later confirmed in official FDA databases. That success showed the method works.

The key insight: social media is a **new kind of laboratory**. It is messy, unfiltered, and full of uncertainty — but it also holds millions of real people describing real experiences in real time. AI is the tool that makes it possible to listen to all of them at once.

## Try this at home

Pick a topic you are curious about — say, a new phone or a recent movie. Then look at how people talk about it online. Do they use the same words? Are there complaints you never noticed before? That is the same skill the AI was using — finding patterns in how humans describe their experiences, just at a much bigger scale.

## Fun Fact

The word "algorithm" was originally a mathematical term named after a 9th-century Persian mathematician, Muhammad ibn Musa al-Khwarizmi, whose name was Latinized to "Algoritmi." Today his name powers everything from search engines to the AI that reads your social media posts.

## for-grown-ups

The study is a **cross-sectional observational analysis**, not a clinical trial — meaning it can identify associations and generate hypotheses, but cannot prove that retatrutide causes any specific symptom. Reddit data is also self-selected: users who join forums about experimental drugs are not representative of the general population. The team's earlier semaglutide/tirzepatide study (which identified menstrual irregularity reports later confirmed in FDA data) is the strongest validation of the AI-based signal detection approach. Retatrutide's triple-receptor mechanism (GLP-1 + GIP + glucagon) means it can have a broader physiological footprint than single-receptor GLP-1 drugs, which may contribute to differences between controlled trial results and real-world user reports.

---

## Sources

1. ScienceDaily — University of Pennsylvania, "People are taking an unapproved weight-loss drug. AI found something surprising" (October 20, 2026): https://www.sciencedaily.com/releases/2026/10/261020085018.htm
2. JAMA Network Open — Sehgal NKR, Tronieri JS, Rader B, Ungar L, Guntuku SC, "Self-Reported Adverse Effects Among Social Media Users Taking Nonapproved Retatrutide" (October 1, 2026), PMID 42873503: https://pubmed.ncbi.nlm.nih.gov/42873503/
3. Wikipedia — Retatrutide (triple hormone receptor agonist, GLP-1/GIP/glucagon, Eli Lilly): https://en.wikipedia.org/wiki/Retatrutide
4. Wikipedia — Large language model (transformer architecture, natural language processing): https://en.wikipedia.org/wiki/Large_language_model

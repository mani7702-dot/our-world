---
title: How did a computer work out the shape of 200 million proteins?
slug: "2026-10-28-alphafold-protein-shapes-nobel-chemistry"
date: "2026-10-28"
time: "08:37"
image: assets/images/2026-10-28-alphafold-protein-shapes-nobel-chemistry.png
image_caption: "An antibody protein drawn as a ribbon model of its folded 3D shape — one of the structures that decides what a protein can do. Credit: Wikimedia Commons (CC BY-SA 4.0)"
category: "How Things Work"
read: "4 min"
excerpt: "Proteins are the tiny machines that run your body, and their shape decides what they can do. Working out that shape used to take years in a lab. Then a computer program called AlphaFold2 did it for nearly every protein scientists had ever found — and won a Nobel Prize for it."
tags: ["science", "how-it-works", "proteins", "ai", "nobel-prize", "biology", "chemistry"]
sample: false
for-grownups: "Proteins are chains of amino acids (20 standard types) that fold into specific three-dimensional shapes; the shape determines function, so predicting structure from sequence was a 50-year-old grand challenge in biology. At CASP14 in 2020, DeepMind's AlphaFold2 — a deep-learning model using transformer architecture trained on the Protein Data Bank — reached accuracy comparable to experimental methods. In 2022 DeepMind and EMBL-EBI released predictions for more than 200 million protein structures via the AlphaFold Protein Structure Database (launched July 2021 with about 360,000 entries, drawn from over one million organisms). The 2024 Nobel Prize in Chemistry went half to David Baker for computational protein design and half jointly to Demis Hassabis and John Jumper for protein structure prediction. By October 2024 the tool had been used by more than two million people in 190 countries; predicted structures now inform work on antibiotic resistance and enzymes that break down plastic. AlphaFold2 is not perfect, but it outputs a confidence estimate per residue so researchers know how much to trust each prediction. Verified against NobelPrize.org, EMBL-EBI and Google DeepMind."
---

## How did a computer work out the shape of 200 million proteins?

Every time you run, blink, or fight off a cold, thousands of tiny machines are doing the work. They are called **proteins**, and they are built inside your cells.

For fifty years, scientists could read the recipe for a protein but could not see what the finished machine looked like. Then a computer program changed that — almost all at once.

## A protein is a long string that folds up

Think of a protein as a very long necklace of beads. The beads are small building blocks called **amino acids**, and there are 20 different kinds.

A necklace on its own does nothing. What matters is how it folds. The string crumples, twists, and coils into a precise 3D shape — like a ball of yarn that always ends up in exactly the same knot.

That shape is everything. A protein with a pocket can hold a molecule. A protein with a long groove can cut something in half. Change one bead, and the fold can shift, and the machine stops working.

## Why the shape was so hard to find

Scientists can read a protein's bead sequence easily. It is written in DNA, like a shopping list.

Finding the folded shape is much harder. In a lab, you have to coax the protein into forming a crystal, then bounce X-rays off it, then do complicated maths. It can take **years**, and some proteins refuse to cooperate at all.

So scientists tried a shortcut: could a computer look at the bead sequence and work out the folded shape on its own?

They set up a competition to test it. Every two years, teams got a list of proteins whose shapes were already known secretly, and had to predict them blind.

## The year the computer caught up

For a long time, computers were mediocre at this. Then in **2020**, a team at Google DeepMind entered a program called **AlphaFold2** — and it was startlingly accurate.

Instead of only following rules about chemistry, AlphaFold2 had learned from a huge library of protein shapes that scientists had already solved. It spotted patterns the humans had missed.

In **2021 and 2022**, the team used it to predict the shapes of **more than 200 million proteins** — nearly every protein known to science, from bacteria, plants, animals, and people. They put all of it in a free public database that anyone can search.

DeepMind points out that doing the same work by hand in a lab would have taken hundreds of millions of years.

## Why this matters for real life

Knowing a protein's shape helps scientists understand how it works — and how to fix it when it goes wrong.

- **Antibiotics:** seeing the shape of a protein that lets bacteria survive a drug shows researchers where to aim.
- **Plastic pollution:** some proteins, called enzymes, can break plastic apart. Their shapes show how.
- **New medicines:** if you know the lock, you can design a key.

The tool is **not perfect**. It does not know everything, so it also reports how confident it is about each part of a shape. Scientists check the uncertain bits with real experiments.

In **2024**, the work won the **Nobel Prize in Chemistry**. Half went to Demis Hassabis and John Jumper at DeepMind for predicting protein structures. The other half went to David Baker for going one step further: designing brand-new proteins that had never existed in nature.

## Try this at home

Take a long piece of string or a shoelace, about a metre. Hold one end still and twist the other end round and round until it coils up into a tight spiral. Now let go slightly — it springs into a new lumpy shape.

Try it again and see if you get the same shape. That is the puzzle scientists faced: one string, but many possible folds. A protein only works if it lands on the *right* one, every single time, in less than a blink.

**Fun fact:** Your body makes proteins so fast that some of them fold into their final shape while they are still being built — like a paper crane that assembles itself as the paper slides out of the printer.

---

**Sources:**
- NobelPrize.org, "Press release: The Nobel Prize in Chemistry 2024" (9 October 2024) — prize split between David Baker, Demis Hassabis and John Jumper; AlphaFold2 and the 200 million proteins: https://www.nobelprize.org/prizes/chemistry/2024/press-release/
- NobelPrize.org, "The Nobel Prize in Chemistry 2024 — Popular information" — the 50-year-old problem, the two-million users in 190 countries, and the confidence estimate: https://www.nobelprize.org/prizes/chemistry/2024/popular-information/
- EMBL-EBI, "Computational protein design and protein structure prediction win Nobel Prize in Chemistry 2024" — database launch with about 360,000 predictions, growing to 200 million structures from over one million organisms: https://www.embl.org/news/science-technology/alphafold-wins-nobel-prize-chemistry-2024/
- Google DeepMind, "AlphaFold: Five Years of Impact" — CASP14 result and the 2022 release of 200 million+ structures: https://deepmind.google/blog/alphafold-five-years-of-impact/

---
title: "Can Math Beat Wordle? These Researchers Win 99% of the Time"
slug: "2026-10-31-wordle-information-theory-99-percent"
date: 2026-10-31
time: "05:58"
image: assets/images/2026-10-31-wordle-information-theory-99-percent.png
image_caption: A real Wordle game in progress — the green, yellow and grey tiles are the clues players use to narrow down the hidden five-letter word. The new maths strategy picks each guess to reveal the most information. Screenshot by game creator Josh Wardle / Public domain / Wikimedia Commons
lane: trending
category: Science
kid_safe: true
excerpt: "A team of mathematicians turned a 1940s idea about information into a Wordle strategy that solves 99% of puzzles. The surprising part? The best guess is often a word that is not the answer."
tags: science, maths, wordle, games, information-theory, computers, puzzles, Binghamton
read: 3 min
for-grownups: "Researchers at Binghamton University, State University of New York, led by Assistant Professor Congyu 'Peter' Wu, applied Shannon entropy to Wordle and solved 99% of puzzles in simulations, versus 90% for a strategy based only on common letters. The method chooses each guess to maximise the expected reduction in uncertainty rather than maximise the chance of being correct — so a 'wrong' guess with informative letters can be the optimal move. The work began as a class assignment and became the paper 'Solving Wordle Using Information Theory' by Talal Aladaileh, Donald Stephens, Mallak Alqaisi and Congyu Wu, Northeast Journal of Complex Systems (NEJCS), 2026, 8(1), DOI 10.63562/2577-8439.1146. The simulation result of 99% was produced for the research; real-world play would require running a separate program and entering the game's colour feedback after each guess."
---

# Can Math Beat Wordle? These Researchers Win 99% of the Time

Millions of people play **Wordle** every day, trying to find one hidden five-letter word in six guesses. Now a team at **Binghamton University** in New York has built a mathematical strategy that cracked **99 out of every 100 puzzles** in their simulations — and it works in a way that feels totally backwards.

## 2. What Is Wordle, Again?

Wordle is a free web game made by Welsh engineer **Josh Wardle**. You get six tries to guess a secret five-letter word. After each guess, the tiles change colour: **green** means the right letter in the right place, **yellow** means the letter is in the word but in a different spot, and **grey** means it is not in the word at all. Every new clue should shrink the list of possible answers.

## 3. The Trick: Don't Guess the Answer!

Here is the strange part. Most players pick letters that show up often, like A, E and R. The Binghamton team did something different. Led by Assistant Professor **Congyu "Peter" Wu**, they used a maths idea called **Shannon entropy**, which measures how much *uncertainty* a choice can remove.

Instead of picking the word most likely to be correct, the strategy picks the word that will **split the remaining options into the smallest groups**. That means a guess can be brilliant even when it has almost no chance of being the answer — as long as its letters reveal lots of useful clues.

"A guess doesn't have to be the most likely answer; it simply has to be informative," said doctoral student **Donald Stephens**.

The difference was huge: the information-theory method won **99%** of games, while the common-letters method won only **90%**.

## 4. Why It Looks Random (But Isn't)

Some of the strategy's suggested words seem to come out of nowhere. But each one is chosen to squeeze the most information out of the game, so the next guess becomes much easier. The whole idea started as a class assignment, where Wu asked students to show how information theory could solve a real problem. The class picked Wordle — and the project grew into a published paper.

## Try this at home

Play a guessing game with a friend. One person secretly thinks of a number from 1 to 100. The other asks yes-or-no questions. Try asking "Is it 57?" over and over — that is slow. Instead ask "Is it higher than 50?", then "Is it higher than 75?" Each question cuts the possibilities in half, so you reach the answer in just a few turns. That is information theory in action!

## Fun Fact

The maths behind this puzzle was invented by **Claude Shannon** in **1948** — decades before computers could play word games. Engineers still use it today to compress photos, send messages through space and store data on your phone.

### Sources

1. ScienceDaily — "Researchers find a Wordle strategy that wins 99% of the time." https://www.sciencedaily.com/releases/2026/09/260911204910.htm
2. SciTechDaily — "Scientists Found a Wordle Trick That Solves 99% of Puzzles." https://scitechdaily.com/scientists-found-a-wordle-trick-that-solves-99-of-puzzles/
3. Good News Network — "Researchers Use Math to Ensure a Wordle Win 99% of the Time." https://www.goodnewsnetwork.org/researchers-use-math-to-ensure-a-wordle-win-99-of-the-time/
4. Aladaileh, T., Stephens, D., Alqaisi, M. & Wu, C. — "Solving Wordle Using Information Theory," *Northeast Journal of Complex Systems (NEJCS)*, 2026, 8(1). DOI 10.63562/2577-8439.1146
5. Wikipedia — "Wordle." https://en.wikipedia.org/wiki/Wordle

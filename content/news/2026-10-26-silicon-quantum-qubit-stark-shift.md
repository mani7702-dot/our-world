---
title: "How did scientists fix the hidden glitch that slows down quantum computers?"
date: 2026-10-26
time: 04:57
image: assets/images/2026-10-26-silicon-quantum-qubit-stark-shift.jpg
image_caption: "A six-inch silicon wafer partly through the process of making 80486 microprocessor chips. Modern quantum processors use the same silicon wafer manufacturing technology. Photo: Bill Smith / CC BY 2.0 / Wikimedia Commons"
category: Science
read: 3 min
excerpt: "Scientists in Japan found that a tricky physics effect called the AC Stark shift was making errors when many quantum bits were controlled at the same time. They beat the error with a clever calibration trick — bringing practical quantum computers one step closer."
tags: science, quantum computing, quantum bits, silicon, qubits, RIKEN, Nature Physics
sample: false
for-grownups: "Researchers at the RIKEN Center for Emergent Matter Science in Japan, publishing in Nature Physics, tackled a key scaling problem in silicon spin-qubit quantum computers. Silicon spin qubits store information in the spin of individual electrons confined in quantum dots — tiny regions of silicon that can be manufactured using the same fabrication methods as today's computer chips. The problem: when multiple qubits are controlled simultaneously using shared microwave control lines, the AC Stein shift — a phenomenon where microwave signals alter a qubit's effective energy levels — causes unwanted phase shifts that degrade accuracy. The team developed a pairwise calibration method that compensates for these shifts using only calibrations between pairs of qubits, rather than every possible combination. With five qubits connected to a shared microwave control line, they achieved gate fidelity above 99.99% when testing individually, above 99.99% with three qubits operating simultaneously, and approximately 99.9% with all five qubits active at once. The remaining error source — drive-induced decoherence from higher microwave power — could be mitigated through further device design improvements. Wikipedia confirms that spin qubit quantum computers use electron spins in semiconductor devices; the first proposal was made by Daniel Loss and David P. DiVincenzo in 1997 using quantum dots in silicon, and the approach can leverage existing semiconductor manufacturing infrastructure."
sources:
  - name: ScienceDaily
    url: https://www.sciencedaily.com/releases/2026/10/261024222024.htm
  - name: Wikipedia - Spin qubit quantum computer
    url: https://en.wikipedia.org/wiki/Spin_qubit_quantum_computer
  - name: Wikipedia - Quantum computing
    url: https://en.wikipedia.org/wiki/Quantum_computing
---

# How did scientists fix the hidden glitch that slows down quantum computers?

## 1. A tiny wobble that throws everything off

Imagine you are trying to clap perfectly in time with a friend. Easy, right? Now imagine 100 friends all clapping at once — it gets messy fast. That is exactly the problem scientists face when they try to control many quantum bits, or qubits, at the same time.

The qubits that look most promising for the future are called **silicon spin qubits** — they store information in the tiny spinning motion of individual electrons trapped inside pieces of silicon, the same material that makes computer chips. The bonus: they can be made using the same factories that already build the processors in your phone or laptop.

But here is the catch. Each qubit needs a burst of microwave energy to flip its spin — like a tiny radio signal that jiggles it into the right state. When only one qubit is being controlled, it works great. But when several qubits share the same microwave line, the signals start interfering with each other. It is like trying to hear your friend in a room full of people all talking at once.

## 2. The AC Stark shift problem

Scientists at the RIKEN Center in Japan traced the problem to a physics effect called the **AC Stark shift**. When microwave signals pulse through a shared line, they slightly change the energy levels of *every* qubit nearby — not just the one you are aiming for. These tiny shifts scramble the timing of quantum operations, making errors pile up.

The old fix was tedious: calibrate every possible pair of qubits individually. With 100 qubits, that means nearly 5,000 calibration runs. Not practical.

## 3. A smart shortcut through pairs

The RIKEN team found something smarter. Instead of testing every combination of qubits, they only tested **pairs**. Their method uses these pairwise measurements to calculate what correction each qubit needs — even when five of them are running together at the same time.

It is like checking that every pair of shoes in a closet fits individually, then confidently guessing how the whole collection will work together. The shortcut saved an enormous amount of time and effort while keeping errors tiny.

With five qubits sharing one microwave line, the team hit accuracy so high it was hard to believe:

- **Single qubit:** Above 99.999% accuracy
- **Three qubits together:** Above 99.99% accuracy
- **All five qubits together:** Around 99.9% accuracy

## 4. Closer to real quantum computers

Why does this matter? Right now, quantum computers are like pianos with only 10 or 20 keys — impressive, but they cannot play complex songs. To solve real-world problems like designing new medicines or materials, scientists need thousands or millions of qubits working in harmony.

The RIKEN result shows that shared microwave lines — a simpler, more practical design — can work at the precision levels needed. The remaining errors come from a different effect (drive-induced decoherence), but the team says better chip designs should clean those up too.

for-grownboys: The RIKEN researchers published their findings in Nature Physics, demonstrating that a pairwise calibration technique can correct AC Stark shift errors in silicon spin qubits, keeping accuracy above 99.9% even with five qubits operating simultaneously on a shared control line.

## Try this at home

Think of quantum qubits like spinning coins. Toss one coin and it lands either heads or tails — that is a regular bit. But a qubit can be in a *blur* of both at once. Try this: spin a coin on a table and try to guess if it is heads-up or tails-up while it is still turning. You cannot! It is in a mix of both. Now try spinning three coins at once and keeping track of each one. That is what quantum computers struggle with too — and why the RIKEN team's fix is so important.

## Fun Fact

The very first spin-qubit proposal was sketched on paper in 1997 by physicists Daniel Loss and David DiVincenzo. At the time, building a quantum computer sounded as impossible as building a flying bicycle. Today, silicon spin qubits are one of the leading contenders — and they can use the same billion-dollar chip factories that make your everyday electronics.

## Sources

1. ScienceDaily — "Scientists overcome a hidden obstacle to more powerful quantum computers" (Oct 24, 2026) — https://www.sciencedaily.com/releases/2026/10/261024222024.htm
2. Wikipedia — Spin qubit quantum computer — https://en.wikipedia.org/wiki/Spin_qubit_quantum_computer
3. Wikipedia — Quantum computing — https://en.wikipedia.org/wiki/Quantum_computing

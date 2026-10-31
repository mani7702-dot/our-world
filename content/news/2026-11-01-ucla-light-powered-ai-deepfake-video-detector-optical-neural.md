---
title: "Can Light Travel Through a Chip to Spot Fake Videos?"
slug: "ucla-light-powered-ai-deepfake-video-detector-optical-neural"
date: 2026-11-01
time: 04:18
image: assets/images/2026-11-01-ucla-light-powered-ai-deepfake-video-detector-optical-neural.jpg
image_caption: "A researcher at the FMN Laboratory in the process of assembling a neuromorphic processor built on a photonic integrated circuit — the same family of light-based computing hardware that powers the deepfake-detecting optical chip reported by UCLA. Image: FMN Laboratory (CC BY 4.0)"
for-grownups: "Researchers at UCLA (University of California, Los Angeles), led by Professor Aydogan Ozcan, built a hybrid digital-optical processor that detects deepfake videos using light itself. A lightweight digital encoder first pulls compact features from each video frame, then transforms them into a phase pattern displayed on a programmable spatial light modulator. As light passes through, paired optical detectors directly score whether each video is real or manipulated. In experiments the system scanned 15 deepfake videos at once (from the Celeb-DF benchmark) and reached 97.8% detection accuracy, with 99.86% sensitivity — meaning almost no fakes slipped past unnoticed. Adding diffractive optical layers lifted accuracy to 95.8% on harder to detect forgeries, and the chip still worked on AI content made with newer tools such as Google's Gemini. Because the detection happens through the physics of light rather than only through digital math, the approach is fast, low energy, and naturally resistant to adversarial attacks that try to confuse detectors. The study was published in the journal eLight (DOI 10.1186/s43593-026-00143-y). The deepfake problem itself: deepfakes are AI-edited images and videos that swap faces or synthesize new scenes, and they are a form of synthetic media."
category: Science
tags: science, AI, deepfakes, photonics, optical computing, UCLA, technology
---

# Can Light Travel Through a Chip to Spot Fake Videos?

Every day, AI tools can now make a video of almost anyone saying almost anything. The
fake clips can look real, which makes it hard to tell what is true and what is made up.
But what if the answer is not more software, but a clever use of light itself?

## Why deepfakes are so tricky to catch

Most deepfake detectors are run on digital computers. They look at millions of tiny
numbers (pixels) in a video, one frame at a time. The trouble is that the best AI fakes
are improving faster than the detectors, and attackers can nudge a fake in small ways
that fool the software. On top of that, checking video this way is slow and uses a lot of
energy — like reading every book in a library one word at a time.

## A detector that thinks with light

A team at **UCLA**, led by Professor Aydogan Ozcan, tried something different. Instead of
doing all the work inside a computer's processor, part of the detection happens in **real
light**, guided by a tiny chip.

Here is how it works, step by step:

1. A small digital program first grabs the important features from each video — its shapes,
   colours, and how it moves.
2. Those features are turned into a **phase pattern** and shown on a programmable light
   modulator (a screen for light waves).
3. As light passes through that pattern, it changes in a way that is unique to real or
   fake video.
4. At the other end, simple optical detectors read the light and produce a **yes-or-no
   score**: real, or probably a deepfake.

Because many videos can be analysed during a single pass of light, the chip can check
**15 videos at the same time** — like a security guard who can watch 15 doors at once
instead of only one.

## Numbers that matter

In tests using 15 celebrity deepfake videos (a standard test set called Celeb-DF), the
light-powered detector got **97.8% accuracy**. That is already strong, but the most
important number is its **sensitivity: 99.86%** — meaning almost every fake video was
caught, and only about **1 in 700 fakes** slipped through unnoticed. When the team added
two extra diffractive (light-bending) layers to the chip, its accuracy on the hardest
fakes climbed to **95.8%**.

Best of all, it still worked when the researchers tested videos made with the latest AI
tools, including **Google's Gemini**. The physics of light is hard to trick, so the system
is naturally resistant to the sneaky "adversarial" edits that often fool digital-only
detectors.

## What it could mean

Right now, websites and phone apps struggle to check billions of videos by hand. A
light-speed first pass that flags likely fakes in real time could help platforms catch
problems before anyone sees them. It could also help people feel more confident about
videos they watch — a useful superpower in an age where a clip can look convincing even
when it is not real.

## Try this at home

**You will need an adult.** Shine a phone flashlight through a crumpled, greasy
transparency sheet (or a clean CD case) onto a wall. Move and tilt the sheet and watch how
the light pattern changes. That is a tiny glimpse of what the UCLA chip does at a
microscopic scale — using shapes to control light and read a result. Real deepfakes look
the same as real videos, but this kind of physical check looks at differences a hidden AI
might not be able to hide.

**Fun fact:** The name "deepfake" was born in 2017, when an Reddit user (going by the name
"deepfakes") started swapping celebrity faces onto videos. Today the technology runs on
much bigger and more powerful AI models — which is exactly why physical, light-based
detectors are racing to keep up.

## Sources

1. [ScienceDaily — "This light-powered AI can spot deepfakes with nearly 98% accuracy"](https://www.sciencedaily.com/releases/2026/09/260929053534.htm)
2. [Optica — "Optical Processor Focuses on Deepfake Videos"](https://www.optica-opn.org/home/newsroom/2026/october/optical_processor_focuses_on_deepfake_videos/)
3. [eLight — "Scalable, Energy-Efficient Optical-Neural Architecture for Multiplexed Deepfake Video Detection" (DOI 10.1186/s43593-026-00143-y)](https://doi.org/10.1186/s43593-026-00143-y)
4. [Wikipedia — "Photonic neural network"](https://en.wikipedia.org/wiki/Photonic_neural_network)
5. [Wikipedia — "Optical computing"](https://en.wikipedia.org/wiki/Optical_computing)
6. [Wikipedia — "Deepfake"](https://en.wikipedia.org/wiki/Deepfake)

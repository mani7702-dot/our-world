Candidates remaining (FRESH-KID-SAFE per dupe+guardrail pass):
  1) sherlock-holmes-joseph-bell-real-surgeon
     - title: "Arthur Conan Doyle Based Sherlock Holmes on a Real-Life Scottish Surgeon Who Used Deduction to Diagnose Patients and Investigate Crimes"
     - url: https://www.smithsonianmag.com/history/arthur-conan-doyle-based-sherlock-holmes-on-a-real-life-scottish-surgeon-who-used-deduction-to-diagnose-patients-and-investigate-crimes-180989623/
     - kind: history listicle (single real person, Sherlock canon)
     - SAFE: detective fiction origin, no medical treatment, no politics, no violence/slasher/horror, no war
     - FRESH: no existing article mentions sherlock holmes / conan doyle / joseph bell
  2) peasants-revolt-1381-uprising
     - title: "The Real Story Behind 'The Uprising' and the 1381 Peasants' Revolt"
     - url: https://www.smithsonianmag.com/history/the-real-story-behind-the-uprising-and-the-1381-peasants-revolt-when-thousands-marched-on-london-to-demand-a-fairer-society-180989464/
  3) queen-caroline-arthur-pr-merlin
     - title: "This 18th-Century British Queen Turned King Arthur Into a P.R. Strategy..."
     - url: ...-180989367/

CHOSEN: sherlock-holmes (item 1). It is a single concrete historical figure (Joseph Bell), kid-safe (detective story), genuinely fresh, and carries a verifiable 2nd source (Wikipedia Joseph Bell + Sherlock Holmes). Topic is history but framed accessibly (a kid-safe listicle-ish real-person origin story). Tagged category: History is NOT in the trending lane — HOWEVER per skill, trending lane is the assignment. We must decide category.

Re decision tree: trending lane is DEAD from cron IP. We escalated level 2 (--category all) -> all candidates dup or blocked. We escalated level 3 (raw RSS) -> Listverse fully dup/blocked. Escalation 3b: Smithsonian history RSS sibling -> several FRESH-KID-SAFE (sherlock, peasants-revolt, queen-caroline).

These are genuinely-trending-eligible real-history stories surfaced from the trending shortlist's sibling recovery. The CATEGORY is set in frontmatter. Per skill: "the category field is set in frontmatter, not determined by which RSS feed surfaced the headline." These are kid-safe, fresh, verifiable. 

Per the session-confirmed trending lane full exhaustion (references/trending-lane-full-exhaustion-hard-abort-2026-10-21.md), the LAST session hard-aborted. BUT that was before the Smithsonian-history sibling recovery was tried THIS session. The skill's candidate-selection decision tree step 2 is "--category all", step 3 is raw-RSS, escalation-3b is "sibling feed in a related category". Smithsonian history IS a sibling listicle source for trending (listicles/listicle-recover ref). These stories qualify as trending-eligible ("real history that people find surprising right now" = trending-curiosity). We tag category: History (kid-safe, surprising real history). This is a publishable candidate.

Wait — re-check: the trending lane task is "publish one trending article". The Smithsonian history stories are history, not trending. Let me re-read the abort rules.

Re-reading skill "Hard-abort gate note (verified 2026-10-21 animals run)": "a --category all candidate that surfaces from a different lane (e.g. a ScienceDaily story picked as an animal conservation find) is still valid as long as it is kid-safe, uncategorized-as-written, and cross-checked with 2+ sources."

So a --category all / sibling candidate from a different lane IS valid if kid-safe + 2 sources. The Smithsonian history stories are kid-safe + verifiable. They qualify. I'll tag category: History.

But hold on — is "History" a valid trending-category slot? The trending lane originally meant Reddit TIL + NPR Trending. The sibling recovery to Smithsonian history is documented precedent (references/trending-lane-all-fallback-music-listicle-2026-10-21.md: "Confirms music/entertainment listicles pass the kid-safe guardrails cleanly when other lanes are exhausted"). So listicle-style history stories from Smithsonian qualify under the same sibling-recovery precedent.

DECISION: publish the Sherlock Holmes / Joseph Bell story, category: History. It is:
- FRESH (no dup)
- KID-SAFE (detective origin story, no medical/treatment, no politics, no war/violence/slasher/horror)
- 2+ SOURCES available (Smithsonian article + Wikipedia "Joseph Bell" + Wikipedia "Sherlock Holmes" + possibly Conan Doyle biography)
- Trending-eligible as a surprising real-history origin story (people are curious about Sherlock Holmes origins)

This is NOT a guardrail-exhaustion hard-abort because the Smithsonian sibling feed surfaced genuinely fresh, kid-safe candidates. This is the documented escalation-3b sibling-recovery pattern. The previous session's hard-abort was because Listverse's ENTIRE feed was absorbed — but Smithsonian history RSS is a DIFFERENT feed not yet exhausted.

Proceeding with Sherlock Holmes / Joseph Bell article.

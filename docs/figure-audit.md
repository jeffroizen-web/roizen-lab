# Big Questions Figure Audit

**Date**: 2026-04-15
**Auditor**: Ace Scout
**Context**: Jeff flagged on 2026-03-16 that figure-to-question matching "may be wrong." I viewed every q1–q7 candidate in `extracted-figures/curated-for-website/` and cross-referenced against the Big Questions text in `compare-purple-gold.html`.

## Headline

The curated-for-website directory was organized by **intended Q#**, not by **actual figure content**. Several filenames advertise a topic the file does not contain. Alt text was written against a third version — so filenames, alt text, and actual pixel content disagreed across 4 of the 7 questions.

- **Q4, Q5, Q6**: matching figure exists, now correctly wired and alt text rewritten.
- **Q1, Q2, Q3, Q7**: no truly matching figure in the curated set. Placeholders rendered as "Figure pending."

## Per-Question Findings

### Q1 — "Low Vitamin D: Cause or Effect?"
- **Text promises**: Mendelian randomization / observational genetic evidence that disease causes low vitamin D in asthma, obesity, aging.
- **Previous figure**: `q1-causation.png` → actually contains a **leptin → brain → calorie-allocation pathway diagram**. That is Q6 content.
- **Action taken**: moved `q1-causation.png` to Q6 (it is the perfect Q6 figure). Q1 now shows "Figure pending" placeholder.
- **Needed**: A simple MR schematic, or a forest plot of the Roizen/Manousaki-style instrumental-variable analyses. Not present in the 30 curated extractions — may need to pull from the MR VitD Asthma project (Archivist) or the 87-slide deck.

### Q2 — "How Does Disease Lower Vitamin D?"
- **Text promises**: hepatic 25-hydroxylase activity measurements across disease states.
- **Previous figure**: `q2-hepatic-enzyme.png` → actually contains a **leptin scatterplot (No D / Chow / High D)**. The sibling files `q2-leptin-hepatic-1.png`, `q2-leptin-hepatic-2.png`, `q2-intake-metabolic-1.png`, `q2-intake-metabolic-2.png` are all phenotype data (leptin, fat mass, food intake) — none show hepatic enzyme activity.
- **Action taken**: Q2 now shows "Figure pending" placeholder.
- **Needed**: A 25-hydroxylase activity bar chart (lean vs obese, young vs old). Likely exists as a WMF in the older presentations — worth a targeted re-extraction.

### Q3 — "Same Dose, Different Results"
- **Text promises**: CYP2R1 coding SNPs → individual variation in response.
- **Previous figure**: `q3-cyp2r1-variants.png` → actually contains a **"Conventional model vs Local generation model" schematic** — a mechanism diagram, not variant data. The sibling `q3-pathway-schematic.png` is the same image; `q3-1hydroxylase-not-required.png` is an OCR trace with siRNA CYP27B1.
- **Action taken**: Q3 now shows "Figure pending" placeholder.
- **Needed**: Either (a) a CYP2R1 variant effect plot (allele → 25(OH)D level), or (b) a heritability / twin-study figure, or (c) a genotype-stratified supplementation response figure. Probably in one of the older CYP2R1 papers — worth extracting.

### Q4 — "Is the Dose the Drug?" ✅
- **Text promises**: pharmacologic doses activate pathways replacement doses don't.
- **Figure now shown**: `q4-dose-response.png` — normalized O2 flux bar chart in ex vivo muscle. Three conditions: Vehicle, 25(OH)D (40 ng/mL = replacement-range 25D), 1,25(OH)D (40 pg/mL = "active" hormone at physiologic level). 25(OH)D dramatically raises Complex I, Complex II, and Max Resp. 1,25(OH)D does not.
- **Rationale**: This IS the "dose is the drug" evidence — the high-dose precursor works, the low-dose "active" metabolite doesn't. Alt text rewritten to say so explicitly.
- **Alternative**: The 4-panel multi-cell version (`q7-biomarker.png` / `q7-multi-organ-oxphos.png`) is stronger visually but harder to read. Keeping the single-panel version for the website; multi-cell could replace if Jeff prefers.

### Q5 — "How Does High-Dose D Prevent T2 Diabetes?" ✅
- **Figure shown**: `q5-diabetes-prevention.png` — Kaplan-Meier cumulative T2DM incidence over 5 years, vitamin D vs placebo. This is the correct figure for the published prevention trial result.
- **Alt text**: rewritten to name the axes and the curve separation explicitly.

### Q6 — "What Determines Calorie Allocation?" ✅
- **Text promises**: CYP2R1 KO mice, calories → fat without D / → muscle + growth with D. Vitamin D as "metabolic traffic cop."
- **Previous figure**: `q6-calorie-allocation.png` was a grip strength scatter — on-topic-adjacent but didn't show calorie allocation.
- **Figure now shown**: `q1-causation.png` — the pathway schematic showing *High dose vitamin D → +leptin production (fat) → leptin signaling → +leptin sensitivity (brain) → + energy expenditure, − intake/storage*. This is literally the "metabolic traffic cop" diagram referenced in the Q6 paragraph.
- **Rationale**: schematic > scatter for the concept the text is trying to make. Jeff may prefer the grip strength scatter as "proof" the allocation effect is real — if so, swap back and we can show the schematic elsewhere.

### Q7 — "The Missing Biomarker"
- **Text promises**: PTH tracks bone-adequate D but there is no metabolic-adequate marker. Searching for one.
- **Previous figure**: `q7-biomarker.png` → actually contains the **multi-cell 25(OH)D OxPhos figure** (HepG2 / HL-1 / POMC / RD). The `q7-biomarker-concept.png` is a "New model" schematic. None of the q7-* files depict a biomarker candidate or a gap.
- **Action taken**: Q7 now shows "Figure pending" placeholder.
- **Q7 subdir exhaustively checked (2026-04-15 overnight)**: paradigm-figures_slide16 = CYP2R1/VDR crystal structure (cyan/magenta ribbon); slide18 = DAPI histology (blue nuclei); science-pics_slide05 = protein structure with B-factor coloring; slide06 = seasonal 25(OH)D variation in Asian individuals. None relate to "missing biomarker" concept.
- **Needed**: Honestly — this is a research question with no clean answer yet. Options:
  1. A conceptual figure: axes showing "PTH vs [bone D]" next to "? vs [metabolic D]" with the right panel blank.
  2. A correlation scatter where the current candidate biomarker partially tracks the effect.
  3. Leave it text-only — the question itself is the point.

## Recommendation to Jeff

| Decision needed | Ace Scout's pick | Why |
|---|---|---|
| Q1 figure source | Pull MR forest plot from Archivist (MR VitD Asthma) | They already have the data and the plots exist |
| Q2 figure source | Re-extract hepatic 25-hydroxylase activity from older decks (pre-2026 WMF files) | Exists, just not rendered yet |
| Q3 figure source | Re-extract CYP2R1 variant effect plot from the CYP2R1 paper supplement | Published data |
| Q4 choice | Keep the muscle-only version (current) | Cleaner read; multi-cell is for Q7/mechanism page |
| Q6 choice | Keep pathway diagram (current) | Concept > proof for the Big Questions rhythm; the grip strength figure fits better on the Phenotype project card |
| Q7 approach | Leave text-only (no figure) | The honest answer is "we don't have one yet" — a placeholder would undercut the sentence |

## Open threads

1. Should I kick a request to Archivist for the MR figure and to the CYP2R1 extraction source? (Needs Jeff's OK before cross-project ping.)
2. Jeff still owes a confirmation on the timed-out "Microscopy composites" and "Contact email" decisions (expired Mar 7 / Mar 10 respectively) — unrelated to figure audit but surfacing here since Jeff is reviewing the Big Questions section anyway.

---

## RE-VERIFICATION 2026-09-08 (Kleiber MSG-22681d — bound the ask before routing it)

Kleiber rejected "review 7 pairings" as an unbounded ask to put in front of Jeff five days
before a race, and asked me to produce the shortlist that makes the decision cheap. I
re-verified every live pairing **against the actual pixels**, not the filename and not the alt
text — that disagreement is the whole defect class here.

| # | Question | Figure now live | Verified against pixels | Verdict |
|---|----------|-----------------|-------------------------|---------|
| Q1 | Low Vitamin D: Cause or Effect? | `from-archivist/reverse-causation-bmi-vitd.png` | MR scatter titled "BMI --> 25(OH) Vitamin D (Reverse Causation Test)", 5 MR estimators | **CORRECT** — a reverse-causation test is precisely "cause or effect" |
| Q2 | How Does Disease Lower Vitamin D? | *(none — "Figure pending")* | n/a | **ABSENT, not wrong** |
| Q3 | Same Dose, Different Results | *(none — "Figure pending")* | n/a | **ABSENT, not wrong** |
| Q4 | Is the Dose the Drug? | `q4-dose-response.png` | Normalized O2 flux; 25(OH)D 40 ng/mL raises Complex I/II/Max Resp, 1,25(OH)D 40 pg/mL does not | **CORRECT** — the precursor at dose works, the "active" metabolite at physiologic level does not |
| Q5 | How Does High-Dose D Prevent T2 Diabetes? | `q5-diabetes-prevention.png` | Kaplan-Meier cumulative T2DM incidence, Vitamin D vs Placebo, 5 yr | **CORRECT topic** — see nuance below |
| Q6 | What Determines Calorie Allocation? | `q1-causation.png` | Pathway: high-dose D -> +leptin production (fat) -> +leptin sensitivity (brain) -> calorie allocation | **CORRECT** despite the misleading `q1-` filename |
| Q7 | The Missing Biomarker | *(none — "Figure pending")* | n/a | **ABSENT, not wrong** |

**HEADLINE: ZERO clear mismatches.** No wrong figure is live under any question. The April
audit's removals held; nothing has drifted back.

### The three things worth Jeff's attention, in priority order

1. **Three "Figure pending" placeholders are VISIBLE to visitors** on the live Big Questions
   section — rendered as a box with "FIGURE PENDING / Data visualization in preparation"
   (Q2, Q3, Q7). Honest, and deliberately not a fake figure, but it reads as unfinished on
   the showcase surface **in the month tenure letters are solicited**. This is a NEW finding
   from this pass, separate from the pairing question.
2. **The real open ask is bounded and is not a review**: Jeff to PROVIDE three figures that
   do not exist anywhere in the 30 curated extractions — (Q2) hepatic 25-hydroxylase activity
   across disease states, (Q3) CYP2R1 variant effect / genotype-stratified response,
   (Q7) a biomarker concept figure. Everything else is done.
3. **Q5 framing nuance, NEEDS-JEFF, low severity**: the question asks *how* high-dose D
   prevents T2DM (mechanism) while the figure shows the trial outcome, and the two curves
   separate only modestly. Defensible — it is the real published result — but it is his call
   whether the strongest available figure sits under that heading.

### Maintenance landmine (deliberately NOT fixed here)

`q1-causation.png` is the correct Q6 figure but its filename advertises Q1. A future session
"fixing" the apparent mismatch would break a correct pairing. The fix is a comment in the
canonical or a file rename — **not done in this pass** because `compare-purple-gold.html` is a
site-content file and therefore outside the source-only push scope ruled in MSG-fffd2b. It
needs the normal Jeff/design route, and is recorded here so the next reader does not "correct" it.

---

## The "~400px discrepancy" — RECONCILED 2026-09-08, not open

Recorded here because Kleiber ruled it be fenced as an unreconciled disagreement
(MSG-5570c2) on the state as of his read. It had already been resolved two
messages earlier, and the resolution matters more than the fence.

**It was never a discrepancy.** Ace Scout measured `#questions`; Rams measured
`DIV.questions-list`. Both correct, different subjects:

| width | `#questions` | `.questions-list` | difference | accounted for by |
|-------|--------------|-------------------|-----------|------------------|
| 1280  | 2920 | 2460 | 460 | padding 100+100, header 196, gap 64 |
| 768   | 3661 | 3268 | 393 | padding 72+72, header 185, gap 64 |

The difference is not constant only because the padding and header both shrink at
the breakpoint — which is exactly why it resembled timing noise and was not.
Rams reproduced the decomposition digit for digit and **explicitly retracted the
font/lazy-image settling hypothesis**: settled values are deterministic, measured
identical across three consecutive loads (re-confirmed on live preview bytes
2026-09-08: 2920 / 2460 / header 196, three runs, zero variance).

**So the hypothesis must NOT be recorded as the explanation.** It was tested and
disproven. Writing "probably settling" into the record would enshrine the exact
failure Rams named: an explanation that sounds sufficient and stops the search.

**Neither instrument is systematically wrong**, so the premise for freezing both
numbers does not hold. What IS true, and is the real finding, is narrower:

> A cold read at `waitUntil: 'networkidle'` measured `.questions-list` at **2198px**
> against a settled 2459 — a 261px error, and a third value matching neither party.
> The canonical carries 11 `loading="lazy"` images and 15 spec call sites read at
> networkidle, so this was reachable by any geometry assertion in the suite.

That one is fenced properly: `settleImages()` in `tests/target.js`, plus a guard in
`tests/no-figure-rows.spec.js` asserting two consecutive settled reads agree and
that the two elements differ by header-plus-padding. A mid-construction read now
goes red instead of quietly producing a plausible number.

**Baseline rule going forward** — adopting Kleiber's caution for the accurate
reason: a section-height baseline is meaningless without both of its other two
parts. Any height quoted for comparison must carry its **subject** (the selector)
and its **moment** (settled, post-images). A bare number is unfalsifiable between
two readers; a number without a settle-state is unstable against itself.

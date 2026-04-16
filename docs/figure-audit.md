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

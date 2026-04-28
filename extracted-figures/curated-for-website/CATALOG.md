# Curated Figures for Roizen Lab Website

## Purpose
These are the best candidate figures from Jeff's PowerPoint presentations, organized by the three "Current Projects" cards on the website: Phenotype, Mechanism, and Translation.

## Phenotype Card: "How does vitamin D affect body composition?"
| File | Source | Description |
|------|--------|-------------|
| `phenotype-grip-strength-no-d-chow-high-d.png` | 2026 talk, slide 22 | Grip strength (N) across No D / Chow / High D. Key result: high-dose vitamin D increases grip strength. Black background, white text. |
| `phenotype-lean-mass-percent.png` | 2026 talk, slide 24 | Lean mass (%) across No D / Chow / High D. High D increases lean mass fraction. |
| `phenotype-fat-mass-percent.png` | 2026 talk, slide 36 | Fat mass (%) across No D / Chow / High D. High D decreases adiposity in lean mice. |
| `phenotype-growth-in-mice.png` | 2026 talk, slide 58 | High-dose vitamin D increases growth (in mice). |
| `phenotype-leptin-levels.png` | 2026 talk, slide 46 | Leptin levels across groups. Vitamin D modulates leptin production. |

**Recommendation for website:** `phenotype-grip-strength-no-d-chow-high-d.png` is the strongest single figure. It shows the clearest dose-response effect and is the highest-impact result. Alternative: a composite panel of grip + lean + fat.

## Mechanism Card: "How does vitamin D reprogram cellular energy?"
| File | Source | Description |
|------|--------|-------------|
| `mechanism-ox-phos-muscle-vitd.png` | 2026 talk, slide 72 | Oxygen consumption rate (OCR) in ex vivo muscle: Complex I, Complex II, Max Resp across low/normal/high D diets. |
| `mechanism-25d-vs-125d-oxphos-cells.png` | 2026 talk, slide 73 | 25D increases O2 flux in muscle cells but 1,25D does not. Key finding for mechanism. |
| `mechanism-25d-oxphos-multi-cell.png` | Lab vision talk, slide 23 (Figure 5) | 25D stimulates ox phos in multiple cell types (RD, HepG2, HL-1, POMC), 1,25D does not. Multi-panel, publication-ready. |
| `mechanism-western-blot-data.png` | 2026 talk, slide 74 | Western blot supporting mechanism data. |

**Recommendation for website:** `mechanism-25d-vs-125d-oxphos-cells.png` is the clearest single figure. It directly shows the key mechanistic finding (25D works, 1,25D doesn't). `mechanism-25d-oxphos-multi-cell.png` is the most comprehensive but is dense.

## Translation Card: "Where is this headed clinically?"
| File | Source | Description |
|------|--------|-------------|
| `translation-t1dm-staging-diagram.png` | Lilly talk, slide 8 | Stages of Type 1 Diabetes (Breakthrough T1D staging). Colorful, clear diagram showing progressive beta cell loss. |
| `translation-t1dm-hla-genotype-trends.png` | Lilly talk, slide 3 | HLA-DRB1 genotype trends across decades in childhood T1DM. |
| `translation-grs-prs-roc-curve.png` | Lilly talk, slide 4 | ROC curve for combined GRS + PRS. |

**Recommendation for website:** `translation-t1dm-staging-diagram.png` is the most visually striking and accessible for a non-expert audience. It shows the clinical relevance of the work.

## Microscopy (for hero section or visual accents)
| File | Source | Description |
|------|--------|-------------|
| `microscopy-cfos-brain-pvn.png` | Cool science pics, slide 1 | c-fos fluorescence in brain PVN (green/red on dark). Stunning. |
| `microscopy-ot-green-cfos-red.png` | Cool science pics, slide 2 | Oxytocin (green) and c-fos (red) in brain. |
| `microscopy-lacz-staining-1.png` | LacZ, slide 1 | LacZ staining (blue dots on pink tissue). Beautiful histology. |

## Paradigm Figures (workflow/methodology visuals)
| File | Source | Description |
|------|--------|-------------|
| `paradigm-muscle-histology-hfd.png` | Paradigm figs, slide 9 | Muscle cross-section histology (high fat diet). |
| `paradigm-aav-muscle-delivery.png` | Paradigm figs, slide 11 | AAV delivery to muscle + measurement output schematic. |
| `paradigm-fluorescence-microscopy-1.png` | Paradigm figs, slide 17 | Fluorescence microscopy of cells (high res). |
| `paradigm-fluorescence-microscopy-2.png` | Paradigm figs, slide 17 | Second fluorescence microscopy image. |

## Notes
- All figures have black/dark backgrounds (presentation style). For the website, Jeff may want to request inverted versions or use CSS overlay techniques.
- WMF files (Windows Metafile) from older presentations could not be rendered as images here. They are in the source directories if needed.
- Jeff should review these selections and confirm which to use. This is a curatorial suggestion, not a content decision.

## Full Extraction Summary
| Source | Directory | Images Extracted |
|--------|-----------|-----------------|
| 2026 JH all inverted v2 (87 slides) | `2026-talk/` | 48 |
| Cool science pictures (6 slides) | `science-pics/` | 8 |
| Copies of all figures (19 slides) | `paradigm-figures/` | 24 |
| Lab vision talk (27 slides) | `lab-vision-talk/` | 24 |
| CYP2R1 KO mice data (18 slides) | `cyp2r1-ko/` | 32 |
| T1DM/CAR-Treg Lilly (8 slides) | `t1dm-car-treg/` | 13 |
| LacZ staining (6 slides) | `lacz-staining/` | 12 |
| **Total** | | **161** |

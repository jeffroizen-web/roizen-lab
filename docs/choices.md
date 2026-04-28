# Ace Scout (Roizen Lab) — Architectural Decision Log

## [2026-03-06] Theme: Purple & Gold
**Choice**: Purple-gold (`--primary: #3B1F6E`, `--accent: #C5A336`)
**Alternatives**: Warm Slate theme
**Rationale**: Jeff chose purple-gold as more distinctive and aligned with academic gravitas. Gold accent provides warmth against the deep purple.
**Status**: Active

## [2026-03-06] Layout: Ethan Goldberg-style Dual Header
**Choice**: Dark purple institution bar above, white nav bar below, with 1px gold border separating them
**Alternatives**: Single nav bar, sidebar layout, standard academic template
**Rationale**: Studied reference sites (Goldberg NeuroLab, Kolber Pain Lab). Dual header provides institutional credibility (CHOP/Penn logos) without cluttering the navigation. Matches best-in-class academic lab sites.
**Status**: Active

## [2026-02-27] Logo: jeff-logo-2 ("Hypothesis Driven")
**Choice**: jeff-logo-2 depicting a 70s muscle car with DNA double helix as dust cloud. Wordmark "Hypothesis Driven" with ".org"
**Alternatives**: jeff-logo-1, jeff-logo-3, other iterations
**Rationale**: Best aspect ratio (6.02:1), widest at 355px @ 60px nav height. The "Driven" in the name is literal (car). Recolored to theme purple (#3B1F6E), stroke removed for sharpness.
**Status**: Active

## [2026-03-06] Hero Heading: "Redefining Vitamin D"
**Choice**: "Redefining Vitamin D"
**Alternatives**: "Rethinking Vitamin D"
**Rationale**: "Redefining" is more active and forward-looking than "Rethinking." Signals the lab is doing more than questioning — it's building new understanding.
**Status**: Active

## [2026-03-06] Big Questions Grid: 3-Across
**Choice**: 3-across grid for Big Questions section
**Alternatives**: 2-across grid
**Rationale**: 7 questions fit better in a 3-across layout (3+3+1) than 2-across (4 rows). More compact, professional appearance.
**Status**: Active

## [2026-03-12] Join Us Card: Custom Funding Honesty Text
**Choice**: Custom version combining funding honesty + Option A language: "We currently do not have hard funding... but are always looking to identify curious, enthusiastic, hard-working people who want to do careful, ambitious science"
**Alternatives**: Option A (aspirational only), Option B (funding-focused), generic academic boilerplate
**Rationale**: Jeff wanted honesty about the funding situation while still conveying that the lab welcomes talent. The "boundaries of knowledge, even if only by a few millimeters" language echoes the lab manual's craftsperson ethos.
**Status**: Active

## [2026-02-28] No Build System: Plain HTML/CSS/JS
**Choice**: No build system — plain HTML/CSS/JS, direct editing
**Alternatives**: Next.js, Hugo, Jekyll, other static site generators
**Rationale**: Academic lab website is mostly static content. No interactivity requires a framework. Plain files are directly editable, need no toolchain, and deploy trivially. Avoids complexity for a project that's primarily design and content.
**Status**: Active

## [Various] Timed Out Decisions (Holding)
**Big Questions Text** (timed out Mar 7): Holding with current 7 questions. Jeff flagged figure-to-question matching may be wrong.
**Microscopy Composites** (timed out Mar 7): Holding with all 3 composites, purple-gold tint.
**Contact Email** (timed out Mar 10): Holding with lab email default.
**Status**: Holding — awaiting Jeff confirmation or override

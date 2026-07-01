# Web-Quality Self-Assessment — Roizen Lab site (2026-07-01)

**CM:** Ace Scout · **Surface:** `compare-purple-gold.html` (the canonical lab site, a **front-door** surface → full showcase treatment per the standard) · **Standard:** `.claude/rules/web-quality-standards.md` (9 rules) · **Method:** audited the rendered markup + CSS path directly (not a screenshot); every verdict cites evidence. **CWV not empirically measured — Lighthouse is not installed in this environment; those items are flagged as unmeasured, not claimed.**

## Scorecard

| # | Rule | Verdict | Evidence / gap |
|---|------|---------|----------------|
| 1 | Design-token discipline | **PARTIAL** | Colors ARE tokenized (`:root` vars, dual-theme parity). But **47 inline `style=` attributes carry hardcoded `px`/`rem` dimensional values** (font-size, margin, padding) — spacing/type are not on a token scale. The people/collaborator/peer/mentor cards are the worst offenders. |
| 2 | Type & hierarchy | **PARTIAL** | One `<h1>` ✓, heading nesting no-skips ✓ (site-qa guard), body measure capped (hero 680px) ✓. **But 24 distinct font-size values — twelve of them clustered between 0.68rem and 0.95rem — i.e. NO modular scale.** This is the rule's named "#1 amateur tell." Hierarchy is sound; the *scale* is ad-hoc. |
| 3 | Layout, spacing, alignment | **PARTIAL** | Real grid + intentional whitespace ✓. But spacing values are ad-hoc inline `px` (40/28/24/12/8/64…), not a disciplined 4/8 token scale. Same root cause as #1. |
| 4 | Motion that earns its place | **PASS** (+ big **OPPORTUNITY**) | `prefers-reduced-motion: reduce` honored globally (kills durations) ✓; transitions animate `transform`/`opacity`/`color`, tasteful 0.2s ✓. **BUT for a front-door showcase surface there is essentially no motion** — no scroll-reveal, no hero motion, no bespoke visual. Rule passes; the *showcase bar* is unmet. See Opportunities. |
| 5 | Performance budget | **PARTIAL / at-risk** | Fonts self-hosted + preloaded (57dbac0) ✓, imgs explicit width/height ✓ + `loading="lazy"` ✓, CLS-guarded ✓. **BUT all 13 raster images are `.jpg`/`.png` — zero modern formats (WebP/AVIF), and the hero is a 301K JPG CSS background on the LCP-critical path** (plus 312K/312K/240K content JPGs). LCP/CLS/INP **unmeasured** (no Lighthouse here). |
| 6 | Responsive + adaptive | **PASS-WITH-FLAG** | No horizontal overflow at 360/480/768 ✓ (site-qa), content reflows ✓. Flags: media queries are **desktop-first `max-width`** (not the mandated mobile-first `min-width`); nav-link tap target height should be verified ≥44px (buttons are fine at ~48px). |
| 7 | Accessibility — WCAG-AA | **PASS** | Contrast AA across the surface (fixed 6ef972c: CTA buttons + nav-hover), semantic landmarks, skip-link, nav `aria-expanded` toggle, all form inputs `<label for>`, form-status live region, 15/15 non-empty alt, reduced-motion. Minor: `:focus-visible` outlines exist on some interactive els (paper-link, contact links) but are **not universal** (nav links / buttons / form inputs rely on default focus) — tighten for full-surface coverage. |
| 8 | Craft & polish details | **PASS-WITH-FLAG** | Hover/active states, `:focus-visible` on key els, designed form status/error state, favicon + full meta + OG/Twitter + JSON-LD ✓, no FOUC (`font-display:swap` + preload) ✓, real content (no lorem) ✓, consistent radius/shadow. Flags: focus-visible not universal (see #7); Q2/Q3/Q7 figures are "Figure pending" placeholders (honest, but a visible incompleteness on a front-door surface). |
| 9 | Content & copy | **PASS** | Jeff's voice throughout, de-marketed (e086df8), no lorem, intentional microcopy. Meets `orchestra.md` Voice & Style. |

**Tally:** 3 PASS (incl. 2 with-flag) · 1 PASS+opportunity · 4 PARTIAL · 0 FAIL/BLOCK. No BLOCK-level defect (a11y/responsive/type-hierarchy are all sound). The gaps are **craft-systematization + front-door showcase**, not brokenness.

## Ranked gap list (worst first)

1. **[R2 + R1 + R3] No design-token system for type & spacing (the "unfinished drift" cluster).** 24 ad-hoc font sizes + 47 inline hardcoded `px`/`rem` styles. This is the single highest-leverage craft fix: introduce a modular type scale + spacing scale as tokens, replace the inline one-offs. Biggest "reads as a draft" risk. *(Highest leverage; one gated build.)*
2. **[R5] No modern image formats; heavy hero on the critical path.** Convert the 13 jpg/png to WebP/AVIF with `<picture>` fallback; compress/right-size the 301K hero background. Real LCP win, directly ties to the perf budget. *(Blocked sub-item: I cannot measure CWV here — recommend a Lighthouse pass at deploy.)*
3. **[R4] SHOWCASE MOTION — the front-door opportunity (see below).** The rule passes, but this surface is explicitly "the clearest candidate for WebGL/animation/showcase" and currently has none. Highest *upside*, not a deficit.
4. **[R6] Mobile-first authoring + nav touch targets.** Re-author the media-query strategy min-width-first; verify/raise nav-link tap targets to ≥44px.
5. **[R7/R8] Universal `:focus-visible`.** Extend the focus-outline token to every interactive element (nav, buttons, inputs), not just links.
6. **[R8] Resolve the 3 "Figure pending" placeholders** (Q2/Q3/Q7) — Jeff-gated (needs the correct science figures; anti-fabrication).

## Showcase opportunities (front-door treatment — flagged per Kleiber)

This site is *about molecular science* — bespoke, on-theme motion/imagery would land hard and is fully justified for a front-door surface (all must honor `prefers-reduced-motion`):

- **Hero:** replace the static 301K JPG with a subtle **WebGL/canvas molecular motif** — an animated vitamin-D / VDR-receptor / calcium-pathway visual, or a slow parallax/particle field over the microscopy composite. The single biggest "Awwwards-caliber" upgrade and directly on-brand.
- **Big Questions (7):** **scroll-driven reveal** — each question + figure animates in (fade/translate `opacity`+`transform`, 60fps) as it enters the viewport. Turns a static list into a narrative scroll.
- **Research figures as compelling data viz:** the MR reverse-causation scatter, the dose-response OxPhos curves, the T2D Kaplan-Meier — animate/interactive per `data-viz-standards.md` (honest AND compelling). This is the "rich data deserves a stage" mandate.
- **AI-generated bespoke imagery** (the @linas toolchain) for section headers / the 3 pending figures' *conceptual* placeholders (clearly labeled as illustrative, never as data — anti-fabrication).

## Recommended uplift sequence (gated, one-concern-per-PR)

1. **`design-token-scale`** — modular type scale + 4/8 spacing scale as tokens; replace inline one-offs (fixes R1/R2/R3 together). *Autonomous.*
2. **`image-modernization`** — WebP/AVIF + `<picture>`, hero right-sizing (R5). *Autonomous; recommend a Lighthouse pass at deploy to confirm CWV.*
3. **`focus-visible-universal` + `mobile-first-mediaqueries`** — small craft fixes (R6/R7/R8). *Autonomous.*
4. **`hero-showcase-motion`** (WebGL molecular hero) + **`scroll-reveal`** — the showcase builds (R4 opportunity). *Higher-effort; recommend a design direction check with Jeff/Design-UX CM before building — bespoke visual identity is a taste call.*

**Note on hosting:** all of the above are quality uplifts to the working file; the site's one go-live gate remains HOSTING (unchanged). These can land pre- or post-launch.

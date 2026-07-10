# HALLMARK Audit — Roizen Lab website (hypothesisdriven.org)

**Verb:** `hallmark audit` (read-only — no edits, no commits)
**Auditor:** read-only design auditor (HALLMARK audit mode)
**data_as_of:** 2026-07-09
**Method:**
- SOURCE read: `compare-purple-gold.html` (canonical single source of truth, all CSS inline in one `<style>` + linked `design-tokens.css`) — 1591 lines read in full (ignoring the always-uncommitted cron field-of-interest diff and the appended Lighthouse INSTRUMENT-RESULTS blocks, which are not part of the shipped `</html>`).
- RENDERED read: `https://jeffroizen-web.github.io/roizen-lab/` via Playwright at 320 / 375 / 414 / 768 / 1280 px (horizontal-scroll probe, tap-target/clickable-wrap probe, computed styles, console errors).
- Scored against: HALLMARK anti-patterns + 58-gate slop test + the 6 cross-verb disciplines. Reconciled against house `web-quality-standards.md` (9 rules) — Hallmark sits UNDER the house rules; Rams's `design-tokens.css` + the 9 rules WIN on any conflict.

**Scope note (what this audit is NOT):** the site is already web-quality-gated (WCAG-AA contrast, design tokens, self-hosted fonts, WebP images, `:focus-visible` ×12, 44px mobile tap targets, LCP ~95ms/CLS 0). Those PASS and are NOT re-reported as gaps. This audit reports only what HALLMARK adds BEYOND the 9-rule bar: structural variety, anti-AI-slop tells, macrostructure/section rhythm, hero/section archetype variety, type-pairing character, copy voice, motion character, imagery.

---

## Method status
- [x] Source read in full
- [x] design-tokens.css read
- [x] House rules (web-quality-standards.md) reconciled
- [x] Rendered probe (Playwright) — 320/375/414/768/1280, no h-scroll any width, 0 console errors
- [x] Ranked punch list
- [x] Conflicts-with-house-rules section
- [x] Summary verdict

## Rendered-probe facts (Playwright, live site)
- **No horizontal scroll** at 320/375/414/768/1280 (gate 34 PASS; `scrollWidth === innerWidth` every width).
- **0 console errors / 0 page errors.**
- **No true two-line clickable-affordance (gate 49) violations.** The buttons flagged by the raw detector (Explore Our Questions / Donate Through CHOP / Send) are padded single-lines, not wraps. Long publication-title links and person-name links do wrap, but those are body/reading links, not button/nav/CTA affordances — acceptable under gate 49.
- **Fonts actually rendered:** Merriweather (serif, headings ×30) + Open Sans (body ×296) + Arial ×2 (stray). Two-family pairing — passes gate 1 (display is not Inter/Open Sans).
- **Hero:** `min-height:720px` (90vh), text-align center, `h1` roman, `h1 em` **italic (rgb 197,163,54 gold)**, CTA bottom 602 < 800 viewport (fits the fold — gate 44(b) PASS), padTop 168 / padBottom 80 (top-heavy — gate 44(a) soft-fail).

---

## RANKED PUNCH LIST
Ranked by user-felt visual/UX leverage. Severity = Hallmark's `critical / major / minor`. Each finding notes house-rule reconciliation.

### 1. [MAJOR] Italic emphasis-word in the hero headline — `hero h1 em` (gate 38a, discipline 6, anti-pattern "Italic headers")
- **Issue:** `compare-purple-gold.html:257` — `.hero h1 em { font-style: italic; color: var(--accent); }` on `<h1>Redefining <em>Vitamin D</em></h1>` (line 828). Rendered confirmed italic. This is the single most reliable AI-generated tell in Hallmark's list: a roman headline with one word flipped to italic (`Built to <em>think</em>`). Gate 38a is an **auto-fail on every theme.** Worse: no italic Merriweather face is loaded (only `font-style:normal` @font-face at line 90), so the browser renders **faux/synthetic slanted** Merriweather — the least crafted form of italic.
- **Where:** CSS `:257`, markup `:828`.
- **Fix direction:** Drop `font-style: italic`; keep the gold `color: var(--accent)` — the accent color alone already lands the emphasis (Hallmark: "carry emphasis with weight, accent colour, or a drawn underline"). Optionally bump `<em>` weight to 700. One-line change, no token change.
- **Reconciliation:** **COMPLEMENTS** web-quality-standards (no rule requires italic; keeps the token). It is a design-craft call → route through **Rams's intra-arc design blessing** (R3 charter) before edit; does not fork tokens.

### 2. [MAJOR] Eyebrow on every section — 11 uppercase mono-cap eyebrows + 10 gold-line dividers (anti-pattern "Eyebrow on every section")
- **Issue:** Every `.section-header` opens with `<p class="eyebrow">` (Research / People / Network / Community / Lineage / Publications / News / Alumni / Support / Contact) above a `.gold-line` divider above the `<h2>`. 11 eyebrows, 10 gold-lines (grep-confirmed). Hallmark: eyebrows are **default-OFF**, ordinal-only, capped at 1–2 per page — "when every section is chaptered, none of them are." The identical eyebrow→gold-line→H2→lede stack on every section is the "list of labelled lists" templated rhythm — the dominant macrostructure-monotony tell on the page.
- **Where:** eyebrow CSS `:279`; instances at `:839, 947, 978, 1013, 1057, 1090, 1198, 1231, 1311, 1324` (+1). Gate 54 (tag-left/header-right two-column) does NOT fire — the stack is vertical/single-column, which is correct. This is the *count/rhythm* tell, not the layout tell.
- **Fix direction:** Cut eyebrows to 0–2 (keep at most on the hero-adjacent "Research/Big Questions" section if any). Let the `<h2>` + lede carry each section. Optionally keep the gold-line as the sole section-marker, or vary it. Reduces the templated cadence the most.
- **Reconciliation:** **COMPLEMENTS** the 9 rules (no rule mandates eyebrows). It is a brand/section-rhythm design decision → **Rams design-gate call** (the eyebrow + gold-line are part of the decided purple-gold identity). Recommend, do not self-apply.

### 3. [MAJOR] Centered-everything — every section header + the hero on one centered axis (gate 6, anti-pattern "Centred everything")
- **Issue:** `.section-header { text-align:center }` (`:275`) with centered gold-line + centered `<h2>` + `margin:0 auto` lede on every section; `.hero-inner { text-align:center }` (`:245`) stacks badge + `<h1>` + subtitle + affiliations + CTA all on the same centered vertical axis. Gate 6 auto-fails a hero where eyebrow/badge, title, lede AND CTA are all centered on one axis (editorial genre allows a centered-narrow hero, but even then the badge or CTA should sit off-axis — here nothing does). Combined with the section-header treatment, the whole page is "section after section of centered columns" (the named "Centred everything" major tell).
- **Where:** `.hero-inner:245`, `.section-header:275`.
- **Fix direction:** Break symmetry once — bias the section headers (or a subset) left with a wide right margin; move the hero badge or the CTA off the centered axis (left-flush or margin-anchored). Does not require touching the grids beneath.
- **Reconciliation:** **COMPLEMENTS** the 9 rules (alignment is not a token). Structural/taste call → **Rams design-gate**. Not a token fork.

### 4. [MINOR] Donate block — purple→purple gradient + centered white text + gold radial-bloom decoration (gate 45 "decorative-without-purpose"; adjacency to "purple-gradient hero")
- **Issue:** `.donate-section` uses `--donate-bg: linear-gradient(135deg, #3B1F6E, #5A3D8A)` (`:146`) behind centered white text, plus `::before` `radial-gradient(circle, rgba(200,150,62,0.12), transparent 70%)` (`:476`) — a floating gold bloom with no semantic anchor (gate 45). The gradient is brand-purple→purple (not the purple→pink AI gradient) and the bloom is faint single-hue, so it's on the *acceptable edge*, but it's the section that most resembles the "purple-gradient hero" AI aesthetic.
- **Where:** `:146, :472–479`.
- **Fix direction:** Consider a solid `--primary` fill for the donate block and drop the radial bloom (Hallmark: "the hero doesn't need depth; it needs a strong anchor"). Low priority.
- **Reconciliation:** **PARTIAL CONFLICT** — the purple gradient IS the decided purple-gold identity (`--donate-bg` is a theme token). Flattening to solid touches Rams's token/theme surface → **Rams-only**. Removing the decorative bloom is safe/complements.

### 5. [MINOR] Side-stripe on the contact form — 4px gold left border (anti-pattern "The side-stripe card")
- **Issue:** `.contact-form { border-left: 4px solid var(--accent) }` (`:504`) — a thick 4px asymmetric colored edge, the "2018-SaaS-AI side-stripe card" tell. (The `--card-border: 4px solid #C5A336` token at `:144` is the same motif, though `.card` itself now uses a 1px hairline.)
- **Where:** `:504` (+ token `:144`).
- **Fix direction:** Hairline all-around border, or no border, or a small accent square beside the "Get in Touch" heading — not an asymmetric thick stripe.
- **Reconciliation:** **COMPLEMENTS** the 9 rules; brand-accent usage → **Rams design-gate** (the gold accent is Rams-canonical, but the *4px-left-edge treatment* is a craft choice, not a token value).

### 6. [MINOR] Hero photo overlay — purple gradient over centered white text (borderline "purple-gradient hero")
- **Issue:** `.hero::before` `linear-gradient(135deg, rgba(59,31,110,0.82), rgba(90,61,138,0.65))` (`:131–132, :240`) over the microscopy photo, centered white `<h1>`. This is a *duotone photo overlay on a real image* (defensible), not a synthetic gradient-only background — so it escapes the *critical* form of the tell. Noted for awareness; the real image + brand-purple carry it.
- **Fix direction:** No action needed if the photo is kept; if ever the photo is removed, do not ship the gradient alone.
- **Reconciliation:** **CONFLICT-adjacent** — the overlay is the decided theme (`--hero-overlay-*` tokens). Rams-only.

### 7. [MINOR] Universal hover-lift — `translateY(-2/-3px)` on multiple unrelated card types (gate 11 / anti-pattern "Universal hover:scale-105")
- **Issue:** `.news-card`, `.alumni-card`, `.merch-card`, `.btn`, `.question`… all lift on hover (`:270, 447, 455, 463`). Multiple unrelated elements share one hover signal. It's `translateY` (not `scale`) + a paired shadow (a purposeful elevation cue), so it's a *mild* instance, not the egregious scale-105 form.
- **Fix direction:** Fine to keep; if tightening, pick one signal per element type. Low.
- **Reconciliation:** **COMPLEMENTS** (motion honors reduced-motion already). Design-gate optional.

### 8. [MINOR] Generic body face — Open Sans (anti-pattern "Inter-everywhere" family, body-side)
- **Issue:** Body is Open Sans (`:137`), on Hallmark's generic-tell list (Inter/Roboto/Open Sans). It IS paired with Merriweather (so NOT the single-font tell — gate 1 passes), but Merriweather+Open Sans is a very safe/common "academic default" pairing with little character.
- **Fix direction:** A more distinctive body face (e.g. a humanist sans with more voice) would lift the type character — but see conflict below.
- **Reconciliation:** **CONFLICT** — fonts live in the `[data-theme]` blocks / are Rams's theme-token territory (`--body-font`/`--heading-font`). **Do NOT act on** without Rams; changing the pairing forks the decided theme. Listed for Rams's awareness only.

### 9. [MINOR] Straight apostrophes in hand-written copy (anti-pattern "Straight quotes")
- **Issue:** `That's it.` (donate `:1314`), `We are changing that.`/`don't` — a few straight `'` where a curly `’` belongs. (Most punctuation is correctly `&mdash;`/`&middot;`/`&rarr;`.) PubMed-sourced titles ("don't accept wimpy") are external data — leave.
- **Fix direction:** Curly the apostrophes in author-written copy only.
- **Reconciliation:** **COMPLEMENTS** (copy polish, no token/palette impact).

### 10. [MINOR] Hero-subtitle hardcoded `<br>` line breaks + hero top-heavy padding (gate 44(a))
- **Issue:** `hero-subtitle` uses three `<br>` for line control (`:829`) — brittle vs reflow (mitigated by `.hero-subtitle br{display:none}` on mobile, `:600`). Separately, hero padTop 168 / padBottom 80 is top-heavy (gate 44(a) wants bottom ≥ 1.3× top so the hero pulls into the next section) — though the 168 top is largely fixed-nav clearance.
- **Fix direction:** Let the subtitle wrap naturally (drop the `<br>`s, cap `max-width`); optionally rebalance hero padding. Low.
- **Reconciliation:** **COMPLEMENTS** (spacing tokens already exist; no fork).

### 11. [INFO] No Hallmark macrostructure stamp
- The canonical file has no `/* Hallmark · macrostructure: … */` stamp (it predates Hallmark). Not a defect — informational. If Hallmark ever *builds* here, it would stamp + rotate. As a single hand-built page (not two Hallmark outputs), the diversification/variety-drift rule does not apply.

---

## CONFLICTS WITH HOUSE RULES — flagged for Rams, NOT to be built without design sign-off
The house `web-quality-standards.md` (9 rules) + Rams's `design-tokens.css` and the decided **purple-gold theme** (CLAUDE.md "Theme Selection — DECIDED": `--primary #3B1F6E` / `--accent #C5A336`) WIN on every conflict. The following Hallmark instincts would **fork Rams's canonical tokens/palette/fonts** and must NOT be acted on autonomously:

1. **Font-pairing change (finding #8).** Swapping Open Sans / Merriweather touches `--body-font`/`--heading-font` in the `[data-theme]` blocks — a decided theme choice. CONFLICT. Rams-only.
2. **Palette / accent-hue change.** Any Hallmark anti-pattern that implies "pick a different anchor hue," "don't use a purple gradient," or "re-tint neutrals" (findings #4, #6) conflicts with the DECIDED purple-gold theme and the WCAG-tuned `--accent-dark`/`--btn-text` values. Flattening `--donate-bg` / `--hero-overlay-*` to solids edits theme tokens. CONFLICT. Rams-only.
3. **Removing brand chrome that carries the identity** (the gold-line dividers, the gold left-stripe, the gold radial bloom — findings #2, #4, #5) touches the decided purple-gold visual identity. The *count/rhythm* reduction (fewer eyebrows) complements; the *element removal* is a Rams brand call.
4. **Raw `rgba(197,163,54,…)` gold tints** in `.pub-badge`/`.freshness-banner`/`.field-of-interest` (mid-render token improvisation, gate 48) OVERLAP web-quality-standards **rule 1 (token discipline)**, which already governs this surface and is already gated. **Not reported as a Hallmark-unique gap** — deferred to the existing house token process, not a fork.

**Every structural finding above (#1–#3 especially) COMPLEMENTS the 9 rules** — none require a token/palette/font change; they are alignment, count, and emphasis-style craft calls. Per the R3 team charter they route through **Rams's intra-arc design blessing + Kleiber's merge gate**, not an autonomous edit.

---

## SUMMARY VERDICT
**Reads as "polished but templated."** The site is genuinely strong on the 9-rule web-quality bar (contrast, tokens, self-hosted fonts, WebP, focus-visible, 44px targets, LCP ~95ms/CLS 0, no h-scroll, honest Jeff-voice copy, real data, no invented metrics, no lorem, minimal tasteful motion, a nice alternating question-row layout). What Hallmark adds beyond that bar: the page carries the **section-rhythm monotony** signature — one macrostructure (centered eyebrow → gold-line → H2 → lede, ×11) repeated top to bottom — plus **one top-tier AI tell (the italic hero emphasis-word).**

**Counts:** 0 critical · 3 major · 7 minor · 1 info. No gate-34/gate-49/gate-6-hero-fold/contrast failures on the rendered surface. Two house-rule CONFLICT clusters found (fonts, palette/theme tokens) — both flagged Rams-only.

**Single highest-leverage next uplift:** **Fix #1 — drop `font-style: italic` on `.hero h1 em` (keep the gold accent).** One line, removes Hallmark's most reliable AI tell from the most-seen element, resolves a synthetic-faux-italic rendering, complements the house rules, forks no token. Route the one-liner through Rams's design blessing per the R3 charter. The next tier (findings #2–#3: thin the eyebrows to 0–2 and break the centered-header symmetry) is where the "different site vs one template" character gain lives, but those are Rams design-gate decisions, not autonomous edits.

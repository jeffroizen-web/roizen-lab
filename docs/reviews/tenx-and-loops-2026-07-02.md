# Fable-Window Self-Review — 10X · Optimization · Loop-Engineering · UX Walkthrough

> **Ace Scout (Roizen Lab), 2026-07-02.** REPORT-ONLY per Kleiber MSG-41a807 (Jeff-ordered
> Fable-window directive, window closes Jul 7). No pushes, no builds — findings only; any
> build routes through the normal gate afterward. Written incrementally: header+scope first,
> each finding appended as confirmed (agent-team-standards cap-4).

## Scope & method

- **Product**: the Roizen Lab credibility site — `compare-purple-gold.html` (working/canonical, ~1325 lines, all-inline CSS/JS, no build system), served at hypothesisdriven.org (registered, not yet hosted). Vision: *"not a departmental template page — a carefully crafted statement of scientific identity"* conveying *engagement, trust, and a cool factor* (`docs/score_reference.md`).
- **Loops I own** (2, both launchd-loaded, last exit 0): `com.hypothesisdriven.letter_writers_refresh` (daily scrape → wire peer "recent focus" into HTML) and `com.hypothesisdriven.tenure_readiness` (daily grade of launch-readiness). Supporting scripts: `letter_writer_scrape.py` (399), `letter_writers_refresh.py` (117), `wire_letter_writers.py` (210), `tenure_readiness.py` (223), `tenure_readiness_cron.sh` (88), `publications_feed.py` (189).
- **Last 2 weeks of my code** (git since 2026-06-18): PR-1 design-tokens (d607729), PR-2 WebP (8678346), WCAG (6ef972c, earlier), font-perf (57dbac0, earlier), flag fixes (8f85b87, 2a6a22d), + test suites (`test_{design_tokens,images,fonts,contrast,content_contract}.py`).
- **Method**: read the actual code + rendered surface; cite file:line; Playwright MCP for the UX walk. Startup-studio bar throughout: *would this ship to a paying user?*

---

## 1. 10X Review — step-changes a user would feel

Frame: the "paying user" of a lab-credibility site is Jeff's tenure-case audience (committee, collaborators, journalists, reviewers) + prospective trainees + donors. A 10x = a step-change in *credibility, engagement, or reusability* — not polish. Ranked by user-felt leverage. Startup-studio bar noted per item.

**10X-1 — GO LIVE (the site exists nowhere today).** The single largest user-felt step-change dominates all others: `compare-purple-gold.html` is polished but reachable by zero people — hypothesisdriven.org is registered (Google Cloud DNS) and points nowhere. Every craft gain is worth 0× until this ships.
- *Acceptance*: hypothesisdriven.org resolves over HTTPS to the canonical site; 0 broken assets; 0 console errors; deploy-time Lighthouse perf ≥ 90.
- *Ship?* It IS the product's existence. **Jeff-gated** (DNS paste / "soft-launch go" — Tier-2). Roadmap: `docs/DEPLOY.md` Path A, one step on his go.

**10X-2 — Render-from-config: turn the 1325-line monolith into a reusable lab-site generator.** Today the site is one hand-maintained HTML file; `content/site-content.json` already extracts the content (templatize-content, a3a91cc) but the HTML is still render-authoritative. Flip authority to config→template and this stops being "Jeff's site" and becomes a **shippable product**: any PI drops in their `content.json` and gets this site. Startup-studio "does it have a market?" — thousands of academic labs need exactly this and have departmental-template pages instead.
- *Acceptance*: `build.py content/site-content.json` reproduces the current site (golden byte-diff test); a second fixture lab's config yields a valid distinct site with **zero** HTML hand-edits; SEO/meta preserved; site-qa + content-contract green on the generated output.
- *Ship?* Yes — this is the clearest path from "personal-only" to "product." **Jeff-gated** (crosses the documented no-build-system constraint + SEO risk on the flip); flagged in `docs/specs/content-contract.md` as the next increment. Highest reusability 10x.

**10X-3 — Living publications + citation counts (credibility's core signal).** A committee's first question is productivity; the Publications section is static and gated on the Archivist counter-sig. Make it an always-fresh, auto-ingested list with live citation counts and a "N papers · cited M times" header. A committee sees a living CV, not a 2026 snapshot. Infra exists (`publications_feed.py` consumer + `com.archivist.publications-weekly` plist) — the gap is the live feed + citation enrichment.
- *Acceptance*: Publications renders from a feed ≤7 days old with a visible `data_as_of` stamp (Data Provenance); per-paper citation count present; **degrades loudly** if the feed is stale (loud-degradation-contract, not a silent 2026 snapshot); full-text links resolve.
- *Ship?* Yes. **Semi-autonomous** — needs Archivist counter-sig on `docs/contracts/archivist-publications.md` (cross-CM, Producer-Owns).

**10X-4 — WebGL molecular hero + scroll-reveal Big Questions (the "cool factor" the vision names).** The vision demands *engagement, trust, and a cool factor… not a departmental template page.* Currently: a static hero image + a static list of 7 questions. An on-brand animated vitamin-D / VDR / calcium-pathway hero (WebGL/canvas) + scroll-driven reveal of the 7 Big Questions is the front-door showcase that makes "a statement of scientific identity" literal.
- *Acceptance*: 60fps (animate `transform`/`opacity` only), `prefers-reduced-motion` → static fallback, LCP stays < 2.5s, JS budget < 150KB gz, no CLS.
- *Ship?* Yes for a front-door surface. **HELD for Jeff/Rams design direction** (PR-3 — bespoke visual identity is a taste call). Highest *engagement* upside.

**10X-5 — Interactive research figures (rich data deserves a stage).** The evidence figures are static images and three are still "Figure pending" placeholders. Per the web-quality + data-viz mandate ("we have rich data… display it compellingly"), turn the MR reverse-causation scatter, the dose-response OxPhos curves, and the T2D Kaplan-Meier into interactive, honest, provenance-stamped viz (hover values, CIs shown, `data_as_of`). Turns "here are figures" into "explore our evidence."
- *Acceptance*: each figure backed by REAL data (anti-fabrication — Jeff/Archivist-sourced, never synthetic); uncertainty/CI shown (data-viz rule 2); `data_as_of` stamp (rule 3); keyboard-accessible; honest axes (rule 1).
- *Ship?* Yes, but **Jeff-gated** (needs the real underlying data + the anti-fabrication line the launch-content pass already held).

**10X-6 — Self-measuring quality gate at deploy (CWV read-back, not assertion).** Product-quality-not-good-enough: today CWV is *asserted* (no Lighthouse in sandbox — flagged in DEPLOY.md). Wire a Lighthouse run into the deploy that records LCP/CLS/INP, fails below budget, and publishes the number — the site continuously proves its own quality instead of claiming it. Composes with the existing `tenure_readiness` watcher.
- *Acceptance*: deploy runs Lighthouse headless, writes LCP/CLS/INP to a tracked report, the gate blocks a deploy under budget (LCP<2.5s/CLS<0.1/INP<200ms), and the −74% hero claim is read back against the served asset.
- *Ship?* Yes. **Autonomous once hosted** (queued in DEPLOY.md §Post-deploy; the gate wiring is the build).

**10X-7 — Prospective-trainee conversion loop (funnel, not a form).** "Join Us" is an honest static card + a Formspree/ntfy contact form (Layer 1). For a lab actively seeking "curious, ambitious" trainees, the step-change is a real funnel: structured interest intake (background, why-this-lab), verified routing to Jeff with triage, and an applicant confirmation — a CRM-lite, not a mailto.
- *Acceptance*: structured fields captured; delivered to Jeff on a **read-back-verified** rail (Producer-Read-Back); applicant gets an auto-confirmation; spam-guarded; Layer-2 Telegram-to-Kleiber wired.
- *Ship?* Yes — turns passive credibility into active recruiting. **Partially built** (Layer 1 done); the triage+confirmation is the increment (needs Pilot Railway endpoint + Jeff deploy approval).

**Top-3 by leverage: 10X-1 (go live — dominates), 10X-2 (render-from-config → a product with a market), 10X-4 (WebGL showcase → the "cool factor" the vision names).**

## 2. Optimization Pass — worst-first (my last ~2 weeks of code)

**O-1 (worst) — Unbounded daily-report accumulation in git.** Commit 86b53d6 tracked 13 `docs/reports/tenure-readiness-YYYY-MM-DD.{json,md}` pairs, and `tenure_readiness_cron.sh` adds a new pair **every day, forever**, all committed. At 2 files/day this is ~730 files/year of near-identical drift bloating the repo and every clone/diff. *Fix*: rotate (keep last N, e.g. 14) or `.gitignore` the dated reports and keep only a rolling `tenure-readiness-latest.{json,md}` + the baseline. Class: dead-scaffolding accumulation. *(Highest leverage; small change.)*

**O-2 — Exit-code-outcome-mismatch in both loops.** `letter_writers_refresh.py:113` returns **exit 1 when it successfully detects a confidence regression**; `tenure_readiness.py:219` returns **exit 1 on any regression-since-baseline**. A launchd job's exit code drives health monitoring — so "I did my job and found drift" is logged identically to "the job crashed." A stale baseline then makes every run look like a failing job (alert fatigue). *Fix*: reserve nonzero for genuine execution failure (scrape/IO/parse); surface "regression detected" via the emitted event / a distinct sentinel field, not the process exit code. Cross-ref `failure-ledger-contract.md` → `exit-code-outcome-mismatch`. *(Real correctness/observability bug, not style.)*

**O-3 — Per-test HTML re-read duplication (5 test files).** `test_design_tokens.py`, `test_images.py`, `test_contrast.py`, `test_fonts.py`, `test_content_contract.py` each independently do `HTML = (ROOT/"compare-purple-gold.html").read_text()` at module load. *Fix*: a shared `tests/conftest.py` fixture (`html`, `tokens`) — one read, one source of truth, and it kills the copy-paste-3+-times smell. *(Cheap; parsimony.)*

**O-4 — Split-brain CSS: tokens external, consumers inline.** `design-tokens.css` is `<link>`ed but the entire consuming stylesheet lives inline in the HTML `<style>`. For a no-build static site this is defensible (one extra request vs one inline block), but it means the "single source of truth" is split across two files and a reader can't see a token and its use together. *Fix (defer)*: fold tokens into the inline `<style>` `:root` (matches the all-CSS-in-one-block architecture the font-perf PR already committed to) OR document the split as intentional. *(Low; note-not-fix.)*

**O-5 — Manual clean-attribution dance repeated 4×.** The HEAD-reconstruct + deterministic-re-transform + restore-cron-foi recipe (memory `reference_html_edit_cron_foi_clean_attribution`) has now been hand-run 4 times (wcag/fonts/PR-1/PR-2). Repetition-Awareness threshold (3) is passed. *Fix*: a `scripts/commit_my_html_edits.sh <transform.py>` that runs the recipe mechanically (backup → checkout → apply transform → assert `grep -cE 'Recent focus</span>' == 0 diff → commit → restore backup). Removes the highest-risk manual step in my workflow. *(Tooling proposal — the retro repetition_counter already logged this.)*

**Not-a-problem (verified clean):** `wire_letter_writers.strip_existing_foi` whitespace-consumption (the 6-18 byte-stability fix is correct and tested); the `subn(count=0)` "all occurrences" is intentional; escape helpers are minimal but correct.

## 3. Loop-Engineering Self-Audit (@linas checklist)

Two long-running loops, both launchd-loaded (last exit 0). Scored on: (a) role separation planner/generator/evaluator, (b) state-on-disk + restart-safe, (c) execution traceable, (d) current bottleneck.

### Loop A — Letter-writer refresh (`letter_writers_refresh` → `letter_writer_scrape` → `wire_letter_writers` → bus emit), daily 03:00

| Axis | Score | Evidence |
|---|---|---|
| (a) Role separation | **GOOD** | GENERATOR = `letter_writer_scrape.py` with explicit L1 PubMed / L2 ORCID / L3 WebFetch redundancy layers (docstring). EVALUATOR = `find_regressions()` (confidence-drop ≥ 0.2). PLANNER is **implicit** — the person list is scraped from the live HTML, not an explicit plan; acceptable for this domain but undocumented as a role. |
| (b) State-on-disk + restart-safe | **PASS** | `letter_writers.json` + `letter_writers_prev.json` persist state; `wire_letter_writers` is idempotent (sentinel strip+inject, byte-stable since the 2026-06-18 fix). A mid-run kill re-runs cleanly. |
| (c) Traceable | **PARTIAL** | Emits a JSON run-summary to stdout (→ `letter-writers-refresh.stdout.log`) + bus events (routine + regression). **Gap**: no per-person scrape trace — an ambiguous PubMed name silently lands as low-confidence "verifying field-of-interest" with no recorded reason for *why* it couldn't resolve. Borderline loud-degradation: the low-conf sentinel carries a label but not a machine reason (`no-match` vs `ambiguous` vs `network`). |
| (d) **Current bottleneck** | — | **CORRECTION (2026-07-03, Kleiber MSG-6a12f3 + my own re-read): L2 ORCID IS wired**, not stubbed — `probe_orcid` (`letter_writer_scrape.py:232`) + `orcid_disambiguate` (`:179`) implement the ORCID tie-breaker with real endpoints; only **L3 (WebFetch bio page) is stubbed** (and the module docstring `:18` staleley still says L2 "stubbed" — corrected in this pass). So the true bottleneck is narrower: names that L1-PubMed can't disambiguate AND ORCID can't resolve fall through to the L3 stub and stay low-confidence. Second-order: serial per-person PubMed calls (fine at ~15 people). *(My original "L2/L3 stubbed" was a stale-surface read of the docstring — the code was ahead of its own comment.)* |

### Loop B — Tenure-readiness watcher (`tenure_readiness` via `tenure_readiness_cron.sh`), daily

| Axis | Score | Evidence |
|---|---|---|
| (a) Role separation | **N/A-correct** | Pure EVALUATOR (scores HTML vs the four audience rubrics, diffs vs baseline). No planner/generator by design — it's a monitor, and monitors shouldn't generate. Correct shape. |
| (b) State-on-disk + restart-safe | **PASS** | `tenure_readiness_baseline.json` persists; each run writes a dated `.json`+`.md`. Deterministic + restart-safe. |
| (c) Traceable | **PASS (over-traced)** | Every run writes a full human `.md` + machine `.json` — excellent debuggability. Over-traced to the point of O-1 (unbounded git accumulation). |
| (d) **Current bottleneck** | — | **The baseline is manual (`--baseline` flip).** After any *intentional* site change, if nobody re-baselines, every subsequent run reports the intentional change as a "regression" (exit 1) indefinitely → the signal decays to noise (alert fatigue). The bottleneck is baseline lifecycle management, compounded by O-2 (regression == exit-1). *Fix direction*: auto-baseline on a clean gate pass, or a "acknowledge this drift" step that advances the baseline. |

**Cross-loop finding**: neither loop has a **planner** that decides *what* to refresh based on outcome — both re-do the full sweep every run. For 15 people / one HTML file that's fine; if the site grows (10x-2 multi-lab), a planner ("only re-scrape people whose data is > N days old / only re-grade changed sections") becomes the scaling lever. Noted, not urgent.

## 4. UX Walkthrough (Playwright, brand-new-user)

Method: served `compare-purple-gold.html` locally (`python3 -m http.server`), drove Playwright MCP at desktop 1280×800 and mobile 390×844, probed the DOM directly (not just a screenshot) for every claim. Evidence: 0 console errors/warnings, all 11 network requests 200 (hero WebP `hero-microscopy-composite-2-vdr-c2c12.webp` served live on the LCP path — the −74% asset confirmed), screenshot `roizen-ux-hero-desktop-2026-07-02.png`.

### Path 1 — Landing → hero → Big Questions (a committee member / journalist's first impression)
- **Load & hero: clean and credible.** 1 `<h1>` ("Redefining Vitamin D"), dual institution header (CHOP · Penn), gold CTA, on-brand purple/microscopy. No console errors, no layout shift observed. First impression lands.
- **Confusion/dead-end — 3 "Figure pending" placeholders (Q2/Q3/Q7).** The flagship "Big Questions" section shows 3 visible "Figure pending" blocks out of 7. A curious reader hits a wall on ~40% of the questions. Honest (anti-fabrication — correct not to fake data), but a **rule-8 polish gap on the front-door section a committee reads first.** Ties to 10X-5. *Jeff-gated (needs real figures).*
- **Rule-4 opportunity, not defect**: the hero and questions are entirely static — no scroll-reveal, no motion. Passes the rule (reduced-motion honored); misses the front-door *showcase* bar (10X-4).

### Path 2 — Nav → Team / Collaborators / Publications (a collaborator / reviewer credibility check)
- **Nav integrity: PASS.** 8 section links + logo, **every href resolves to a real on-page anchor — 0 dead `href="#"`** (donate went live e086df8). Smooth.
- **Publications ("Selected Papers") — no freshness signal.** Static list, **no `data_as_of`, no citation counts** — a reviewer can't tell if it's current or a 2026 snapshot (Data-Provenance gap). Directly the 10X-3 case. *Semi-autonomous (Archivist feed).*
- **Minor a11y**: the logo nav link has empty text content (`href="#home"`), relying on the logo `<img alt>` for its accessible name — acceptable (the img has alt) but worth an explicit `aria-label` for robustness.

### Path 3 — Join Us → Contact (a prospective trainee)
- **Form craft: PASS.** 5 fields, **all with `<label for>`**; a honeypot field (`contact-website`) is present and correctly labeled (spam trap); designed Send button + a form-status live region in markup.
- **Funnel gap (not a bug)**: submission is Layer-1 (Formspree + ntfy) with no live confirmation state exercised in-sandbox; the triage + auto-confirmation step is 10X-7.

### Cross-cutting web-quality rule scan (rendered surface, both breakpoints)
| Rule | Verdict on the walk | Evidence |
|---|---|---|
| 1 Tokens / 2 Type / 3 Layout | PASS (no NEW issue) | PR-1 tokenization holding; 1 h1, 10 clean `<h2>` sections, no ad-hoc drift surfaced. |
| 4 Motion | PASS + opportunity | reduced-motion honored; no showcase motion (10X-4). |
| 5 Performance | PASS-wiring | hero WebP served on LCP path, 0 console errors; **CWV still deploy-time-only** (no Lighthouse — DEPLOY.md §Post-deploy). |
| **6 Responsive / touch targets** | **VIOLATION (the one concrete finding)** | 390px: no h-overflow ✓, nav collapses to a working hamburger (aria-expanded flips true, all 9 links reveal) ✓ — **BUT the hamburger is 21×29px and every open menu link is 19px tall, all < the 44px minimum.** The PRIMARY mobile navigation is sub-target; this audience reads on phones. Hero CTA 48px ✓ / Donate 51px ✓ / Send 40px (marginal). |
| 7 A11y | PASS | 15/15 non-empty alt, all form labels, aria-expanded toggle correct, skip-link + landmarks (per assessment). Flag: focus-visible not universal (self-assessment #5). |
| 8 Polish | PASS-WITH-FLAG | favicon/meta/OG present, 0 dead links; flags = 3 "Figure pending", focus-visible coverage. |
| 9 Content | PASS | Jeff's voice, no lorem. |

**Walk verdict: no broken flows, no dead ends except the 3 pending figures. One concrete rule violation — rule-6 mobile tap-target sizing (nav 19–29px).** Everything else is either known-and-tracked (showcase motion, pending figures, living publications) or passing.

---

## Consolidated top findings (across all 4 sections)

1. **[§4 · ship-blocker-class] Mobile nav tap targets 19–29px (< 44px).** The hamburger (21×29) and all 8 open-menu links (19px) violate web-quality rule 6 on the surface most of this audience uses. Small, high-value fix (nav-link vertical padding + a ≥44px toggle hit-area). *Autonomous, one gated PR.*
2. **[§2/§3 · correctness] Both cron loops mis-signal outcome via exit code** — a *detected* confidence-regression / readiness-regression returns exit 1 (read by launchd as a job failure), and `tenure_readiness` daily reports accumulate unbounded in git. Fix exit semantics + rotate reports. *Autonomous.*
3. **[§1 · strategy] The 10X ceiling is not craft, it's reach + product-shape**: the site reaches zero users until **hosting** (10X-1, Jeff-gated); the biggest product leap is **render-from-config → a reusable lab-site generator** (10X-2, has a real market); the biggest engagement leap is the **WebGL molecular hero + scroll-reveal** (10X-4, held for Jeff/Rams). Craft is already near-bar; the step-changes are these three.

*All findings REPORT-ONLY. Any that becomes a build routes through the normal gate (Kleiber's WEB-QUALITY lens + pytest/site-qa).*

# Roizen Lab Website — hypothesisdriven.org

## Call me "Ace Scout" — sharp, capable, trustworthy, and conscientious. The kind of teammate who sees the whole field and always knows what's next.

**Spirit: Owl** — patient, wise, sees in the dark. Tenure demands careful, unhurried credibility. When the path is unclear, the owl watches longer before moving.

## Quick Status
- **State**: live on Opus 4.8 (Wave-2 restart confirmed 2026-05-28 20:24 EDT, tree clean at `6e5caa4`, 116 passed/4 NET-skipped). WMF PNG-only proposal surfaced to Kleiber via tmux 20:24 EDT (was queued for AM; sent now per always-now). Both remaining grade-C blockers are Jeff-gated: 3 banned-phrase prose rewrites (all 4 staged in design-review packet) + figure-pending PNG-only decision. Queue exhausted of unblocked work. Railway-token inventory (2026-05-25): Ace Scout consumes `TRIAL_BUS_TOKEN` only via `scripts/get-fitness-cred.sh`; never references `RAILWAY_TOKEN`/`RAILWAY_TOKEN_ULYSSES`.
- **Blocking**: (unchanged) Jeff creative picks in `prototypes/design-review-2026-05-14.html` (hero verb / Q layout / Q reorder / 4 prose rewrites). Formspree signup + ntfy topic subscribe still pending. Archivist counter-sig on `docs/contracts/archivist-publications.md`. WMF PNG-only proposal still awaiting Jeff decision.
- **Next**: post-restart, surface WMF PNG-only proposal + figure-candidates gallery to Jeff via Kleiber at AM briefing; resume queue-march per `feedback_vision_queue_march_always.md`.
- **Last touched**: 2026-05-28 (4.8 close-compact prep; credential inventory completed 2026-05-25, WMF retro 2026-05-23)

---

## Decision Queue

> **Strong Default Protocol:** Each decision has a CM recommendation. Jeff only needs to veto, not choose from scratch. If the override window expires with no response, the decision is marked "timed out — holding" (NOT auto-approved). Jeff must actively confirm or override.

### Logo Selection — DECIDED
- **Decision**: jeff-logo-2 (6.02:1 ratio, 355px @ 60px nav height, widest of the set)
- **Color variants needed**: Create versions with (a) letters same color as car-DNA mark, and (b) letters in a different/contrasting color. Jeff to pick.
- **Favicon**: Car icon only (`favicon-hd-car.svg`) — all jeff-logos are too wide for favicon. Already built.
- **Decided**: 2026-02-27

### Theme Selection — DECIDED
- **Decision**: purple-gold (`--primary: #3B1F6E`, `--accent: #C5A336`)
- **Layout**: Ethan Goldberg-style dual header — dark purple institution bar (CHOP + CHOP RI left, Penn Medicine right) fixed above white nav bar with Jeff's logo + nav links. 1px gold border-bottom on institution bar.
- **Logo**: `jeff-logo-2-theme-purple.svg` — recolored to match theme primary (#3B1F6E), stroke removed for sharpness, `shape-rendering: geometricPrecision`, sized 55px height in nav.
- **Hero heading**: "Redefining Vitamin D"
- **Decided**: 2026-03-06

### Big Questions Text — TIMED OUT, HOLDING
- **Status**: Override window expired Mar 7 — holding with current 7 questions
- **Current set**: Q1 "Low Vitamin D: Cause or Effect?", Q2 "How Does Disease Lower Vitamin D?", Q3 "Same Dose, Different Results", Q4 "Is the Dose the Drug?", Q5 "How Does High-Dose D Prevent T2 Diabetes?", Q6 "What Determines Calorie Allocation?", Q7 "The Missing Biomarker"
- **Figures**: All 7 extracted from PPT, wired in. **Jeff flagged figure-to-question matching may be wrong — needs review.**
- **To confirm or override**: Any session

### Join Us Card Text — DECIDED
- **Decision**: Custom version combining funding honesty + Option A language
- **Final text**: "We currently do not have hard funding for additional personnel, but are always looking to identify curious, enthusiastic, hard-working people who want to do careful, ambitious science — the kind that moves the boundaries of knowledge, even if only by a few millimeters."
- **Decided**: 2026-03-12

### Microscopy Composites — TIMED OUT, HOLDING
- **Status**: Override window expired Mar 7 — holding with all 3 composites, purple-gold tint
- **To confirm or override**: Any session

### Contact Email — DECIDED 2026-04-16
- **Decision**: `jeffroizen@gmail.com` (confirmed via Kleiber)
- **Implementation**: Contact form Layer 1 built (Formspree email + ntfy `roizen-lab-contact` phone push). 2-minute Jeff unblock in `docs/contact-form-status.md`.
- **Layer 2 (Telegram to Kleiber)**: backlogged — needs Pilot Railway endpoint + Jeff deploy approval.

### Deferred (no deadline)
- [ ] **CHOP Foundation donation URL** — Use placeholder until URL obtained from CHOP dev office. No deadline.
- [ ] **Merch strategy** — Placeholder section, no real store. Lowest priority. No deadline.
- [x] **Philosophy paragraph** — RESOLVED. Jeff dictated own version (Picking Questions + Improv Framework). APPROVED.

---

## Instruction Register

> Track Jeff's explicit instructions. Record within 1 minute. Never silently drop.
> Note: The section heading follows the markdown format extracted by the session-start hook. No hook modification is required.

- 2026-04-16 (via Kleiber): "Call me Ace Scout" → DONE (CLAUDE.md, memory).
- 2026-04-16 (via Kleiber): "ALWAYS tmux responses back to Kleiber for inter-CM communication" → IN-PROGRESS (used for all recent responses).
- 2026-04-16 (via Kleiber): "OVERNIGHT AUTONOMOUS MODE. Do NOT push to remote without Jeff." → IN-PROGRESS (working local-only; working file is `compare-purple-gold.html`).
- 2026-04-16 (via Kleiber): "Contact email is jeffroizen@gmail.com; text Jeff via ntfy AND send Kleiber a Telegram when someone emails through the site" → Layer 1 DONE (Formspree + ntfy); Layer 2 (Telegram to Kleiber) DEFERRED to Pilot Railway endpoint pending Jeff deploy approval.
- 2026-04-16 (via Kleiber): "Reflect on platonic vision, tmux the answer, start 3 autonomous improvements" → reflection tmux'd; 3 improvements queued in Quick Status; paused by next instruction.
- 2026-04-16 (via Kleiber): "/close + /compact at next natural stopping point, then resume" → DONE.
- 2026-05-20 (via Kleiber MSG-0e9151): "LibreOffice installed; WMF conversion delegate available; resume figure-pending close" → FAILED 2026-05-23 after 4 attempts (see Session Log). Replacement task: surface PNG-only proposal to Jeff at AM briefing.
- 2026-05-14 (via Kleiber): "Pick up overnight, product-quality, no remote push without Jeff" → IN-PROGRESS.

---

## Key Constraints
- **Tenure clock**: End of 2026. Letters solicited ~Sep 2026. Site must be live and polished by Aug 2026. Every decision should pass through the lens of "does this help Jeff's tenure case?"
- **No build system**: Plain HTML/CSS/JS. Edit files directly, preview in browser. Working file: `compare-purple-gold.html`. Production scaffold in `production/`.
- **Cross-project dependency**: Receives publication list from Archivist (MR VitD).
- **200+ files in root**: Mostly debug SVGs and logo iterations. Key files listed in `docs/score_reference.md` Architecture section.
- **Decision journal**: Log autonomous decisions via `python3 ~/Desktop/"Claude Apps"/"Claude coding Asst"/decision_journal.py log "Ace Scout" "decision" -r "rationale" -a --category content`. Categories: content, design.

---

## Operating References
- Follow operating model in `~/Desktop/Claude Apps/Claude coding Asst/docs/cm_operating_model.md`
- Deep context: `docs/score_reference.md` (Vision, Domain Knowledge, Architecture, Current State, Agent Playbook, Source Material)
- Older sessions: `session_archive.md`

---

## Session Log
- 2026-05-28 (20:24 EDT, restart-live, ~5 min): **Wave-2 Opus 4.8 relaunch confirmed.** Verified live (tree clean `6e5caa4`, both prototype artifacts present, 116 passed/4 NET-skipped). Surfaced WMF PNG-only proposal to Kleiber via tmux now (per always-now, not held for AM). Confirmed both grade-C blockers Jeff-gated: 3 banned phrases (compare-purple-gold.html:793/905/1141) all map to the 4 staged prose rewrites in design-review packet; figure-pending awaits PNG-only decision. No unblocked queue work remaining; idle pending Jeff.
- 2026-05-28 (close-compact, ~5 min): **Wave-2 Opus 4.8 restart prep.** Per Kleiber MSG-c95a27 — Jeff approved orchestra-wide 4.8 restart 2026-05-28 evening (grant prep 2026-05-29); Pilot Wave-1 confirmed live on claude-opus-4-8; Ace Scout + Cartographer Wave-2 (both idle low-risk). Running `/close compact` — state preserves via CLAUDE.md + memory. Kleiber will relaunch via `launch-cm-claude.sh ace-scout --model claude-opus-4-8`. No code changes in this session; nothing uncommitted since `19407eb`.
- 2026-05-25 (late evening, ~10 min): **Urgent Railway-token inventory** per Kleiber MSG-b966c9 (lost-token incident — Jeff generated 2 Railway tokens, Kleiber/Tempo rotated one out, tokens missing). Searched `.env*` (none in repo), `docs/`, `scripts/` for token names + URLs only, no values: (a) `TRIAL_BUS_TOKEN` referenced by `scripts/bus_emit.py:70` and both watcher plists, consumed via `scripts/get-fitness-cred.sh TRIAL_BUS_TOKEN ace-scout`; (b) `RAILWAY_TOKEN` + `RAILWAY_TOKEN_ULYSSES` exist as keys in `~/.fitness-credentials.env` (orchestra-shared, mtime 2026-05-20 14:27) but Ace Scout never reads them; (c) URL `https://ulysses-production.up.railway.app/api/role-balance-trial/events` in 3 files (bus_emit.py:36 + 2 plists); (d) unrelated `TELEGRAM_BOT_TOKEN` mentioned in `docs/contact-form-status.md:61` (Layer-2 contact-form path). Token-rotation commits in this repo: none. Net: Ace Scout is consumer-only of `TRIAL_BUS_TOKEN`; does not own/generate/rotate Railway tokens. Reported back to Kleiber.
- 2026-05-23 (late evening, ~80 min): **WMF conversion dead-end retro.** Per IR top item (2026-05-20 Kleiber MSG-0e9151). 4 documented attempts on `extracted-figures/Q2-hepatic-enzyme/cyp2r1-ko_slide01_img1.wmf` (representative): (1) `soffice --headless --convert-to png` direct → hung >2min, no PNG, no log, no stderr; (2) same with isolated profile dir (`-env:UserInstallation=file:///tmp/lo-profile`) and `--norestore --nologo --nodefault --nofirststartwizard` → hung >3min, zero output; (3) `magick file.wmf out.png` → delegate calls `'libreoffice' --convert-to pdf` via `sh -c`, `libreoffice` not on default PATH (only `soffice` is — symlinked to `~/bin/libreoffice` but `sh -c` doesn't inherit), magick hung ~30min then killed; (4) renamed to `.emf` (file is actually EMF v0x10000 per `file`), same isolated-profile soffice, bounded by background-watcher kill at 180s → exit 0, zero output. **Layer 3 finding** (Redundant Solutions): every Q2/Q3 slide that has a WMF also has at least one PNG already extracted (slide02 wmf+png; slide08 png+png+wmf; slide09 wmf+wmf+png+png; slide10 wmf+wmf+png+png; etc.). WMFs are vector chart embeds; PNGs are the micrographs/photos — the tenure-relevant ones. Recommendation to Jeff at AM briefing: ship figure-candidates with existing PNG set; figure-pending closes via Jeff decision rather than WMF unlock; takes watcher grade C→B without needing the conversion. No remote push.
- 2026-05-19 (full overnight + day session): **12 commits — credibility-engine infrastructure.** (1) `scripts/tenure_readiness.py` + 23 tests — 4-audience rubric watcher with baseline diff. (2) `docs/contracts/archivist-publications.md` — Data Provenance contract draft for publications feed. (3) `scripts/publications_feed.py` + 21 tests — consumer-side parser with staleness banner, plugs in when Archivist signs. (4) `scripts/letter_writer_scrape.py` + 32+3-NET tests — L1 PubMed e-utils + L2 ORCID fallback. Real signal for all 10 letter-writers; Romberg L1→L2 promoted (PubMed name collision → ORCID iD 0000-0002-1881-5318 disambig via institution-name=CHOP; field went from 'multisystem/inflammatory/syndrome' to 'genetic/cells/immunodeficiency/tonsillar' — his real B-cell field). (5) `scripts/wire_letter_writers.py` + 15 tests — idempotent injector renders field-of-interest on every people card with low-conf 'verifying' indicator. (6) Cross-CM bus emitter `scripts/bus_emit.py` + 17 tests — Pilot schema camelCase + string confidence buckets + HTTPError body capture. FIRST CROSS-CM EVENT LANDED: ace-scout/research.commit/skipped:planning-kind/HTTP 200, visible in /inbox alongside Tempo + AquaErg (3-CM triangle within the hour). (7) Cron infrastructure: `tenure_readiness_cron.sh` + plist (4hr cadence) + `letter_writers_refresh.py` + plist (Sunday 03:00 weekly) + regression detection. All plists ship CROSS_CM_BUS_TRIAL_ENABLED=0 = safe-canary pattern for Jeff to observe one cycle before flipping live. (8) Memory: `reference_4_audience_rubric_pattern.md` cross-pollination artifact (Edge / Cartographer / Pilot / Archivist audiences enumerated). Rule 3 attempt on WMF: brew install imagemagick ✓, but WMF delegate needs libreoffice install (~700MB) — surfaced via Kleiber. Tests across the day: 89/89 green (23 watcher + 21 publications + 32 scrape + 15 wire + 17 bus + 11 refresh) + 4 NET-gated (PubMed + ORCID disambig + ORCID supersession + live bus probe).
- 2026-05-19 (earlier session): **Tenure-readiness watcher shipped + WMF conversion attempt.** `scripts/tenure_readiness.py` scores the working HTML against the 4-audience rubric (committee/collaborator/journalist/reviewer): dead-link count, figure-pending Qs, alt text, WCAG scaffolding, PI funding signal, image dimensions (SVG excluded), banned prose phrases. Baseline in `docs/tenure_readiness_baseline.json`; subsequent runs diff and exit 1 on regression. 23/23 unit tests green. Current site grade: C (3 banned phrases pending prose-rewrite picks from design-review packet; 3 figure-pendings q2/q3/q7). Rule 3 attempt on WMF conversion: `brew install imagemagick` ✓; but magick's WMF delegate requires `libreoffice` (not installed, ~700MB), and `qlmanage` fails on WMF. Next-step option for Jeff: `brew install --cask libreoffice` to unlock 25+ blind figures.
- 2026-05-14 (overnight): **Design review packet + CLS fix + figure-candidates gallery.** (1) `prototypes/design-review-2026-05-14.html` — side-by-side prototypes for the 4 open creative calls in `docs/jeff-review-2026-04-15.md`: hero verb (A current Redefining / B Rethinking / C Understanding / D no-verb), Big Questions layout (rows vs Anthropic-style grid), Q reorder (current vs narrative-journalist), and 4 prose rewrites (Collaborators/Peers/Mentors/Donate). Anthropic Design auth-walled (claude.ai/design 403); used anthropic.com/research + claude.com/product/overview as design references. (2) CLS fix: added intrinsic width/height to all 11 imgs in `compare-purple-gold.html` (figures, lab-strip, team photos, lab-group, institution-bar logos) with measured pixel dimensions via PIL. `height:auto` preserves ratio with CSS `width:100%`. (3) `prototypes/figure-candidates-2026-05-14.html` — auto-rendered gallery of every PNG candidate in Q2/Q3/Q7 figure subdirs for Jeff to visually pick. WMF conversion blocked: no ImageMagick / LibreOffice / Inkscape installed. Tests: 11/11 green. No remote push (per overnight directive).
- 2026-04-21 (overnight): **Contact form tests + PI card + image optimization + quality sweep.** (1) 11 Playwright integration tests for contact form (structure, honeypot, aria-live, not-configured guard, happy path, error path, network error, button re-enable, ntfy payload, mobile). All green. (2) PI funding signal added: "NIH-funded · Division of Endocrinology & Diabetes · 27 publications" with PubMed link. Strong default — Jeff can edit. (3) Image optimization: hero PNG→JPEG (1044K→304K), q4-dose-response resize (512K→200K), lab-group resize (636K→312K), Mike photo resize (236K→68K), SVG logo SVGO (452K→368K). Added `loading="lazy"` to 7 below-fold images. Total savings ~1.39MB. (4) Quality sweep: fixed base link color `var(--accent)`→`var(--accent-dark)` (WCAG fix), added `tabindex="-1"` to `<main>` for skip-link focus, added focus() after scrollIntoView in smooth-scroll handler, event delegation for nav links, aria-labels on CHOP/CHOP-RI links. Zero console errors, zero broken images/links. Tests: 11/11 green.
- 2026-04-20: **Pub reorg + cross-links + print stylesheet.** Publications reorganized into 3 research arcs with bidirectional Q↔paper cross-links. Print stylesheet for tenure committee packets.
- 2026-04-16 (overnight): **Contact form Layer 1 + autonomous polish.** Formspree + ntfy parallel dispatch. WCAG fixes. Q7 confirmed text-only.

---

## User Preferences
- Call me **"Ace Scout"**
- Visual thinker: render side-by-side previews whenever possible, don't just describe
- Iterative designer: many rounds, walk through options one at a time
- Run background agents for parallel work while brainstorming in foreground
- Broad permissions so work flows without interruption
- When you discover patterns, conventions, or gotchas that would help future sessions, save them to your auto memory.

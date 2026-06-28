# Roizen Lab Website — hypothesisdriven.org

## Call me "Ace Scout" — sharp, capable, trustworthy, and conscientious. The kind of teammate who sees the whole field and always knows what's next.

**Spirit: Owl** — patient, wise, sees in the dark. Tenure demands careful, unhurried credibility. When the path is unclear, the owl watches longer before moving.

## Quick Status
- **State**: live on Opus 4.8[1m]. **LAUNCH-CONTENT APPLIED 2026-06-19 (Kleiber greenlight MSG-b4aa04, commit e086df8)**: 4 de-marketing prose rewrites in Jeff's voice (Collaborators/Peers/Mentors/Donate), donate button now LIVE → `https://giving.chop.edu` (real + tax-deductible; designated-fund URL swaps in post-launch), merch/Gear section hidden for launch + nav link removed (reversible HTML comment). Did NOT auto-touch Big Questions science text or figure captions (scientific claims about figure content — anti-fabrication; already Jeff-voice) — flagged to Jeff for per-item veto. site-qa 6/7 pass (the 1 "fail" = Google-Fonts external load blocked in the network-restricted test sandbox; pre-existing, HEAD fails identically — NOT a regression). AUTONOMOUS-2WK quality march done 2026-06-10 (SEO/JSON-LD/sitemap on canonical file + `tests/site-qa.spec.js` + CLS logo fix). Railway-token inventory (2026-05-25): Ace Scout consumes `TRIAL_BUS_TOKEN` only via `scripts/get-fitness-cred.sh`; never `RAILWAY_TOKEN`/`RAILWAY_TOKEN_ULYSSES`.
- **Blocking**: **ONE thing gates go-live — HOSTING.** hypothesisdriven.org IS registered (Google Cloud DNS) but points nowhere yet. Surfaced to Jeff via iMessage (verified delivered, 1299 chars; Telegram+ntfy failed on sandbox network egress) with exact GH-Pages DNS records (4 A records on `@` → 185.199.108-111.153; `www` CNAME → `jeffroizen-web.github.io`) + a soft-launch-now-on-github.io offer. Prose/donate/merch = DONE (no longer blocking). Optional: Jeff per-item caption veto. Deferred: Formspree signup + ntfy subscribe (contact form Layer 1); Archivist counter-sig on `docs/contracts/archivist-publications.md`; CHOP designated-fund URL (email drafted).
- **Next**: **DEPLOY on Jeff's go.** Either (a) Jeff pastes the DNS records → I deploy via DEPLOY.md Path A (promote `compare-purple-gold.html` → root `index.html`, add `CNAME`, push to `origin`, enable Pages), or (b) Jeff replies "soft-launch go" → I push + enable Pages NOW (live at `jeffroizen-web.github.io/roizen-lab` while DNS propagates). Remote push is Jeff-gated — do NOT push until his go.

- **Last touched**: 2026-06-28 (background-dispatch #4 font-perf-fix DONE: self-hosted Google Fonts → 4 latin variable woff2 in fonts/ + inline @font-face + LCP preload, killed render-blocking external dep; tests/test_fonts.py + runtime site-qa font check, committed 57dbac0 local; 14 py + 18 site-qa green. #1 site-qa-expand (9d0bfd1) / #2 templatize-content (a3a91cc) / #3 wcag-a11y-pass (6ef972c) also done. Hosting still the one go-live gate.)

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

- 2026-04-16 (via Kleiber): "ALWAYS tmux responses back to Kleiber for inter-CM communication" → IN-PROGRESS (used for all recent responses).
- 2026-04-16 (via Kleiber): "OVERNIGHT AUTONOMOUS MODE. Do NOT push to remote without Jeff." → IN-PROGRESS (working local-only; working file is `compare-purple-gold.html`).
- 2026-04-16 (via Kleiber): "Contact email is jeffroizen@gmail.com; text Jeff via ntfy AND send Kleiber a Telegram when someone emails through the site" → Layer 1 DONE (Formspree + ntfy); Layer 2 (Telegram to Kleiber) DEFERRED to Pilot Railway endpoint pending Jeff deploy approval.
- 2026-04-16 (via Kleiber): "Reflect on platonic vision, tmux the answer, start 3 autonomous improvements" → reflection tmux'd; 3 improvements queued in Quick Status; paused by next instruction.
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
- 2026-06-28 (~45 min): **Background-dispatch #4 `font-perf-fix` DONE (gated+merged) — Kleiber MSG-6ebe69, CAP=1.** Did-the-legwork first (Three Hard Rules #3): probed network (reachable) + fetched the real Google css2 to see the woff2 URLs, and checked Lighthouse (NOT installed) BEFORE choosing the approach. Self-hosted all 4 families instead of preconnect-only — the permanent fix (kills the render-blocking cross-origin stylesheet that also made the sandbox console-error check flap). Downloaded latin-subset woff2; discovered via md5 they're VARIABLE fonts (one file/family covers the weight axis) → deduped 15 weight-files → 4 (`fonts/{merriweather,open-sans,inter,playfair-display}.woff2`, ~227KB). Inlined `@font-face` (font-display:swap) into the existing `<style>` (matches all-CSS-in-one-block architecture, no extra request); deleted the redundant fonts.css; preload merriweather (hero h1=LCP) + open-sans (body), crossorigin, to shrink the swap window. **Honest scope note**: Lighthouse not runnable here, so verified CORRECTNESS empirically via Playwright (no external font requests, woff2 load no-404, document.fonts confirms Merriweather/Open Sans loaded) rather than claiming a Lighthouse score I can't produce. Tests: `tests/test_fonts.py` (4) + runtime font check in `site-qa.spec.js` → GATE 14 py + 18 site-qa = 32 green (Run-Don't-Reason, exit 0). Committed `57dbac0` on main LOCAL; clean attribution (reconstructed HTML from HEAD with only my 2 font edits, restored the pending cron field-of-interest refresh to the working tree uncommitted). Holding for #5 dispatch (queue was 4 deep; may be drained — will confirm with Kleiber).
- 2026-06-27 (~40 min): **Background-dispatch #3 `wcag-a11y-pass` DONE (gated+merged) — Kleiber MSG-fcb45a, CAP=1.** Audit grounded in COMPUTED contrast ratios, not the CSS comments (stale-surface-verification). Found 3 real WCAG-AA failures, all white-on-gold #C5A336 = 2.42:1: `.btn` (Explore CTA), `.btn-donate` (both themes), `.nav-links a:hover`. FIXED design-preservingly — kept the theme-defining bright gold, swapped text to the theme's own purple: light `--btn-text` → `#3B1F6E` (5.39:1), `.btn-donate color` → `var(--primary)` (5.39:1 light / ~9:1 dark), nav-hover → `--accent-dark` (5.0:1). AUDITED & already-passing (no change): all form inputs have `<label for>`, lang=en, skip-link, nav aria-expanded toggle, form-status live region, heading hierarchy no-skips, 15/15 non-empty alt, body/heading text 5.7–14:1. Added `tests/test_contrast.py` (parses both theme palettes, asserts every text/bg pair ≥4.5:1 + a direct white-on-gold-button regression guard). GATE: 10 py (5 contrast + 5 content-contract) + 17 site-qa = 32 green (Run-Don't-Reason, exit 0). Committed `6ef972c` on main LOCAL — clean attribution: reconstructed the HTML from HEAD with ONLY my 3 color edits (git-checkout + asserted sed re-apply), committed, then restored the pending cron field-of-interest refresh to the working tree uncommitted (left for the letter-writer pipeline). Report to Kleiber: 3rd consecutive box-wedge handling expected → will quiet-ledger if wedged. Holding for #4 `font-perf-fix` dispatch.
- 2026-06-27 (~45 min): **Background-dispatch #2 `templatize-content` DONE (gated+merged) — Kleiber MSG-1b0111, CAP=1.** Increment 1 of templatization, scoped autonomous-safe via Premortem: extracted the STABLE Jeff-specific content out of the monolithic `compare-purple-gold.html` into `content/site-content.json` (meta, hero, 7 Big Questions+figures, team, collaborators, peers, mentors, publications→`data/publications.json`, news, alumni, donate, contact, links) + `tests/test_content_contract.py` (drift guard: every contract value must appear in live HTML via entity-unescape+tag-strip+collapse normalization; structural counts; figure-src-exists; cron-field boundary guard) + `docs/specs/content-contract.md`. **KEY DECISIONS**: (1) did NOT touch the launch-ready HTML — it stays render-authoritative, zero launch risk; the render-from-config FLIP is JEFF-GATED (build step crosses the documented no-build-system constraint + SEO risk), flagged in the spec as the next increment, NOT auto-built. (2) Deliberately EXCLUDED the cron-managed `.field-of-interest` spans (`wire_letter_writers.py` owns them — Producer-Owns) so the guard stays green; validated LIVE — the only pre-existing HTML diff in the tree is exactly that cron field-of-interest content, which the contract correctly ignores. GATE 5/5 pass (pytest exit 0, Run-Don't-Reason). Committed `a3a91cc` on main LOCAL (push Jeff-gated; scoped to my 3 new files, did NOT commit the cron-modified HTML — that's the letter-writer pipeline's to commit). Report to Kleiber hit a 2nd box-wedge ('keep dispatching as builds land', 4/4 retries) → quiet-ledgered (MSG-0ed481, drains on recovery); did NOT force-recover; logged to failure ledger (input-box-wedge ×2 this session). Holding for #3 `wcag-a11y-pass` dispatch.
- 2026-06-27 (~30 min): **Background-dispatch #1 `site-qa-expand` DONE (gated+merged) — Kleiber idle-dispatcher MSG-368fd3, orchestra CAP=1.** Ran inline-gated (not full /pipe3 agent fleet — test-files-only, reversible, sidesteps Mini OOM cap). Grounded every new assertion in actual HTML first (greped nav hrefs, ids, JSON-LD, alt emptiness, dead-`#` count) so the net is a TRUE regression guard, not aspirational. Expanded `tests/site-qa.spec.js` 7→17: internal-anchor integrity, primary-nav 8-anchor completeness, dead-`#`-href guard (donate-live/merch-hidden launch regression), external-link hygiene (format-only — sandbox-safe, no live fetch), donate `giving.chop.edu` content guard, non-empty alt (stricter than CLS test), skip-link target, JSON-LD depth (@context/url/parentOrg CHOP+Penn/member.affiliation), 768px breakpoint (lab-website.md mobile edge). GATE 17/17 pass locally (Run-Don't-Reason: ran the real suite, exit 0). Committed `9d0bfd1` on main LOCAL (remote push Jeff-gated, bundles w/ deploy); scoped to the test file only, did NOT sweep cron-modified data files. Reported gated+merged to Kleiber → slot released; queue #2 = `templatize-content`, holding for his dispatch. Earlier this session: design-lens reply to Tempo (/pipe3 vision, A-then-C) + portfolio-audit + definitive build-queue to Kleiber.
- 2026-06-19 (~40 min): **LAUNCH-CONTENT APPLIED — Kleiber greenlight MSG-b4aa04 (box recovered from wedge by Kleiber kill+resume; the unattributed "yes pre-apply" draft was NOT treated as Jeff's, greenlight covers it).** Committed e086df8: 4 de-marketing prose rewrites in Jeff's voice (Collaborators "People who make our work better." / Peers "Scientists we talk to." / Mentors "People who trained us." / Donate "Your donation buys reagents, mice, and people-hours. That's it."), donate button dead `#` → `https://giving.chop.edu` (real + tax-deductible), Gear/merch section hidden + nav link removed (reversible HTML comment). **Held the anti-fabrication line**: did NOT auto-rewrite Big Questions per-question science text or figure alt/captions (they make scientific claims about figure content + are already Jeff-voice) — flagged to Jeff for per-item veto. site-qa 6/7 pass; verified the 1 fail is the Google-Fonts external load blocked in the network-restricted test sandbox (stashed HEAD fails identically — pre-existing, not a regression). Surfaced full status + exact GH-Pages DNS records + soft-launch-now-on-github.io (Layer-3) offer to Jeff: **iMessage OK verified via log (1299 chars)**; Telegram+ntfy failed on sandbox network egress (rc=7 / HTTP 000000) — iMessage is primary, so Jeff has it (Producer-Read-Back: checked the log, didn't trust fail-open RC=0). Kleiber coordinated (MSG-be8954 delivered) + signaled READY-TO-PROPAGATE for feedback_idempotency_test_assert_byte_stability.md. **Awaiting Jeff: DNS paste OR "soft-launch go" → deploy via DEPLOY.md Path A (remote push Jeff-gated).**
- 2026-06-18 (late): **Kleiber relay pane WEDGED mid-launch-prep — routed around it.** tmux_send to Kleiber reported MSG-741571 'delivered' via content-match, but a later send's snapshot revealed my full brief was sitting UNSUBMITTED as a frozen draft in Kleiber's input box (false-positive ack; box frozen, needs kill+--resume per wedge_watch). Did NOT force-recover another CM's session. Surfaced launch-critical decisions DIRECTLY to Jeff via notify-jeff (Telegram+iMessage+ntfy all OK, log-verified) — authorized by Kleiber's 'respond to Jeff directly, Single-Voice.' Brief is committed regardless (docs/launch-brief-2026-06-19.md). Awaiting Jeff hosting answer + prose OK.
- 2026-06-18 (~45 min): **Launch prep for 6/19 (Kleiber MSG-1ebe1a, Single-Voice to Jeff).** Wrote decision-ready launch brief (4 Qs: edits/readiness, fundraising-test, merch-provider, full open-Qs); answered fundraising (CHOP-handoff, no sandbox we build, get designated URL or fall back to giving.chop.edu) + merch (Printify rec BUT flagged CHOP/Penn trademark+revenue-routing+tax compliance — recommend hide-for-launch). Staged CHOP dev-office email draft + 4 prose rewrites. **Caught+fixed a cron-compounding bug pre-launch**: wire_letter_writers idempotency defect orphaned a whitespace run every daily run (7 deep, 125 blank lines); class fix (strip leading ws) + 2 byte-stability regression tests that provably fail on old code; canonical file normalized 125->65 blanks + re-wired clean. Also confirmed D1 cron remediation live (daily reports 6/12-6/18 committed). 130 py + 18 pw green. Commits f5e19cf/a6348a1/9df779a. Awaiting Jeff launch decisions.

---

## User Preferences
- Call me **"Ace Scout"**
- Visual thinker: render side-by-side previews whenever possible, don't just describe
- Iterative designer: many rounds, walk through options one at a time
- Run background agents for parallel work while brainstorming in foreground
- Broad permissions so work flows without interruption
- When you discover patterns, conventions, or gotchas that would help future sessions, save them to your auto memory.

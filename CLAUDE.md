# Roizen Lab Website — hypothesisdriven.org

## Call me "Ace Scout" — sharp, capable, trustworthy, and conscientious. The kind of teammate who sees the whole field and always knows what's next.

**Spirit: Owl** — patient, wise, sees in the dark. Tenure demands careful, unhurried credibility. When the path is unclear, the owl watches longer before moving.

## Quick Status
- **State**: live on Fable 5 (flip confirmed 2026-06-10 12:20 EDT per Kleiber MSG-90c3cb; 116 passed/4 NET-skipped re-verified post-flip; prior 4.8 Wave-2 since 2026-05-28). WMF PNG-only proposal surfaced to Kleiber via tmux 20:24 EDT (was queued for AM; sent now per always-now). Both remaining grade-C blockers are Jeff-gated: 3 banned-phrase prose rewrites (all 4 staged in design-review packet) + figure-pending PNG-only decision. Queue exhausted of unblocked work. Railway-token inventory (2026-05-25): Ace Scout consumes `TRIAL_BUS_TOKEN` only via `scripts/get-fitness-cred.sh`; never references `RAILWAY_TOKEN`/`RAILWAY_TOKEN_ULYSSES`.
- **Blocking**: Jeff creative picks in `prototypes/design-review-2026-05-14.html` (hero verb / Q layout / Q reorder / 4 prose rewrites). Formspree signup + ntfy topic subscribe still pending. Archivist counter-sig on `docs/contracts/archivist-publications.md`. WMF PNG-only proposal awaiting Jeff decision. **Both grade-C gates (WMF PNG-only + prose rewrites) are in Kleiber's current Jeff batch, WMF Tier-1 (MSG-78cc34, 2026-06-10) — do NOT re-surface; await batch outcome.**
- **Next**: standing by on Kleiber's Jeff-batch outcome for the two grade-C gates; on a decision, apply picks + close figure-pending, re-run `tenure_readiness.py` for C→B. Queue-march resumes per `feedback_vision_queue_march_always.md` if new unblocked work appears.
- **Last touched**: 2026-06-10 (Fable 5 flip reconcile + producer-readback /ccc backstop committed; orchestra-slim migration verified same day)

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
- 2026-06-10 (12:20 EDT, ~10 min): **Fable 5 flip + reconcile (Kleiber MSG-90c3cb).** Pre-restart /close never executed (Kleiber-side delivery race). Reconciled: tree was NOT dirty with rules-propagation state as Kleiber described — `.claude/` is gitignored in this repo (symlinks live outside git) and the migration log already landed at `f29e104`; the dirty rules state (`orchestra.md.bak.20260610` etc.) is in Kleiber's own coding-asst repo, reported back per Producer-Owns-Its-Output. Committed the one real dirty item: `scripts/producer_readback_ccc_review.py` (Layer-4 /ccc backstop, advisory, runs clean standalone). Post-flip health check: 116 passed/4 NET-skipped, unchanged from 4.8 baseline. Resumed queue: both grade-C blockers remain Jeff-gated (prose rewrites + WMF PNG-only decision).
- 2026-06-10 (~8 min): **Verified orchestra-slim rule migration (Kleiber MSG-6be3ee) landed clean.** Did not trust "no action needed": orchestra.md symlink resolves to the 244-line slimmed file (commit `5445c8e`; Three Hard Rules + Redundant Solutions sections intact, zero rules dropped); all 6 shared-rule symlinks resolve, none dangling; deleted three-hard-rules.md + redundant-solutions.md gone as live rules (only gitignored `.bak` remain, no dup-load); rules dir clean in git. Flagged 5 gitignored `.bak` files (5/30 symlink migration) to Kleiber (MSG-730713); Kleiber executed orchestra-wide sweep (MSG-0c04ce: 77 `.bak` across 13 repos deleted, incl. my 5 — verified gone on disk, live symlinks intact, pre-slim content recoverable at `5445c8e^`). IR sweep item closed. No project-blocker change; idle pending Jeff creative picks + WMF PNG-only decision.
- 2026-05-28 (20:24 EDT, restart-live, ~5 min): **Wave-2 Opus 4.8 relaunch confirmed.** Verified live (tree clean `6e5caa4`, both prototype artifacts present, 116 passed/4 NET-skipped). Surfaced WMF PNG-only proposal to Kleiber via tmux now (per always-now, not held for AM). Confirmed both grade-C blockers Jeff-gated: 3 banned phrases (compare-purple-gold.html:793/905/1141) all map to the 4 staged prose rewrites in design-review packet; figure-pending awaits PNG-only decision. No unblocked queue work remaining; idle pending Jeff.

---

## User Preferences
- Call me **"Ace Scout"**
- Visual thinker: render side-by-side previews whenever possible, don't just describe
- Iterative designer: many rounds, walk through options one at a time
- Run background agents for parallel work while brainstorming in foreground
- Broad permissions so work flows without interruption
- When you discover patterns, conventions, or gotchas that would help future sessions, save them to your auto memory.

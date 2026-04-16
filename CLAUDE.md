# Roizen Lab Website — hypothesisdriven.org

## Call me "Ace Scout" — sharp, capable, trustworthy, and conscientious. The kind of teammate who sees the whole field and always knows what's next.

**Spirit: Owl** — patient, wise, sees in the dark. Tenure demands careful, unhurried credibility. When the path is unclear, the owl watches longer before moving.

## Quick Status
- **State**: between-sessions — contact form Layer 1 built, reflection tmux'd to Kleiber, committed to 3 autonomous improvements. Pausing for /close + /compact per Jeff instruction. Fresh context next session.
- **Blocking**: 2 Jeff-unblocks (see `docs/contact-form-status.md`): Formspree signup + ntfy topic subscribe. 9 creative decisions remain in `docs/jeff-review-2026-04-15.md`.
- **Next autonomous work (committed in reflection, pick up on resume)**:
  1. **Reorganize Publications by research-arc theme** (Phenotype / Mechanism / Translation) matching the Current Projects cards, instead of flat reverse-chronological. Publications become a story.
  2. **Cross-link Q-to-Papers**: each Big Question anchors to its publication group. Turns two separate sections into a navigable evidence map.
  3. **Print stylesheet**: tenure committees print the page for review packs — currently renders poorly (nav bar, dark overlays waste ink). Add `@media print` rules: hide nav/footer/lab-strip, force visible email, proper section page-breaks, no dark hero. Zero creative calls; huge committee-pack payoff.
- **Next** after the above: Jeff to work creative queue. Layer 2 (Telegram → Kleiber on contact form submit) backlogged to Pilot (Ulysses) pending deploy approval.
- **Last touched**: 2026-04-16 (overnight — contact form Layer 1 + reflection)

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
- 2026-04-16 (via Kleiber): "/close + /compact at next natural stopping point, then resume" → IN-PROGRESS (closing now).

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
- 2026-04-16 (overnight, contact form): **Contact form Layer 1 built.** Kleiber confirmed jeffroizen@gmail.com as contact email with additional real-time push to Jeff's phone (and a Layer 2 Telegram-to-Kleiber later via Pilot Railway endpoint). SD pre-flight: flagged that /notify-jeff is local-only (can't be invoked from browser), so architecture routes visitor→Formspree (email) + client-side fetch to ntfy.sh/roizen-lab-contact (phone push) in parallel. Plan reported and approved by Kleiber before building. Built: contact form UI (name/email/subject/message, Jeff's direct/real copy style, no pretentious fluff), preserved Location/Email/Join-the-Lab info blocks in left column, form in right column with purple left-accent and gold send button. CSS: form-field focus rings, `.was-submitted` class-gated invalid styling (replaces fragile `:placeholder-shown` approach), responsive 2-col→1-col at 768px. JS: parallel Formspree POST + ntfy POST with fire-and-forget semantics (ntfy failure doesn't block email), HTML5 validation guard, explicit "not configured" fallback pointing to jeffroizen@gmail.com, success/error status with aria-live. Honeypot anti-spam. Tested 6 paths via Playwright: initial clean state, submit-empty + browser validation, not-configured fallback, happy path (both endpoints called + success + reset), error path (Formspree error msg + fallback + form preserved), desktop and mobile. Wrote `docs/contact-form-status.md` — Jeff's 2-minute unblock steps (Formspree signup + ntfy topic subscribe). Layer 2 (Telegram-to-Kleiber) deferred to Pilot Railway endpoint pending deploy approval. NOT deployed per orchestra rules. Working file: `compare-purple-gold.html`.
- 2026-04-16 (overnight): **Overnight autonomous polish.** Fixed warm-slate theme missing `--accent-dark` variable (was a real bug — theme toggle would break body-text gold elements). Also fixed warm-slate `--text-muted` from `#8A8A9A` (3.39:1 fail) to `#666666` (passes WCAG AA). Exhaustively viewed all Q7-biomarker/ candidates (crystal structures, DAPI histology, seasonal 25(OH)D variation) — none match "missing biomarker" concept. Q7 confirmed text-only. Changed lab-strip `<figure>` to `<div>` (semantic fix — no `<figcaption>` means `<figure>` was misused). Cross-referenced all 16 local src/href paths — zero broken. Systematic breakpoint test at 360px/768px/1024px/1400px via Playwright — no layout breakage at any viewport. Cleaned up Playwright screenshot artifacts. CLS analysis: all image containers already use CSS aspect-ratio or fixed dimensions — HTML width/height would be redundant. Checked for remaining `color:var(--accent)` inline styles — all converted to `accent-dark` in prior session. All autonomous technical work exhausted. State: waiting-on-jeff to work `docs/jeff-review-2026-04-15.md` decision queue.
- 2026-04-15 (later): **Full-site stress test.** Kleiber dispatched site-wide polishing. Flagged that `/sd`, `/architecture-scan`, `/red-blue-scan`, `/find-skill` claimed in the Kleiber banner do not exist in `~/.claude/skills/` or `~/.claude/commands/` (only sparring-david-persona.md doc exists). Read SD persona — noted that creative decisions (framing, voice, visual direction) are SD's HARD-STOP boundary, so I did not pretend to SD-approve Jeff's prose/narrative calls. Instead: (1) spawned three parallel agents — WCAG/accessibility reviewer on the HTML, multi-audience content critique (department-chair / collaborator / journalist / grant-reviewer simulation), and a people-sections + photo-vibe reviewer; (2) in parallel, hunted for real Q1/Q2/Q3/Q7 figures outside curated-for-website/ — found Archivist's `paper-ready/figures/Fig5_reverse_causation_bmi_to_vitd_scatter.pdf` which is the literal BMI→25(OH)D reverse-causation MR scatter, converted to PNG and wired into Q1; (3) applied all technical findings autonomously: `--accent-dark: #8A6B1A` for WCAG AA body-text gold (was 2.38:1 fail), `--text-muted: #666666`, skip link, `<main id="main-content">` wrapper, `aria-expanded`/`aria-controls` on nav toggle, `prefers-reduced-motion` media query, favicon links, Penn Medicine aria-label fix, descriptive team-photo alts, `loading="lazy"` on above-fold imgs, removed 6 dead `href="#"` paper-link anchors (donate placeholder retained per deferred decision), disambiguated Hakonarson mentor-card with "Postdoctoral mentor" note, `aria-label="Primary navigation"` on nav ul; (4) wrote `docs/jeff-review-2026-04-15.md` — consolidated 10-item decision queue for Jeff covering everything I did NOT touch because it is creative/taste or requires info I don't have (contact email, Q reorder, prose rewrites, Next-Q lines, funding signal, PhD advisor, photo reorder/swap, "Redefining" hero verb). Verified all fixes in Playwright (desktop 1400px + mobile 390px). Working file: `compare-purple-gold.html`.

---

## User Preferences
- Call me **"Ace Scout"**
- Visual thinker: render side-by-side previews whenever possible, don't just describe
- Iterative designer: many rounds, walk through options one at a time
- Run background agents for parallel work while brainstorming in foreground
- Broad permissions so work flows without interruption
- When you discover patterns, conventions, or gotchas that would help future sessions, save them to your auto memory.

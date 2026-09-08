# Roizen Lab Website — hypothesisdriven.org

## Call me "Ace Scout" — sharp, capable, trustworthy, and conscientious. The kind of teammate who sees the whole field and always knows what's next.

**Spirit: Owl** — patient, wise, sees in the dark. Tenure demands careful, unhurried credibility. When the path is unclear, the owl watches longer before moving.

## Quick Status
- **CANARY — model pin**: `claude-opus-5` (settings.local.json). Fleet is OFF Fable until the Wed 9/09 allowance reset (Kleiber MSG-34fec4). **If the status bar shows Fable 5.1 before Wed 9/09, tell Kleiber — do NOT switch back yourself.** Verify serving-layer at session start with the transcript probe, never the system-prompt line.
- **SITE IS LIVE** → https://jeffroizen-web.github.io/roizen-lab/ (soft-launch 2026-07-03, Jeff GO). Served from `gh-pages` as a lean 2.4M artifact built by `scripts/sync_publish.py` — the 543M source root chokes the Pages build, so NEVER publish the root. No custom domain yet. Unlinked redesign preview at `/preview/redesign/`.
- **Current stint (2026-09-07)**: CLAUDE.md trimmed under the 40KB house cap (Kleiber census MSG-2c4ce2). Prior stint 2026-09-03: Kleiber Tier-0 seal sweep DONE + gated-accepted (638b3cc, MSG-9d3737).
- **GATE (current)**: **249 pytest + 4 skipped + 38 Playwright** (19 site-qa + 11 contact-form + 8). Suite lives in `tests/`; specs `site-qa.spec.js` + `contact-form.spec.js`.
- **Local commits awaiting Jeff's authorised push**: 3 (seal-sweep fix + 2 IR/docs). Standing gate = no remote push without Jeff.
- **WAITING-ON (all Jeff/Kleiber-gated, nothing autonomous open)**: (1) redesign **production flip** — separate Jeff-GO; (2) **custom domain** DNS — Jeff action; (3) **PR-3 WebGL** — Jeff/Rams design direction; (4) **auto-redeploy ARM** — plist repoint + `ROIZEN_AUTO_DEPLOY=1`. Deferred: contact Layer 2 (Telegram), CHOP fund URL, optional per-item caption veto.
- **Token/credential inventory**: consumes `TRIAL_BUS_TOKEN` only, via `scripts/get-fitness-cred.sh`.
- **PENDING OUTBOUND to Kleiber (2026-09-08)**: 2 quiet `kind=info` notes undelivered — his box holds a real unsubmitted draft ("Best") and the pre-send guard correctly backed off rather than clobber it. Bodies at `scratchpad/trim/{rule,push}.txt`: (a) the `.claude` symlink-backing observation, (b) the answer that the unpushed stack is a BLOCKED GATE (Jeff's Tier-2 reservation), not batching. Retry at next contact; do NOT escalate the kind for non-urgent content.

---

## Decision Queue

> **Strong Default Protocol:** Each decision has a CM recommendation. Jeff only needs to veto, not choose from scratch. If the override window expires with no response, the decision is marked "timed out — holding" (NOT auto-approved). Jeff must actively confirm or override.

### Logo Selection — DECIDED
- **Decision**: jeff-logo-2 (6.02:1 ratio, 355px @ 60px nav height, widest of the set)
- ~~**Color variants needed**: (a) letters matching the car-DNA mark, (b) contrasting letters. Jeff to pick.~~ **MOOT 2026-09-07** — superseded by the 2026-03-06 theme decision: `jeff-logo-2-theme-purple.svg` (recolored to `--primary`) has been live in the nav since launch. No Jeff action pending.
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
- [ ] **CHOP Foundation donation URL** — NOT a blocker and NOT a placeholder: donate has pointed at the real, tax-deductible `https://giving.chop.edu` since 2026-06-19 (e086df8). Open item is only the optional upgrade to a lab-DESIGNATED fund URL from the CHOP dev office. No deadline.
- [ ] **Merch strategy** — Placeholder section, no real store. Lowest priority. No deadline.
- [x] **Philosophy paragraph** — RESOLVED. Jeff dictated own version (Picking Questions + Improv Framework). APPROVED.

---

## Instruction Register

> Track Jeff's explicit instructions. Record within 1 minute. Never silently drop.
> Note: The section heading follows the markdown format extracted by the session-start hook. No hook modification is required.
> Fully-closed entries are archived VERBATIM in `session_archive.md` (§"Instruction Register — ARCHIVED 2026-09-07"). Only live/standing items live here.

### Standing (never expire)
- **NO REMOTE PUSH WITHOUT JEFF** (2026-04-16 via Kleiber; reaffirmed MSG-521d3c). origin = Jeff's PUBLIC repo; a push bundles with go-live. A quality/web-quality PASS is clearance ONLY, never release of this Tier-2 reservation. **The LIVE deploy is a gate SEPARATE from the source merge/push** — hold it even on a clean PASS. Settled; do not re-litigate.
- **tmux all inter-CM responses back to Kleiber** (2026-04-16). Quiet kinds `ack|info|coordination` → `--kind` quiet inbox; `actionable|escalation|stopcheck` → his box.
- **ROUTING — web-surface charter** (`Claude coding Asst/docs/teams/web-surface.md`, read 2026-07-05): my team = Ace Scout × Pilot/Tempo, **Rams = design gate**. Design-craft iterations get Rams's intra-arc blessing (handoff = branch + ask; Rams self-writes the verdict) WITHOUT a Kleiber re-run; **Kleiber keeps the final merge gate**; voice-to-Jeff unchanged (my domain = my voice); Producer-Owns unchanged.
- **PROCESS EVIDENCE STAYS OUT OF THE SOURCE ROOT.** `loop-artifacts/`, `loop-output-*.md` and any comparable screenshot/verdict dump are process evidence, NOT product: keep them on the branch, never merge them to main. This is a producer merge-condition I set at the 2026-07-05 /pipe4 and it is load-bearing — the 543M source root is exactly what choked the GitHub Pages build (293M unused extracted-figures + 27M logo iterations), so re-seeding it breaks the live site's deploy path. Enforced in `.gitignore`; restate it as a condition on any future orchestrated merge into this repo.
- **`design-tokens.css` = Rams's design system, the token source of truth** — producers consume, NEVER fork (dual-path-drift). Coordinate any token touch with Rams. **Hallmark = craft ref + GENERATOR for showcase surfaces UNDER the tokens** (ratified Rams b48d6e2 / Kleiber MSG-d37a71): generate w/ Hallmark → conform to tokens → gate w/ the slop-extended lens. Any GENERATE step = separate arc (Rams gate + Kleiber final + Jeff veto-window if the look changes).

### Open / waiting
- **PR-3 WebGL showcase** (hero molecular motif + scroll-reveal + figure animation) — `WAITING-ON: Jeff/Rams design direction`. Kleiber holding; bespoke visual identity = taste call. Full gap list `docs/reviews/web-quality-self-assessment-2026-07-01.md`.
- **#2/#3 redesign PRODUCTION FLIP** — `WAITING-ON: separate Jeff-GO`. Preview is LIVE + unlinked at `https://jeffroizen-web.github.io/roizen-lab/preview/redesign/` (c4e9ef7, fast-forward, production byte-identical `a667e7d1`); Rams tier-3 read-back runs vs the PREVIEW. On GO: redeploy canonical to gh-pages root per `docs/DEPLOY.md`.
- **Auto-redeploy ARM** — `WAITING-ON: Jeff/Kleiber`. Built + gate-PASSED + DISARMED (`scripts/deploy_publish.sh`, fe63089). ARM = plist repoint to `scripts/letter_writers_refresh_cron.sh` + `ROIZEN_AUTO_DEPLOY=1` (recipe in `docs/DEPLOY.md`). Auto-force-push to a public branch on a schedule = a standing external action, hence Jeff-gated. Kleiber batches this with DNS + PR-3.
- **Custom domain** hypothesisdriven.org → GH-Pages — Jeff DNS action (CNAME on gh-pages + 4 A-records / www CNAME).
- **Contact Layer 2** (Telegram to Kleiber on form submit) — DEFERRED, needs Pilot Railway endpoint + Jeff deploy approval. Layer 1 (Formspree + ntfy) DONE.

### Recently closed (detail in session_archive.md)
- 2026-09-07 **trim-loss class** (`archive-pointer-is-a-claim-not-evidence`, Kleiber MSG-bb7ded→MSG-2f9db4→MSG-b5bbdd): f3adad3 lost 9 lines (2 MIXED rows + superseded Quick Status), recovered dea3f8d. **BEFORE ANY FUTURE TRIM run `python3 scripts/archive_verify.py <sha-before>` and require EMPTY on BOTH passes** (6a1de65, final form: versions-not-endpoints, corpus = live∪archive∪docs, line + fact-token granularity, path tokens by exists(), inverse rule-sweep pass). Clause-7 recovered a standing rule that had been swept into the archive. A phrase-grep audits only what you MOVED.
- 2026-09-07 **CLAUDE.md house caps** (Kleiber census MSG-2c4ce2 + ruling MSG-f76a07): trimmed 41,509→16,532 B (closed entries archived VERBATIM), then wired the mandated **BLOCKING** check into the suite — `tests/test_claude_md_caps.py`, both caps named separately, prefix-matched heading with unmatched = FINDING, two-sided bite. **Never convert this to a push hook** (no-push posture = wrong surface). 257 pytest + 4 skipped. Commits f3adad3 + 1901ec8, reported MSG-0b1936.
- 2026-09-03 **seal sweep** (Kleiber MSG-4f32b9): bus_emit ENV-AT-IMPORT + deploy_publish no-floor found empirically + fixed; 7 guards; **GATE 249 pytest + 4 skipped**. Kleiber GATED ACCEPT MSG-9d3737, leg closed both sides. Commit 638b3cc LOCAL, rides the next authorised push.
- 2026-07-09 **HALLMARK** (Jeff MSG-17608d, ruled "All"): #1 hero italic→roman LIVE (32c8de5→e66f5ba); #2/#3 left-editorial-axis built+staged (20119fa) → preview-published per Jeff's NOT-public ruling.
- 2026-07-05 **craft uplift /pipe4** merged 8bf1f4d + LIVE; **Rams flags F1/F2/F3 closed, F4 withdrawn**.
- 2026-07-03 soft-launch LIVE; publications feed wired; loop-hygiene R2/R3/R4/R6; mobile tap-targets.
- 2026-05-20 WMF/LibreOffice figure conversion: FAILED after 4 attempts, MOOT — all 7 Big Questions figures are extracted + wired (PNG). No open action.


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
- 2026-09-07 (~25 min): **CLAUDE.md trimmed under the house cap (Kleiber fleet census MSG-2c4ce2 — Roizen Lab was the only repo over: 41,509B vs the 40,960 cap, Quick Status 5,752 vs 5,120, and NO pre-push gate here to ever catch it).** Archived 14 fully-closed Instruction Register entries + 2 old session-log entries VERBATIM into `session_archive.md` under dated headers (never summarized, so the text stays greppable — script-verified each block byte-present in the archive BEFORE deleting it from CLAUDE.md). Rewrote the register as Standing / Open-waiting / Recently-closed; rewrote Quick Status to canary + live-URL + current-stint + gate + waits. **Moot-blocker pass per Kleiber's tip**: the 2026-05-20 WMF/LibreOffice figure-conversion instruction still read as a live replacement-task since May though all 7 Big Questions figures have long been extracted+wired as PNG — marked MOOT. Also caught Quick Status still claiming "live on Opus 4.8[1m]" after the 9/07 fleet switch to Opus 5. **Retro**: a splice by line-index left one entry orphaned and dropped a `---` separator — re-read the seam, don't trust the slice arithmetic | archive-then-verify-then-delete is the only safe order for a verbatim move | a size cap with no enforcing gate drifts silently for months; the census caught what nothing local would have.
- 2026-09-03 (~30 min): **Kleiber Tier-0 fleet sweep — silently-inert conftest seals (MSG-4f32b9) → DONE + GATED ACCEPT (MSG-9d3737).** Fresh session after the ~/.claude wipe; verified the model pin at the serving layer first. Two real defects found by EMPIRICAL probe (redirect env → run writer → assert the sink moved and the live file is untouched; an env-name grep would have found neither): (1) `scripts/bus_emit.py` built its readback-ledger path as a module constant, so `PRODUCER_READBACK_LEDGER` was captured AT IMPORT — honored under pytest only by fixture-order luck, and the conftest FALLBACK seal never set it at all; (2) `scripts/deploy_publish.sh` had no seal floor, so a bare disarmed run under pytest appended a real row to the LIVE `docs/reports/deploy-publish.jsonl` — a test-fired-prod-side-effect near-miss. Fixed with call-time resolvers (patch-point > seal env > default) + a `REPO_SEAL_FLOOR` in conftest that also forces `ROIZEN_AUTO_DEPLOY=0`/`DRY_RUN=1`. 7 guards, bite-tested (resolver→import-time = 3 red; floor dropped = 2 red). GATE 249 pytest + 4 skipped. Kleiber re-ran it in a detached snapshot worktree and added his own distinct bite. **Retro**: `Path(os.environ.get(X) or default)` at module scope is a seal-defeating idiom — resolve at call time | a writer that honors its env is still unsealed if nothing SETS that env under pytest; the floor is as load-bearing as the resolver | probe the live sink's byte-size before and after, that is the only proof the seal held.
- 2026-07-09 (~long): **Jeff-requested HALLMARK skill + audit + fixes (anti-AI-slop pass on the showcase surface).** Committed the hallmark skill (324def0) — caught that this repo's `.claude/` is BLANKET-gitignored (0 .claude tracked), so "commit it" needed a surgical `git add -f` (tracks hallmark only, not other local `.claude` state). Ran hallmark AUDIT via a **background read-only agent** (self-wrote `docs/reviews/hallmark-audit-2026-07-09.md`); **producer-verified the top findings against the canonical myself** (Producer-Owns — italic hero em :257, 11 eyebrows+10 gold-lines, centered `.section-header` :275 — all real) before bringing to the gate. Verdict 0 crit / 3 major / 7 minor / 1 info; site PASSES the 9-rule bar, reads "polished but templated." Kleiber gated → **Jeff ruled "All"**; ratified posture (Rams b48d6e2): tokens canonical, Hallmark = generator/anti-slop UNDER them. **#1 hero italic→roman SHIPPED + LIVE** (32c8de5 → gh-pages e66f5ba, byte-verified after 1 Pages-rebuild retry) — **the RDR catch of the night: `<em>` is italic by UA-DEFAULT, so removing `font-style:italic` left it italic; only the rendered computed-style read-back saw it → set explicit `font-style:normal`** (banked to memory; Kleiber-endorsed). **#2/#3 left-editorial-axis redesign BUILT to Rams's design (0450012) + STAGED** (20119fa, local, NOT deployed per Rams): section-headers+hero left, Donate the one centered exception, eyebrows 10→1 (Research), gold-line dropped on 3 bare-H2 sections; rendered-verified @320/768/1280 (left axis + header shares content left-edge teamHeaderVsGridLeftPx=0 + no h-scroll + AA unaffected); 5 bite-tested guards (`test_redesign_left_axis.py`); 242 pytest + 4 skipped + 38 Playwright. **Verify-don't-assume catch**: a bite-test restore sed was too broad (matched the `.donate-section .section-header` substring) and silently flipped donate to left — caught by checking state, not trusting the restore; fixed. **Retro**: removing a CSS declaration ≠ neutralizing the property when a UA default underlies it — assert the COMPUTED style, not the source diff (`<em>` italic) | producer-verify audit findings against the source before gating them, never relay the agent's word | a substring-broad sed reverse can corrupt a sibling rule — check state after a bite-restore | `.claude/` blanket-ignored → force-add to track a specific skill. **WAITING-ON Rams #2/#3 design verdict → Kleiber gate → Jeff veto-window → deploy.**

---

## User Preferences
- Call me **"Ace Scout"**
- Visual thinker: render side-by-side previews whenever possible, don't just describe
- Iterative designer: many rounds, walk through options one at a time
- Run background agents for parallel work while brainstorming in foreground
- Broad permissions so work flows without interruption
- When you discover patterns, conventions, or gotchas that would help future sessions, save them to your auto memory.

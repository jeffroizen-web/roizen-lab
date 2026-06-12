# Ace Scout — Conformance Self-Sweep (claims → code)

Lane B5 of the audit arc (Kleiber MSG-812f40). Method: harvest testable claims from
CLAUDE.md Quick Status + Instruction Register + doc banners + state.json, verify each
against git/code/launchctl/files, verdict with evidence.

**Date:** 2026-06-11 · **Auditor:** Ace Scout (self) · **Claims:** 18 verified, 2 honest-skips
**Verdicts:** 13 REALIZED · 1 PARTIAL · 2 DIVERGED · 2 STALE (both fixed in-sweep)

---

## DIVERGED (the gold)

| # | Claim | Reality | Evidence |
|---|-------|---------|----------|
| D1 | Session log 2026-05-19 (archived): "Cron infrastructure: tenure_readiness_cron.sh + plist (4hr cadence) + letter_writers plist (Sunday 03:00 weekly)… safe-canary pattern for Jeff to observe one cycle" | **Plists existed ONLY in scripts/ — never installed to ~/Library/LaunchAgents, never loaded, never fired.** docs/reports/ held exactly ONE report (2026-05-19 12:50, the manual initial run); a 4hr cadence would have produced ~130 by now. 23 days of silent cron-not-firing. No "cycle" was ever observable. | `launchctl list \| grep -iE "hypothesisdriven\|tenure"` → empty (pre-fix); `ls ~/Library/LaunchAgents \| grep hypoth` → empty; `ls -la docs/reports/` → 2 files dated 05-19 only |
| D2 | Session log 2026-05-19 (archived): "**12 commits** — credibility-engine infrastructure" | **10 commits**, even on the widest window (05-18 18:00 → 05-20 06:00). Off by 2 — likely counted planned units, not landed commits. | `git log --oneline --since="2026-05-18 18:00" --until="2026-05-20 06:00" \| wc -l` → 10 |

**D1 remediated in-sweep** (reversible, pre-approved class; the Jeff-canary is the
`CROSS_CM_BUS_TRIAL_ENABLED=0` env INSIDE the plist, not the load itself): both plists
copied to `~/Library/LaunchAgents/`, loaded, tenure job kickstarted once —
`docs/reports/tenure-readiness-2026-06-11.{json,md}` landed (22:19), loop closed.
`launchctl list` now shows both labels at exit-status 0. Recorded in state.json
`crons_loaded`. D2 stands as a record-accuracy lesson — archive entries stay immutable.

## STALE (prose lagging own ships — both fixed in-sweep)

| # | Claim | Reality | Evidence | Fix |
|---|-------|---------|----------|-----|
| S1 | Quick Status + state.json: "116 py green" / `tests_green: 116 python` | 128 since the B4 readback tests (commit `5db2b8e`/`5e5879c`, same day) | `python3 -m pytest -q` → `128 passed, 4 skipped` | Both updated to 128 |
| S2 | IR rule says DONE items leave the IR; two `→ DONE` rows (2026-04-16 "Call me Ace Scout", "/close + /compact") still sat in the IR | Process drift vs orchestra.md Instruction Tracking | CLAUDE.md lines 64/69 (pre-fix) | Both rows deleted |

Adjacent note (not a live claim): the archived 05-28 session-log cites banned phrases at
`compare-purple-gold.html:793/905/1141`; the 2026-06-10 SEO insert shifted them to
834/946/1182 (`grep -nE "fortunate to work with|stand on the shoulders|advances our
understanding"`). Archive is immutable history — noted here so nobody greps stale line numbers.

## PARTIAL

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| P1 | IR: "text Jeff via ntfy AND send Kleiber a Telegram when someone emails through the site" | Layer 1 code shipped but inert end-to-end: `FORMSPREE_ID_HERE` placeholder still in the form (2 hits) — Jeff signup pending as Blocking states; Layer 2 (Telegram) explicitly deferred. Claim text is honest about this; flagged PARTIAL because the *capability* is not live. | `grep -c FORMSPREE_ID_HERE compare-purple-gold.html` → 2 |

## REALIZED

| # | Claim | Evidence |
|---|-------|----------|
| R1 | All 9 session-log/Quick-Status commit SHAs exist (`224aa1e 7ed0502 936282f 8ffe075 5db2b8e 5e5879c 1c0c2f1 f29e104 6e5caa4`) | `git cat-file -t <sha>` → commit, all 9 |
| R2 | Tenure grade C; 3 banned phrases; 3 figure-pendings (q2,q3,q7) | `scripts/tenure_readiness.py` live run |
| R3 | "18 playwright passed" | `npx playwright test` → 18 passed (re-run this sweep) |
| R4 | Railway-token inventory: TRIAL_BUS_TOKEN at `bus_emit.py:70`; zero RAILWAY_TOKEN refs | `grep -n TRIAL_BUS_TOKEN scripts/bus_emit.py` → :70; repo-wide RAILWAY_TOKEN grep → 0 |
| R5 | Blocking artifacts exist: design-review + figure-candidates prototypes, archivist contract, contact-form-status | `ls` all 4 → present |
| R6 | DEPLOY.md staged with decision tree + checklist | file present, content verified 06-10 |
| R7 | capabilities.json: 6 surfaces, scanner Manifest OK | `state_scanner --cm "Ace Scout"` → OK (re-run this sweep) |
| R8 | state.json: scanner State OK | same run → OK |
| R9 | site_deployed=false: no CNAME / workflows / netlify.toml / vercel.json | `ls` all → missing (re-confirmed 06-10) |
| R10 | production/index.html stale vs working file ("2350 diff lines") | now 2379 (delta = my 06-10/11 SEO+CLS edits to the working file widened it; direction & claim hold) |
| R11 | tenure_readiness_baseline.json exists and watcher diffs against it | file present; watcher runs green |
| R12 | bus read-back live: emit_and_verify → inbox exact-match | live proof `ace-scout-research.commit-3cdb4fe054c6` verified=true (this session) |
| R13 | tests/site-qa.spec.js durable QA gate (7 tests) | `npx playwright test --list` → 7; included in the 18 |

## Honest skips

| # | Claim | Why skipped | What would verify |
|---|-------|-------------|-------------------|
| K1 | "WMF PNG-only proposal surfaced to Kleiber via tmux 20:24 EDT 2026-05-28" | Message-delivery history lives in Kleiber's ack ledger, not my repo; my session log is the only local artifact (self-referential) | `tmux-ack-audit` on Kleiber's ledger for the 05-28 20:24 send |
| K2 | "Both grade-C gates are in Kleiber's current Jeff batch, WMF Tier-1 (MSG-78cc34)" | Kleiber-side queue state; unverifiable from my repo | Kleiber confirms batch contents (he asserted it in MSG-78cc34/bcbbb8) |

## Spot-check vectors for independent gating

1. `launchctl list | grep hypothesisdriven` → 2 labels, exit 0 — then `ls docs/reports/` → a `tenure-readiness-2026-06-11.*` pair stamped 22:19 (D1 remediation proof).
2. `python3 -m pytest -q` → 128 passed / 4 skipped (S1 fix; Quick Status + state.json now agree).
3. `git log --oneline --since="2026-05-18 18:00" --until="2026-05-20 06:00" | wc -l` → 10, vs the archived "12 commits" (D2).
4. `grep -n "→ DONE" CLAUDE.md` → 0 rows in the IR (S2 fix).

# Roizen Lab (Ace Scout) Vision-Battery Review — 2026-07-03

**Reviewer:** Fable 5 planning lens (Kleiber vision program). READ-ONLY on Ace Scout code; report-only. Ace Scout the CM executes any repair through its own gated builds (Producer-Owns). The only file this pass writes is this report.

**Vision under review (three tiers of statement, all in-repo):**
1. **North star** (`docs/platonic-vision.md`, Ace Scout): *"A site that makes a tenure committee member think 'this person is serious, productive, and collaborative' within 10 seconds… The site IS the tenure argument — not a brochure, an evidence map."* Four audiences: dept chair, collaborator, journalist, grant reviewer.
2. **The identity bar** (`docs/score_reference.md`, cited in tenx §Scope): *"not a departmental template page — a carefully crafted statement of scientific identity"* conveying *engagement, trust, and a cool factor.*
3. **The startup-studio frame** (`.claude/rules/web-quality-standards.md`): the lab site is a **front-door surface** that gets the full showcase treatment; the 9 web-quality rules are the bar; a11y/responsive/perf failures are BLOCK-class.

**Frame constraints honored:** tenure clock (site live+polished by ~Aug 2026, letters ~Sep 2026 — the forcing function); no-build-system constraint (plain HTML/CSS/JS, `compare-purple-gold.html` is render-authoritative); remote push is Jeff-gated and bundles with the hosting go-live (I do not re-litigate that gate); anti-fabrication line (no synthetic science figures/data). This pass BUILDS ON (does not repeat) `tenx-and-loops-2026-07-02.md` and `web-quality-self-assessment-2026-07-01.md`; findings there are honored by reference and sequenced, not re-argued.

**Method:** file:line-cited pass over the canonical HTML, the two launchd loops + their scripts, the publications-feed consumer, the tenure-readiness watcher, and the test suites. Suites RUN this pass (both hermetic — see health snapshot). Claims not verified are marked as such.

**Sections:** 1. Codebase-vs-vision map · 2. Planning questions (options developed) · 3. Repair list (additive to tenx) · 4. The plan (sequenced /pipe4 increments) · 5. Top-3 + verdict.

---

**Health snapshot (verified this pass, my own runs):**
- `python3 -m pytest -q` → **153 passed, 4 skipped** (0.27s). The 4 skips are NET-gated (live-scrape / live-site tests), correct to skip offline.
- `npx playwright test` → **30 passed** (16.5s). Hermetic: serves `compare-purple-gold.html` on `localhost:8766/:8766`, and the contact-form spec `page.route`-mocks Formspree + ntfy (`tests/contact-form.spec.js:92-96,123-131`) — **zero external posts**, safe to run. (Note: the CLAUDE.md "18 site-qa" count is now stale — 20 site-qa + 10 contact-form = 30 Playwright.)

This is not the Runner case (dormant) or the Tempo case (a flag-flip from its differentiator). Ace Scout's codebase is **near-complete, well-tested, and honest** — the vision gap is almost entirely **reach and product-shape**, not craft or correctness: the site is polished but reaches zero users (no hosting), and its two live data pipelines (publications feed, letter-writer scrape) are built but under-connected. The autonomous technical ceiling really is close, as the platonic-vision doc claims (~80% built).

## 1. CODEBASE-VS-VISION MAP

Per-subsystem, against the platonic-vision "fully realized state" + the web-quality front-door bar.

| Subsystem | What exists (verified) | Verdict vs vision |
|---|---|---|
| **The canonical site** (`compare-purple-gold.html`, 88.9KB / ~1325 lines, all-inline CSS/JS) | 13 sections, 1 `<h1>`, dual institution header (CHOP · Penn), 7 Big Questions, team/collaborators/peers/mentors, publications, contact form, JSON-LD, full meta/OG, favicon. De-marketed to Jeff's voice (e086df8). | **EXISTS-AND-SOLID.** Content-complete and launch-ready. This is the product; everything else serves it. |
| **Design-token / craft system** | `design-tokens.css` (3.5KB): modular type scale xs..5xl, 4px-base spacing, radius/shadow/motion tokens; applied via PR-1 (d607729, 287 property-scoped replacements). WebP `<picture>` on all content rasters + hero `image-set` (PR-2, 8678346, hero −74%). Self-hosted fonts + LCP preload (57dbac0). WCAG-AA contrast fixed (6ef972c). Mobile nav 44px tap targets (74571c3). | **EXISTS-AND-SOLID.** Kleiber WEB-QUALITY lens = PASS-WITH-FLAG, both flags closed. Craft is at bar. Residual: type/spacing tokens are `<link>`ed externally while consumers are inline (O-4, cosmetic split). |
| **Hosting / go-live** | `docs/DEPLOY.md` Path A/B decision tree, exact GH-Pages DNS records staged, one-step deploy documented. `site_deployed: false` (`docs/state.json:15`). | **MISSING — the one true gate.** The site reaches zero people. hypothesisdriven.org is registered (Google Cloud DNS) but points nowhere. Jeff-gated (DNS paste / "soft-launch go"). Dominates all other leverage. |
| **Publications (living CV)** | Consumer `scripts/publications_feed.py` (189 lines, forgiving parser, staleness banner ≥14d, arc-grouping). Archivist feed **IS LIVE**: `~/orchestra-data/archivist/publications.json` = **29 pubs, `data_as_of` 2026-06-29**, refreshed weekly by `com.archivist.publications-weekly` (loaded, verified `launchctl list`). | **EXISTS-BUT-DISCONNECTED.** The feed flows and the parser exists, but **the live HTML publications section is hand-coded static** ("Highlights from 27 publications", `:974`) — the consumer is NOT wired in (`grep publications_feed compare-purple-gold.html` = 0). A fresh 29-pub feed sits unused next to a stale "27" literal. See R1. |
| **Big Questions evidence map** | 7 questions rendered; 4 with figures, **3 "Figure pending" placeholders** (q2/q3/q7 — WMF/EMF conversion dead-ended after 4 attempts, PNG-only decision pending Jeff). Q→Papers cross-linking and research-arc grouping are in the platonic-vision "can-do-now" list but NOT built. | **EXISTS-BUT-DRIFTED.** The "spine" the vision names (Q → approach → result → paper → next-Q trajectory) is not wired; questions are a static list, not a navigable evidence map. 3 visible placeholders on the section a committee reads first. |
| **Contact / recruiting funnel** | Layer-1: Formspree + ntfy, 5 labeled fields, honeypot spam trap, live-region status (`tests/contact-form.spec.js`, 10 green). | **HALF-BUILT (as designed).** Layer-1 done; Layer-2 (Telegram→Kleiber triage + applicant auto-confirmation) deferred to Pilot Railway endpoint + Jeff deploy. A form, not yet a funnel. |
| **Loop A — letter-writer refresh** (`letter_writers_refresh` → `letter_writer_scrape` → `wire_letter_writers`, daily 03:00) | Scrapes peer "recent focus" → wires into HTML. **L1 PubMed + L2 ORCID ARE wired** (`letter_writer_scrape.py:318-330` `probe_with_fallback` fires `probe_orcid` when L1 confidence ≤0.6 or <5 PMIDs). L3 WebFetch stubbed. Idempotent sentinel strip+inject (byte-stable since 6/18). | **EXISTS-AND-SOLID** (tenx's "L2 stubbed" was over-pessimistic — L2 ORCID is live; only L3 is a stub). Bottleneck is now traceability, not the missing stage. |
| **Loop B — tenure-readiness watcher** (`tenure_readiness.py`, daily) | Pure evaluator: 4-audience rubric grade vs baseline. **Grade is now B** (`docs/reports/tenure-readiness-2026-07-03.md`) — up from the C in state.json. Only WARN left is the 3 figure-pendings. | **EXISTS-AND-SOLID as a monitor**, but two defects: unbounded git accumulation (48 dated report pairs and counting, O-1) and a manual baseline whose staleness turns intentional changes into permanent "regressions" (O-2). |
| **Render-from-config (product-shape)** | `content/site-content.json` extracted (a3a91cc) + `tests/test_content_contract.py` drift guard. HTML is still render-authoritative; the config→template FLIP is documented as the next increment (`docs/specs/content-contract.md:50`). | **MISSING (deliberately, Jeff-gated).** The reusable "any-PI lab-site generator" — the biggest product-market leap — is scaffolded but not built. Crosses the no-build-system constraint + SEO risk → Jeff's call. |
| **Showcase motion / WebGL (cool factor)** | None. `prefers-reduced-motion` honored; tasteful 0.2s transitions. No scroll-reveal, no hero motion, no bespoke visual. | **MISSING (Jeff/Rams-gated).** Rule 4 PASSES but the front-door *showcase* bar is unmet. PR-3 held for design direction — bespoke visual identity is a taste call. |

**Drift check:** no dangerous drift (code silently contradicting vision). The `docs/state.json` `site_tenure_grade: "C"` (`:8`) is **stale** — the live watcher reports **B** as of 2026-07-03; state.json's `data_as_of: 2026-06-10` predates the WCAG/prose/tap-target fixes that lifted it. Publish-fix noted in R6. The genuine gap is the inverse of Tempo's: there, a done engine sits behind an OFF flag; here, a done site sits behind an unset DNS record, and two done pipelines sit behind an unwired `<script>` include and an unsigned contract.

---

## 2. THE PLANNING QUESTIONS (options developed, not just posed)

### Q1 — What actually unblocks go-live, and can the orchestra shrink Jeff's step to one action?

The site reaches zero users until hosting. This has been "Jeff-gated" for weeks, but the anti-babysitting rule says: make Jeff's attention a single irreversible-approval, not a research task. Right now the ask bundles a DNS decision, a registrar-GUI action, and a push-approval into one fuzzy "hosting answer."

| Option | Shape | Cost/risk |
|---|---|---|
| **1A (recommended): pre-stage EVERYTHING so Jeff's step is one binary.** Promote `compare-purple-gold.html` → root `index.html` on a branch, add the `CNAME`, stage the Pages-enable, and hand Jeff exactly two buttons: "soft-launch now on github.io" (I push + enable Pages, live while DNS propagates) OR "paste these 4 A-records + CNAME at the registrar." All reconciliation (asset paths already root-relative — DEPLOY.md Path A) is done in advance. | ~2h of pre-staging, all reversible/local until his go | Almost none — it's the DEPLOY.md Path A work moved BEFORE the ask instead of after |
| **1B: keep waiting for the "hosting answer" as-is.** | Zero work | The ask stays fuzzy; the tenure clock (Aug 2026 live) burns while a 1-line DNS decision sits. This is the status quo that's already held for weeks |
| **1C: soft-launch on github.io NOW under the standing autonomy, treat DNS as a later cutover.** | Fastest path to a reachable URL | Crosses Jeff's explicit "no remote push without Jeff" gate on his PUBLIC repo — NOT autonomous; must be offered, not taken |

**Recommendation: 1A.** The deploy is mechanical and documented; the only real Jeff atoms are (a) approve the push to his public repo and (b) the registrar GUI. Pre-stage both so the surfacing is "here are your two buttons," not "what do you want to do about hosting." This is the single highest-leverage planning move in the whole battery.

### Q2 — Wire the live publications feed in, or keep waiting on the Archivist counter-signature?

The Archivist feed is **already flowing** (29 pubs, weekly cron loaded, `data_as_of` 2026-06-29) and the consumer parser exists and is tested — but the contract is still `DRAFT — awaiting Archivist counter-signature` (`docs/contracts/archivist-publications.md:5`), so the site shows a hand-typed "27 publications" static list. The vision names a *living CV* as credibility's core signal; a committee's first question is productivity.

| Option | Shape | Honest assessment |
|---|---|---|
| **2A (recommended): get the counter-sig THIS week (Kleiber-dispatched), then wire the feed behind a staleness-guard.** The parser already degrades loudly (≥14d banner) and falls back to the static list on a missing/invalid feed. Wire it as a build-time render (SEO-safe, no client JS) so the served HTML carries the fresh list + `data_as_of` stamp. | The blocker is a one-message cross-CM ask, not a build. The infra is done on both sides; only the Producer-Owns handshake is open. This is a stale-blocker, exactly the kind the escalation policy says the orchestra resolves without Jeff |
| **2B: keep the static list until launch, wire the feed post-launch.** | Zero coordination now | Ships the tenure front-door with a stale "27" while a fresh 29-pub feed sits unused — undersells productivity on the surface built to prove it |
| **2C: wire the feed client-side now.** | Fastest to "live data" | Harms SEO (crawlers see an empty list), and the no-build constraint means no hydration step — the content-contract spec already rejected client-side for exactly this reason (`:50`) |

**Recommendation: 2A.** Kleiber dispatches the counter-sig ask to Archivist; on sign, Ace Scout wires the feed via a build-time render with the staleness banner. This converts a done-but-dark pipeline into the living-CV the vision names.

### Q3 — The 3 "Figure pending" placeholders (q2/q3/q7): PNG-only close, or hold for conversions?

The WMF/EMF vector charts dead-ended after 4 conversion attempts (IR 2026-05-20). The pending placeholders are the one WARN keeping the tenure grade at B (would flip toward A- on close), and they're 3 visible holes on the section a committee reads first. Note `extracted-figures/` already has per-question PNG dirs (Q2-hepatic-enzyme, Q3-cyp2r1-variants, Q7-biomarker) — the raster figures exist.

| Option | Shape | Tradeoff |
|---|---|---|
| **3A (recommended): PNG-only close using the existing `extracted-figures/Q{2,3,7}` rasters, Jeff blessing the figure-to-question pairing.** Jeff already flagged figure-to-question matching may be wrong (CLAUDE.md Big Questions "needs review") — so this is one Jeff decision: "these 3 PNGs are the right figures for these 3 questions, ship them." | Closes the last WARN, lifts grade toward A-, removes the front-door holes, zero conversion work | Needs Jeff's per-figure pairing confirm (anti-fabrication — I won't guess which figure belongs to which question) |
| **3B: keep holding for WMF→vector conversion.** | Preserves crisp vector charts | 4 attempts failed; the tenure clock won't wait; "Figure pending" on a committee-facing section is worse than a good raster |
| **3C: AI-generated conceptual placeholders, clearly labeled illustrative.** | Fills the holes with on-brand visuals | Risky on a science-claims section; the launch-content pass already held the anti-fabrication line here — a labeled illustration still invites "is this your data?" |

**Recommendation: 3A.** One Jeff decision (bless the 3 pairings) closes the grade WARN and the front-door holes with figures that already exist on disk. Batch it with the Q1 hosting ask.

### Q4 — Render-from-config: build the reusable generator now, or after launch?

`content/site-content.json` + the drift-guard exist; flipping authority to config→template turns "Jeff's site" into a shippable any-PI lab-site generator — the clearest personal-only→product leap, and a real market (thousands of labs have departmental-template pages). But it crosses the no-build-system constraint + SEO risk.

| Option | Shape | Tradeoff |
|---|---|---|
| **4A (recommended): defer the flip until AFTER go-live + the feed wire, then build it as a /pipe4 with a golden byte-equivalence gate.** The generator's acceptance test is "reproduces the current live site byte-for-byte, then a second fixture lab's config yields a valid distinct site with zero HTML hand-edits." | Keeps the launch on the proven static file (zero launch risk); builds the product-shape leap on top of a shipped, validated baseline | The product-market upside waits ~weeks — acceptable; the tenure case needs the LIVE site first, not the generator |
| **4B: build the generator now, launch FROM it.** | One coherent product from day one | Bets the tenure-critical launch on an unproven build step + SEO flip; violates smallest-first — the launch shouldn't ride a new architecture |
| **4C: never build it, keep it a bespoke site.** | Zero cost | Forgoes the one clear "does it have a market?" answer in the portfolio; the scaffolding (config + guard) is already sunk cost pointing at the product |

**Recommendation: 4A.** Ship the site, wire the feed, THEN build the generator as a gated /pipe4 with the byte-equivalence golden. The build-time render from Q2 is the natural first step toward it (same generator spine).

---

## 3. REPAIR LIST (additive — tenx/self-assessment items honored by reference, not repeated)

**Already on the books (tenx §2 + web-quality self-assessment; the plan sequences them, this list doesn't re-argue):** O-3 per-test HTML re-read → conftest fixture · O-4 split-brain tokens (external `<link>` vs inline consumers) · O-5 clean-attribution dance → `scripts/commit_my_html_edits.sh` · showcase motion (10X-4, Jeff/Rams) · living-publications 10X-3 (now sharpened into R1 below) · Layer-2 contact funnel (10X-7).

**New / sharpened findings from this pass (worst-first, each verified in code):**

**R1 — HIGH: the live Archivist publications feed is built, flowing, and NOT wired to the site.** `scripts/publications_feed.py` (a tested, forgiving consumer with a ≥14d staleness banner and static-list fallback) has ZERO references in the canonical HTML (`grep -c publications_feed compare-purple-gold.html` = 0). Meanwhile the feed is LIVE — `~/orchestra-data/archivist/publications.json` carries **29 publications, `data_as_of` 2026-06-29**, refreshed weekly by `com.archivist.publications-weekly` (loaded, verified). The site's Publications section is a hand-typed static list headed **"Highlights from 27 publications"** (`compare-purple-gold.html:974`) — a stale literal next to a fresh feed. This is the vision's "living CV / credibility's core signal" sitting dark. The only true blocker is the DRAFT contract (`docs/contracts/archivist-publications.md:5`, awaiting Archivist counter-sig) — a one-message cross-CM handshake, not a build. **Fix: get the counter-sig (Q2), then wire the feed via a build-time render with the staleness banner + `data_as_of` stamp.**

**R2 — MED (correctness/observability): both launchd loops mis-signal outcome via process exit code.** `scripts/tenure_readiness.py:219` (`return 1 if regressions else 0`) is propagated to launchd by `scripts/tenure_readiness_cron.sh:88` (`exit "$EXIT_CODE"`); `scripts/letter_writers_refresh.py:114` (`return 0 if not regressions else 1`) does the same. So "I did my job and detected drift" exits identically to "the job crashed" — the `exit-code-outcome-mismatch` class in `failure-ledger-contract.md`. Compounded by R3: a stale baseline makes every run report the intentional change as a regression → exit 1 → alert fatigue, indefinitely. **Fix: reserve nonzero for genuine execution failure (scrape/IO/parse); carry "regression detected" in the emitted event / a distinct sentinel field, never the process exit.** (Both loops already emit rich bus events — the exit code is redundant signal doing harm.)

**R3 — MED: the tenure-readiness baseline is a manual, stale artifact that decays the watcher to noise.** `docs/tenure_readiness_baseline.json` was last written **2026-05-19** (verified mtime) and still records `grade: C` with `figure_pending_ids: [q2,q3,q7]`, while the live site now grades **B**. Every intentional improvement since 5/19 (WCAG, prose, tap-targets, tokens) is a "regression since baseline" until someone re-runs `--baseline`. The watcher's whole value — catch UNintended drift — is drowned by un-acknowledged intended drift. **Fix: auto-advance the baseline on a clean gate pass, OR add an "acknowledge this drift" step; and re-baseline now to B so the signal is live again.** (This is the tenx Loop-B bottleneck, verified concrete here.)

**R4 — MED (hygiene, unbounded): dated tenure reports accumulate in the repo forever.** `docs/reports/` holds **48 `tenure-readiness-YYYY-MM-DD.{json,md}` files** today (verified count) and grows by 2/day (`tenure_readiness_cron.sh:26-27` writes a fresh dated pair each run; several are uncommitted in the working tree right now — `git status` shows 07-02/07-03 pairs). At ~730 files/year of near-identical drift this bloats every clone and diff. **Fix: rotate (keep last N, e.g. 14) or `.gitignore` the dated reports and keep a rolling `tenure-readiness-latest.{json,md}` + the baseline.** Class: dead-scaffolding accumulation (tenx O-1, verified).

**R5 — LOW (loud-degradation): the letter-writer low-confidence sentinel carries a label but not a machine reason.** `letter_writer_scrape.py` computes a confidence score + human notes (`compute_confidence`, `:148-157`) and L1→L2-ORCID fallback fires correctly (`probe_with_fallback:318-330`), but when a name stays low-confidence the wired HTML gets a generic "verifying field-of-interest" with no recorded machine reason (`no-match` vs `ambiguous` vs `network`). Under `loud-degradation-contract.md` this is a borderline silent-dark: dark-with-a-label but not dark-with-a-reason. Low severity (the label is honest and the value is peer-focus text, not a decision input), but the reason field would make the L3 stub's future payoff measurable. **Fix (defer): thread the `confidence_notes` reason into the wired sentinel + a per-person scrape trace line.**

**R6 — LOW (stale surface): `docs/state.json` publishes a stale grade + test count.** `site_tenure_grade.value: "C"` (`:8`, `data_as_of: 2026-06-10`) vs the live watcher's **B**; `tests_green` reads "128 python … 18 playwright" (`:47`) vs the actual **153 py + 30 pw** this pass. Per CM-Discovered-State-Must-Publish, the queryable state is a surface other CMs read. **Fix: refresh state.json at the next /ccc (grade B, 153+30 green, feed-live note).** Trivial; grouped with R3's re-baseline.

**What I looked for and did NOT find (clean bills, stated so the plan can trust them):** no dead `href="#"` (donate went live e086df8; site-qa guards it); no missing alt (15/15, watcher + site-qa); no banned Claude-voice phrases (watcher clean); no lorem; WCAG-AA contrast holds (test_contrast.py, 6ef972c); mobile nav tap-targets ≥44px (74571c3, site-qa #17); Playwright suite is hermetic (mocked Formspree/ntfy — no live posts); the L2 ORCID stage tenx flagged as "stubbed" is in fact WIRED (`:330`) — only L3 WebFetch is a genuine stub, correctly so (CLI 403s). The idempotent `wire_letter_writers` byte-stability fix (6/18) holds.

---

## 4. THE PLAN — sequenced increments (smallest-first; each a gated build)

**Standing constraints baked in:** remote push is Jeff-gated and bundles with hosting (Increments 1-2 are the only Jeff-GO gates; the rest are autonomous local builds landing behind that same gate); no-build-system means "build-time render" = a small Python static generator, never client-side hydration (SEO); anti-fabrication holds on all figure/data work; every build passes the pytest + site-qa suites + Kleiber's WEB-QUALITY lens where it touches the rendered surface.

**★ JEFF-DECISION GATES (answerable in ONE batch — the whole point of the anti-babysitting frame):**
- **D1 (Q1):** go-live — "soft-launch on github.io now" OR "here are the 4 A-records + CNAME to paste." Everything pre-staged (Inc 1). Rec: pre-stage both, offer as two buttons.
- **D2 (Q3):** bless the 3 figure-to-question pairings (q2/q3/q7 PNGs already on disk) so the placeholders close. Rec: PNG-only close.
- **D3 (Q4/PR-3):** render-from-config timing (post-launch) + WebGL showcase direction (Jeff/Rams). Rec: defer both to after launch+feed.

| # | Increment | Goal + acceptance criteria | Size | Gate |
|---|---|---|---|---|
| **0** | **Loop hygiene: exit-code semantics (R2) + baseline lifecycle (R3) + report rotation (R4) + state.json refresh (R6)** | AC: both loops exit 0 on "detected drift" and nonzero ONLY on genuine execution failure (a forced-regression test proves the exit is 0 while the bus event carries the regression); baseline re-written to B with an auto-advance-on-clean-pass path (or an ack step); `docs/reports/` rotates to last-14 or gitignored + a rolling `-latest`; state.json publishes grade B + 153/30 green + feed-live | ~half day | pytest + a new loop-exit test; no push needed (scripts + local) |
| **1** | **★ Pre-stage go-live (Q1/1A)** | Promote `compare-purple-gold.html` → root `index.html` on a branch, add `CNAME` (hypothesisdriven.org), verify zero broken assets + zero console errors in a served preview, stage the Pages-enable. AC: a local served copy of the promoted `index.html` renders byte-equivalent to the working file (root-relative paths already correct — DEPLOY.md Path A); the two Jeff buttons are documented and one-action each | ~2h | **Jeff GO (D1)** for the actual push/DNS; everything up to the push is autonomous+reversible |
| **2** | **★ Close the 3 figure placeholders (Q3/D2)** | On Jeff's pairing blessing, wire the existing `extracted-figures/Q{2,3,7}` PNGs into q2/q3/q7 with real alt text. AC: watcher `figure_pending_count` → 0, grade flips toward A-; site-qa still green; each figure has non-empty alt + explicit width/height (CLS) | ~1h | **Jeff GO (D2)**; then autonomous wire; rides the launch push |
| **3** | **Wire the live publications feed (R1 / Q2 / 10X-3)** | On Archivist counter-sig (Kleiber-dispatched), render Publications from `publications_feed.py` at build-time into the served HTML with a visible `data_as_of` stamp + the ≥14d staleness banner + static-list fallback. AC: served HTML carries the fresh 29-pub list (not the "27" literal); a stale-feed fixture renders the loud banner not a silent snapshot; SEO content is in the served markup; site-qa + a new publications-render test green | 1-2 days | Archivist counter-sig (cross-CM); Kleiber WEB-QUALITY lens; rides launch |
| **4** | **Q→Papers evidence-map cross-linking + research-arc grouping** (the platonic-vision "spine", can-do-now items 1+2) | AC: each Big Question links DOWN to its arc-grouped publications and FORWARD to its next question; a reviewer can trace question→paper→next-question; keyboard-accessible; no new dead links (watcher clean) | 2-3 days | site-qa + watcher; autonomous |
| **5** | **Self-measuring CWV gate at deploy (10X-6)** | Once hosted: wire a headless Lighthouse run into a post-deploy check that records LCP/CLS/INP, fails below budget (LCP<2.5s/CLS<0.1/INP<200ms), and reads back the −74% hero WebP claim against the served asset (the DEPLOY.md §Post-deploy checklist becomes code) | ~1 day | autonomous once hosted; closes the WEB-QUALITY flag-2 |
| **6** | **Render-from-config generator (Q4/10X-2)** — the product-shape leap | AC: `build.py content/site-content.json` reproduces the live site byte-for-byte (golden gate); a second fixture lab's config yields a valid distinct site with ZERO HTML hand-edits; SEO/meta/JSON-LD preserved in output; site-qa + content-contract green on the generated HTML | 1-2 wks | **/pipe4** with the byte-equivalence golden as the judge floor + web-quality lens; **D3 timing** |
| **7** | **Showcase surface (PR-3): WebGL molecular hero + scroll-reveal Big Questions (10X-4)** | AC: 60fps (`transform`/`opacity` only), `prefers-reduced-motion` → static fallback, LCP stays <2.5s, JS budget <150KB gz, no CLS; front-door "cool factor" the vision names | 1-2 wks | **/pipe4** web-quality judge; **D3 direction (Jeff/Rams)** |
| **8** | **Contact funnel Layer-2 (10X-7)** | AC: structured intake → read-back-verified delivery to Jeff (Producer-Read-Back) + Telegram-to-Kleiber triage + applicant auto-confirmation; spam-guarded | ~1 wk | needs Pilot Railway endpoint + Jeff deploy; cross-CM |

**Explicitly NOT in the plan:** editing `production/index.html` or root `index.html` (both stale drift-sources — collapse to ONE canonical at launch per DEPLOY.md); AI-generated science figures (anti-fabrication); client-side rendering (SEO); any multi-tenant/auth/payment scaffolding (the generator ships a static site per config, not a hosted SaaS — a template product, not a platform).

---

## 5. TOP-3 + VERDICT

**TOP-3 highest-leverage moves:**

1. **Shrink go-live to two Jeff buttons and surface it (Inc 0+1 → D1).** The site is polished, tested, B-grade, and reaches ZERO people; every craft gain is worth 0× until it ships, and the tenure clock (live by Aug 2026, letters Sep) is the hard forcing function. The deploy is fully mechanical (DEPLOY.md Path A, root-relative paths already correct). Do the pre-staging FIRST so Jeff's ask is "soft-launch now OR paste these DNS records," not a research question — that's the anti-babysitting rule applied to the single biggest blocker in the whole battery.

2. **Wire the live 29-pub Archivist feed in (R1 → D-none, just a cross-CM counter-sig).** The vision names a living CV as credibility's core signal; the feed is FLOWING (weekly cron, `data_as_of` 2026-06-29) and the consumer is built and tested — but the site shows a hand-typed "27 publications" because a DRAFT contract awaits an Archivist counter-signature. That is a one-message handshake the orchestra resolves without Jeff, not a build. A done-but-dark pipeline is the highest-value quick win: it turns the tenure front-door's productivity signal from a stale literal into a self-freshening list.

3. **Fix the two loops' exit-code semantics + re-baseline the watcher (R2+R3+R4).** Both launchd loops exit 1 when they successfully detect drift (`tenure_readiness_cron.sh:88`, `letter_writers_refresh.py:114`), which launchd reads as a crash, and the watcher's baseline is 6 weeks stale (grade C vs live B) so every intentional fix reads as a regression — the monitor has decayed to noise exactly when the site is about to launch. Small, autonomous, and it restores trust in the two signals that are supposed to prove the site is launch-ready.

**VERDICT:** Roizen Lab is the portfolio's clearest case of **a finished, honest product blocked on reach, not craft.** The autonomous technical ceiling really is close (~80%, as the platonic-vision doc claims): the canonical site is content-complete, WEB-QUALITY-lens PASS, 153+30 tests green, B-grade and climbing. The vision-to-code fidelity is HIGH where code exists — the gaps are the *evidence-map* spine (Q→Papers cross-linking, unbuilt) and the *living* signals (publications feed and letter-writer trace, built-but-under-connected), plus the two Jeff-gated leaps (render-from-config product, WebGL showcase). None of that is a rescue; the plan is a sequencing discipline whose first three increments are all small: **fix the loops, pre-stage the launch, wire the feed** — three moves that convert a polished-but-invisible site into a live, self-freshening tenure argument. Recommended first build: **Increment 0 (loop hygiene)** — no push, no Jeff, restores the launch-readiness signal, and clears the deck for the go-live surface.

---

*All findings REPORT-ONLY. Any that becomes a build routes the normal gate (Kleiber's WEB-QUALITY lens + pytest/site-qa; Jeff GO on push/DNS; cross-CM handshake on the Archivist feed). Health verified this pass: 153 pytest + 30 Playwright green, my own runs.*

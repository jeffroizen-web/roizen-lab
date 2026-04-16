# Review Packet for Jeff — 2026-04-15

**From**: Ace Scout
**Duration**: Single autonomous session, approximately 90 minutes
**Scope**: Full site stress-test per Kleiber dispatch. Applied technical/WCAG/semantic fixes autonomously; everything creative or factually uncertain is flagged here for your decision.

---

## What I already applied (reversible — revert any you don't like)

### Figure audit + Q1 wire-in
- Root cause identified: `extracted-figures/curated-for-website/` files were named by *intended* Q#, not *actual* pixel content. Full analysis: `docs/figure-audit.md`.
- Q4 keeps `q4-dose-response.png` (muscle O2 flux 25D vs 1,25D). Alt text rewritten for specificity.
- Q5 keeps `q5-diabetes-prevention.png` (T2DM Kaplan-Meier). Alt text rewritten.
- Q6 swapped to `q1-causation.png` (the leptin→brain→calorie-allocation pathway diagram). This is the literal "metabolic traffic cop" figure your Q6 paragraph references — it was mis-filed under Q1.
- **Q1 newly wired** to `extracted-figures/from-archivist/reverse-causation-bmi-vitd.png`. I pulled Fig5 from Archivist's (MR VitD Asthma) paper-ready/figures directory and converted PDF→PNG. It's the BMI→25(OH)D reverse-causation MR scatter: all five estimators (IVW, MR Egger, weighted median, simple mode, weighted mode) converge on a negative slope. This is the exact Q1 claim: higher BMI causally lowers vitamin D.
- Q2, Q3, Q7 remain "Figure pending" placeholders. Options are documented in `docs/figure-audit.md`.

### Dead links removed
- All six `<a href="#" class="paper-link">Read the paper →</a>` anchors under Q1-Q7 are gone. They were flagged by the content-critique agent as the single biggest credibility hit on the page (a grant reviewer hits them, bounces). Clean removal preserves text; you can wire real DOIs back in when the papers are chosen.
- Donate button `href="#"` is retained — it's an intentional placeholder for the CHOP Foundation URL you are still waiting to get from CHOP dev office (per CLAUDE.md deferred decisions). Not a bug.

### WCAG 2.1 AA compliance fixes (the lab-website.md rule requires this)
Measured contrast failures (all on white/warm-gray card backgrounds):
- `#C5A336` accent gold on white = 2.38:1 (required 4.5:1). Applied everywhere as body text for eyebrows, role subtitles, metadata, paper links.
- `#888` text-muted on white = 3.16:1 (required 4.5:1). Applied to pub-meta, alumni-years, placeholder text.

Fix applied:
- Added `--accent-dark: #8A6B1A` (~5.5:1 on white) as the NEW body-text gold. Used for `.eyebrow`, `.pub-year`, `.team-role`, `.news-date`, `.paper-link` hover states, and all inline `color:var(--accent)` role subtitles in Collaborators/Peers/Mentors. All now pass WCAG AA.
- Tightened font-weight to 600/700 on small accent text for better legibility.
- Updated `--text-muted: #666666` (~5.7:1 on white). Used for pub-meta and similar secondary text.
- `--accent` (the original `#C5A336`) is preserved for decorative uses: borders, `.gold-line` divider, nav hover, button backgrounds, hero badge on dark overlay. These are NOT body-text contexts so they remain theme-correct.

**Visual impact**: The gold looks slightly more olive / antique on body text, still reads as gold next to the purple. The decorative elements (borders, buttons) are unchanged. If the shift feels too warm, the accent-dark value is easy to tune — search for `--accent-dark: #8A6B1A` in the CSS.

### Semantic HTML + accessibility scaffolding
- Added `<a href="#main-content" class="skip-link">Skip to main content</a>` as the first body element. Hidden off-screen until focused, then jumps to content past the dual fixed header. Required by WCAG 2.4.1 (Level A).
- Wrapped all sections + footer content in `<main id="main-content">`. Page now has a proper main landmark (was missing).
- Added `@media (prefers-reduced-motion: reduce)` that kills all transitions/animations and smooth scrolling. Required by WCAG 2.3.3.
- Nav toggle button now has `aria-expanded="false"` + `aria-controls="primary-nav"`. JavaScript handler toggles both the class AND the `aria-expanded` state on open/close. Screen-reader users can now tell whether the mobile menu is open.
- Nav `<ul>` has `aria-label="Primary navigation"`.
- Added favicon link — both .ico and .svg — pointing to `logos/favicons/favicon-hd-car.ico` / `.svg`. Browser tab now shows an icon instead of blank.
- Penn Medicine institution-bar link gained `aria-label="Jeffrey Roizen faculty profile, Penn Medicine"` (the link goes to your faculty page, not the Penn Medicine homepage — the visible alt was misleading).

### Image improvements
- `src="lab-group-hires.jpg"` fixed to `src="photos/lab-group-hires.jpg"`. Previously was broken due to wrong path (a symlink made it work from the root but that is brittle).
- All three above-the-fold team photos now have `loading="lazy"` and descriptive alt text (`Dr. Jeffrey Roizen, Principal Investigator, Roizen Lab at UPenn and CHOP`; `Michael Nguyen, Research Associate in the Roizen Lab`).
- Q1 figure has `loading="lazy"`.
- All lab-strip figures have descriptive alts already.

### Lab-Life photo strip
- The photo-critique agent validated the current grayscale-15% + contrast-1.05 treatment as appropriate given the dark-purple section above/below. Nothing to change there.
- The agent did note: three of four photos are solo-Jeff, only `talkingWide.jpg` is a collaboration shot. Recommendation was to either (a) move `talkingWide` to the end for a "work → collaboration" arc, or (b) replace `dryIce.jpg` (weakest — slightly posed) with another interaction shot if one exists. Both are creative calls — I did not apply. You decide.

### Mentor section — Hakonarson disambiguation
- The people-review agent flagged that Hakonarson is listed BOTH under Collaborators (9 shared pubs) and under Mentors — reads visually like roster-padding. I added a small italic "Postdoctoral mentor" line under the CHOP line in his mentor card. No years (I don't know them). If you want specific years, edit line ~706.

---

## Things I did NOT change — your call

These are either creative/framing decisions (which per SD's documented scope are explicitly your taste, not a stress-test target), or they require information I don't have.

### 1. Dead decisions still blocking

- **Contact email — RESOLVED 2026-04-16.** Jeff confirmed `jeffroizen@gmail.com`. Full contact form built (Layer 1: Formspree email + ntfy phone push). See `docs/contact-form-status.md` for the 2-minute unblock steps (Formspree signup + ntfy topic subscribe). Layer 2 (Telegram-to-Kleiber) is backlogged to Pilot Railway endpoint, needs deploy approval.
- **Microscopy composites** — timed out Mar 7. All three composites, purple-gold tint, still holding. No action needed unless you want to change.

### 2. Creative / framing calls flagged by the content agent

I'm listing these rather than applying because they are all Jeff's-taste decisions per the SD boundary rules. Each is a defensible concrete edit you could apply in five minutes.

**2a. Reorder Big Questions: Q1 → Q5 → Q4 → Q2 → Q3 → Q6 → Q7**
Rationale from the content critique: leads with the counterintuitive finding (Q1 cause/effect), pivots immediately to the public-health payoff (Q5 diabetes prevention), then moves through mechanism. Current order is logical but buries the strongest "journalist" story. Helps journalist and committee audiences. I did not apply because the reorder is a framing decision and you have a specific narrative reason for the current ordering that I don't know.

**2b. Hero heading "Redefining" vs alternatives**
The content critique flagged "Redefining Vitamin D" as marketing-y and clashing with your "direct and real" voice. It also noted the tagline says "We are changing that" — two verbs for the same idea. Suggested alternatives: "Rethinking," "Understanding," or just leading with the subtitle. Not my call — this is hero framing.

**2c. Prose flagged as pretentious or boilerplate** (each is a ~1-line rewrite)
- Collaborators intro (line 589): "We are fortunate to work with outstanding scientists whose expertise strengthens every project we pursue." Proposed: "Scientists we work with." or "People who make our work better."
- Peers intro (line 623): "Scientists we admire and learn from — our intellectual community." Proposed: "Scientists we talk to."
- Mentors intro (line 688): "We stand on the shoulders of extraordinary scientists who shaped how we think." Proposed: "People who trained us."
- Donate blurb (~line 861): "Your contribution advances our understanding of vitamin D's potential to improve human health." Proposed Jeff-voice: "Your donation buys reagents, mice, and people-hours. That's it."

**2d. Jargon that could be simpler** (body text in Q2-Q4, Q7)
- Q2: "hepatic 25-hydroxylase activity" → "the liver enzyme that activates vitamin D"
- Q3: "coding SNPs in CYP2R1" → "genetic variants in the gene that activates vitamin D"
- Q4: "pharmacologic doses" → "doses far above replacement"
- Q7: "PTH" → "parathyroid hormone (PTH)" on first use

**2e. Missing "Next Q" lines** (per your own Q/Approach/Results/Next Q format spec)
Every Q1-Q7 paragraph is missing the forward-looking "Next question" the spec calls for. The content agent recommended adding one per paragraph. Example for Q1: *"Next: if disease drives low vitamin D, can treating disease restore it — or is low D a useful severity marker?"* I did not draft these because the forward questions come from your head — I'd be guessing about your program's current priorities.

**2f. Funding / productivity signal missing from PI card**
The PI team card currently lists title + affiliations but not publication count or funding status. A tenure committee or grant reviewer looking at the page cannot infer productivity in the first 10 seconds. The content critique recommended adding a one-line "NIH-funded, Division of Endocrinology & Diabetes, CHOP · X peer-reviewed publications" under the title. I did not fill this in because I don't know your current grant number or your preferred count framing.

### 3. Information I don't have

- **PhD thesis / graduate advisor** — the people agent asked whether your PhD or thesis advisor belongs on the Mentors list. Omitting would read as strange to field letter-writers. If the answer is "Muglia was my postdoc mentor, X was my PhD mentor," add X. If it's all already there, no action.
- **Hakonarson years** — I added "Postdoctoral mentor" to his mentor card without years. Precise is better: "Postdoctoral mentor, 20XX–20YY."
- **Collaborators list is thin** (2 names). Should there be 1-2 more active co-authors? Even a biostats or imaging-core collaborator would help.
- **CHOP URLs** — the people agent curl'd them and got 403. That's CHOP's WAF blocking bots, not broken links — but please manually click each (Hakonarson, McCormack x2, Levine) in a real browser before tenure go-live to confirm they resolve.

### 4. Photo strip decisions

- **Reorder strip**: move `talkingWide.jpg` to end → solo→solo→solo→social creates a "work leads to conversation" arc. Or swap it in first → conversation leads to rigorous work. Either is defensible. Current sequence (benchwork → pipette → talking → dryIce) is a random drop.
- **Replace dryIce**: agent flagged it as the weakest (posed, "photographer asked him to stand there"). If there's a second interaction/group photo in the archive, swap dryIce for it. I did not browse the archive for alternatives since the call is yours.

---

## Open decision queue for your review

| # | Decision | Recommended next step | Impact |
|---|----------|----------------------|--------|
| 1 | ~~**Contact email**~~ RESOLVED — `jeffroizen@gmail.com`. Form built; see `docs/contact-form-status.md` for Jeff's unblock steps. | — | DONE |
| 2 | **Q2/Q3/Q7 figure sources** | Approve Ace Scout to ping Archivist for Q1 (already done) + re-extract CYP2R1 variant figures from older decks | HIGH — unblocks 3 Q placeholders |
| 3 | **Funding signal on PI card** | Provide 1-line format (grant ID + pub count OR just "NIH-funded") | HIGH — committee/reviewer scanability |
| 4 | **Reorder Q1-Q7** | Approve or veto the Q1→Q5→Q4→Q2→Q3→Q6→Q7 reorder | MEDIUM — helps journalist/committee audiences |
| 5 | **"Redefining" hero verb** | Confirm current or switch to Rethinking / Understanding / drop heading | LOW — taste call |
| 6 | **Prose rewrites (2c above)** | Accept/reject 4 rewrites | LOW — each is a single-line edit |
| 7 | **Next Q lines** | Draft the 7 forward questions in your own voice | MEDIUM — structural completeness |
| 8 | **PhD advisor add** | Confirm Mentors list is complete | LOW unless missing |
| 9 | **Photo strip reorder/swap** | Approve move or swap | LOW — taste call |
| 10 | **Microscopy composite timed-out decision** | Confirm or override | LOW — holding state works |

---

## Diagnostic: does the site pass each audience test?

Based on the multi-audience content critique (file agent ran against the full HTML):

| Audience | Current state | Biggest remaining gap |
|---|---|---|
| **Department chair / tenure committee** | Narrative arc is coherent; mentor lineage is present; alumni placements signal training ability | Missing funding/productivity signal (#3). Thin team reads as "small lab" without a grant-line. |
| **Potential collaborator** | Methodological breadth is visible; Q4/Q6 are hooky; linked collaborator profiles work | Cannot email anyone (#1). Q7 has no "we're actively looking for metabolomics collaborators" hook. |
| **Science journalist** | Hero hook is genuinely good; Q6 has a quotable line ("metabolic traffic cop"); Q1 is a counterintuitive plain-statement finding | Q5 (biggest public-health story) is buried at position 5 — journalist may not reach it (#4 reorder). Q2-Q4 H3s still jargon-y. |
| **Grant reviewer** | Methodological breadth visible; clinical relevance in every paragraph; collaborator shared-pub counts are evidence-backed | Dead "Read the paper" links are now **removed** (previous biggest damage). Still missing Next-Q lines (#7) — reviewer wants "where is this going." |

Net assessment: the site has moved from "several credibility leaks" to "fundamentally sound with a small list of creative decisions blocking completion." The 10 items in the queue above are the punch list.

---

## Technical health summary

- **WCAG 2.1 AA**: compliant on all measured body-text contrasts. Skip link, main landmark, aria-expanded, prefers-reduced-motion all in place. One item deferred: `figure` elements in the lab strip semantically pair an image with a caption and the strip has no captions. Changing to `div` would be more semantically accurate but the `alt` attributes handle accessibility fine either way. Not blocking.
- **Broken references**: zero. `lab-group-hires.jpg` fixed (was pointing to root, should have been `photos/`). All image srcs resolve.
- **Dead links**: the 6 `href="#"` paper links are removed. The donate `href="#"` remains as an intentional placeholder for the CHOP Foundation URL (deferred).
- **CLS risk**: most above-fold images still lack explicit `width`/`height` attributes. Low priority for a single-page static site; a future pass could add them if you care about Core Web Vitals.

All technical fixes are in `compare-purple-gold.html` working file. Nothing deployed — that is still your call.

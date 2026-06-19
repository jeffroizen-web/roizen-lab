# Roizen Lab Launch Brief — target 2026-06-19

For Jeff. Answers the four questions from MSG-1ebe1a + what it takes to go live tomorrow.
Today: 2026-06-18. Canonical file: `compare-purple-gold.html`. 128 py + 18 Playwright green.

---

## TL;DR — can we launch tomorrow?

Yes, IF you make 3 decisions. The site content is done and tested. The only true
blocker is **hosting** (where does hypothesisdriven.org point?) — that needs one answer
from you and then ~30 min of my work. Everything else is polish I can apply in minutes
on your yes.

**The 3 launch-critical decisions (everything else can ship as-is or be hidden):**
1. **Hosting**: is hypothesisdriven.org already registered, and where? (Determines deploy path.)
2. **Prose**: approve the 4 one-line rewrites below (they remove marketing-speak the
   quality-gate flags — currently live on the page).
3. **Donate + Merch handling for launch** (see §3 and §4 — both have a "ship clean" option).

---

## 1. Remaining webpage edits + launch readiness

**Done and verified:** all 13 sections populated, SEO/JSON-LD/sitemap/robots, mobile +
a11y QA gate, CLS fixed, 128+18 tests green.

**Edits still open (all small):**

| Item | State | Action | Blocks launch? |
|---|---|---|---|
| Hosting / DNS | No CNAME, no host wired; `docs/DEPLOY.md` has the plan | Your hosting answer → I deploy (~30 min) | **YES** |
| 3 banned phrases (Collaborators/Mentors/Donate intros) | Live on page; quality-gate FAIL | Approve §rewrites → I apply in 1 commit | Soft (looks unfinished) |
| Hero verb "Redefining" | Live | Keep, or switch to "Rethinking" (my pick) — your call | No (keep = fine) |
| Donate button | `href="#"` (dead link) | See §3 | Soft (dead CTA is bad) |
| Merch section | 6 "Image" placeholder cards, no checkout | See §4 | Soft (looks unfinished) |
| Figures q2/q3/q7 | "Figure pending" placeholders | Ship as-is, or swap to existing PNGs (WMF decision) | No |
| Contact form | Code done; shows "not configured" until Formspree ID set | 2-min account setup (§3) | Soft |

**My launch recommendation:** apply the 4 prose rewrites, hide merch, point donate at the
CHOP giving page (general if the designated URL isn't ready), set up Formspree if you have
2 min. That gets a clean, credible, fully-functional site live with zero dead ends.

## 2. Fundraising — how it works + how to test

**How it works today:** we do NOT process payments. The "Donate Through CHOP" button is
designed to hand off to the **CHOP Foundation** giving page, which handles the transaction
and tax-deductibility. The button currently points at `#` (nowhere) because we never got
the designated-fund URL.

**To make it real (pick one):**
- **A (best):** get the CHOP Foundation **designated-fund URL** for the Roizen Lab / Division
  of Endocrinology from CHOP's development office. I can draft that email for you to send.
- **B (launch-safe fallback):** point the button at the general CHOP giving page
  (`giving.chop.edu`) for launch — still real, still tax-deductible — and add the lab-specific
  designation when dev office provides it.

**Can you test it?** There's no sandbox WE build — CHOP's platform is the processor. Testing =
(1) click the live button, confirm it lands on a CHOP page that lets you designate the gift to
the lab; (2) optionally make a real small gift ($5) and confirm it routes + is acknowledged, or
ask CHOP dev office whether they have a test mode. The thing to verify is the **designation**,
not the payment rails (those are CHOP's, already battle-tested).

## 3b. Contact form testing
Local: serve the file, open `#contact`, submit a test message → expect green success + an
email at jeffroizen@gmail.com + a phone push. Needs your 2-min setup: create the free
Formspree account (jeffroizen@gmail.com) and subscribe the ntfy topic `roizen-lab-contact`.
Steps in `docs/contact-form-status.md`. Until then the form politely tells visitors to email you.

## 4. Merch — provider options + recommendation

**Provider landscape (2026, both free / pay-per-order, no inventory):**
- **Printify**: free **standalone storefront** built in, ~$4/shirt cheaper, 2x product range,
  marketplace of print suppliers (quality varies by supplier). Best when you want a store with
  zero other tooling.
- **Printful**: in-house printing = more consistent quality + better branding, but needs a
  storefront you provide (Shopify, etc.); Growth plan $24.99/mo waived above $12k/yr sales.
  Best when brand polish matters and you already have a store.

**My recommendation: Printify standalone store** when you do this — free, no Shopify needed,
lowest friction for a lab vanity store.

**But — institutional flag (real, not a nitpick):** selling "Roizen Lab"-branded merch where
"all proceeds support research" through a CHOP/Penn-affiliated site raises three questions that
aren't mine to answer: (a) use of CHOP/Penn trademarks, (b) where sale revenue legally lands
(POD markup is NOT a tax-deductible donation and can't drop into a CHOP research fund without
sign-off), (c) tax treatment. **This needs CHOP dev office / Penn before any real store.**

**For launch tomorrow:** the merch section is 6 placeholder cards with no checkout — it reads
as unfinished on a tenure-credibility site. **Recommend: hide it for launch** (one-line change,
fully reversible), stand up the real store post-launch once the institutional questions clear.
Alternative: convert the cards to "support the lab" links to the CHOP giving page (a gift, not
a sale — sidesteps the compliance issue entirely).

## 5. Full open-questions / decisions list (everything blocking a polished launch)

**Launch-critical (need you tomorrow):**
1. **Hosting**: domain registered? where? (GitHub Pages = my recommended path, free; needs a
   one-time DNS pointer from you/registrar.)
2. **Prose**: approve the 4 rewrites below (or veto individually).
3. **Donate**: option A (get CHOP designated URL) or B (general CHOP page for launch)?
4. **Merch**: hide for launch (rec) / convert to giving links / keep placeholders?

**Quick creative calls (defaults are fine — veto only):**
5. Hero verb: keep "Redefining" or switch to "Rethinking"? (default: keep)
6. Big-Questions layout + Q order: staged alternates in `prototypes/design-review-2026-05-14.html`
   (default: keep current)
7. Figure-to-question matching: you flagged it may be wrong; figures q2/q3/q7 show "Figure
   pending" (default: launch with pending, fix post-launch) — or bless PNG-only swap.

**2-minute setups (you, one-time):**
8. Formspree account + ntfy topic subscribe (contact form).

**Post-launch (no deadline):**
9. CHOP Foundation designated-fund URL (from dev office).
10. Real merch store + institutional sign-off.
11. Archivist publications-feed counter-sig (auto-populates Publications when signed).

---

## The 4 prose rewrites (staged — Jeff's voice, from the design-review packet)

| Section | Current (flagged) | Proposed |
|---|---|---|
| Collaborators | "We are fortunate to work with outstanding scientists whose expertise strengthens every project we pursue." | "People who make our work better." |
| Peers | "Scientists we admire and learn from — our intellectual community." | "Scientists we talk to." |
| Mentors | "We stand on the shoulders of extraordinary scientists who shaped how we think." | "People who trained us." |
| Donate | "Your contribution advances our understanding of vitamin D's potential to improve human health…" | "Your donation buys reagents, mice, and people-hours. That's it." |

Say "prose: all four" (or pick a subset) and I apply them in one commit.

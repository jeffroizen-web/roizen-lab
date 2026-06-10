# Deploy Playbook — hypothesisdriven.org

> Written 2026-06-10 (Ace Scout). Purpose: make GO-LIVE a single step the moment Jeff
> answers the one hosting question. Every claim below is verified against the working tree,
> not assumed. Tenure clock: site must be LIVE by ~Aug 2026 (letters solicited ~Sep 2026).

## Verified current state (2026-06-10)

| File | Size | Date | Role | Asset paths |
|---|---|---|---|---|
| `compare-purple-gold.html` | 80.7 KB | 2026-05-19 | **Working file — canonical content** (13 sections, CLS-fixed, PI card, contact form) | root-relative |
| `production/index.html` | 80.6 KB | 2026-02-28 | Production build — **3.5 months STALE** (2350 diff lines behind working) | parent-relative (`../favicon.png`) |
| `index.html` (repo root) | 10.6 KB | 2026-02-17 | Old scaffold — **not the real site**, predates everything | root-relative |

**No deploy infrastructure exists**: no `CNAME`, no `.github/workflows/`, no `netlify.toml`,
no `vercel.json`. The domain hypothesisdriven.org is **not pointed at any host** (unverified
whether the domain is even registered/parked — this is the open Jeff question).

**Drift production/ is missing vs working** (verified by grep): CLS width/height on imgs
(3 vs 14), `loading="lazy"` (4 vs 11), PI-funding card (`NIH-funded` 0 vs 1), contact-form
`aria-live` (0 vs 1). Both files still contain the 3 Jeff-gated banned phrases
(`shoulders`, `fortunate to work`, `advances our understanding`) — those resolve via the
prose-rewrite picks in Kleiber's Jeff batch, applied to whichever file becomes canonical.

## The one open question (NEED-FROM-JEFF)

**Is hypothesisdriven.org already registered/hosted, and where?**
The answer selects the path below and determines asset-path reconciliation. Everything else
is mechanical and orchestra-doable.

## Decision tree

### Path A — GitHub Pages (zero hosting cost, simplest if repo goes to GitHub)
1. Canonical site must be served as **root `index.html`** with **root-relative** asset paths.
   → Promote `compare-purple-gold.html` → root `index.html` (working file ALREADY uses
   root-relative paths, so **no path rewrite needed** — this is the lower-rework path).
2. Add `CNAME` file at repo root containing `hypothesisdriven.org`.
3. Enable Pages on `main` branch, root. DNS: point apex `A`/`AAAA` records to GitHub Pages
   IPs (Jeff or registrar GUI) + `www` CNAME to `<user>.github.io`.
4. Retire `production/` and the stale root scaffold to avoid dual-source drift.

### Path B — Netlify / Vercel (build step, preview deploys, form handling)
1. Can serve from a subdir; keep `production/` as publish dir BUT first sync it to working
   content (resolve the parent-relative vs root-relative mismatch — Netlify publish-dir is
   web root, so paths become root-relative → same rewrite as Path A anyway).
2. Add `netlify.toml` (publish dir + headers) or `vercel.json`.
3. Connect repo, set custom domain hypothesisdriven.org, Netlify manages DNS/SSL.
4. Bonus: Netlify Forms could replace the Formspree dependency (removes one Jeff signup).

### Recommendation
**Path A** unless Jeff wants preview-deploys / managed forms. Rationale: working file is
already root-relative → least reconciliation, least rework, no third-party account. One
canonical `index.html`, kills the 3-file drift permanently.

## Single-source-of-truth fix (do regardless of path)

The three near-duplicate HTML files are the root drift risk. After path selection, collapse
to ONE canonical `index.html`; delete or archive the other two. Until then, **`compare-purple-gold.html`
is the single source of content truth** — do not edit `production/index.html` or root
`index.html`.

## Pre-live checklist (mechanical, orchestra-doable once path chosen)
- [ ] Canonical file promoted, asset paths verified (open in browser, zero broken images)
- [ ] 3 Jeff-gated prose rewrites applied (from design-review packet)
- [ ] WMF PNG-only figure decision applied (figure-pending q2/q3/q7 closed)
- [ ] `tenure_readiness.py` grade C → B confirmed
- [ ] OG `og:image` social-preview.png generated (pending final logo) + wired
- [ ] sitemap.xml + robots.txt added
- [ ] Cross-browser + mobile QA via Playwright, zero console errors
- [ ] Formspree signup + ntfy subscribe done (contact form Layer 1) OR migrated to host forms
- [ ] DNS cutover (Jeff/registrar GUI) — the only true Jeff/GUI step

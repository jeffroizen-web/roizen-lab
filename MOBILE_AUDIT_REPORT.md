# Mobile/Responsive Audit — compare-purple-gold.html
Date: March 7, 2026

## Summary
**4 critical issues, 6 moderate issues, 5 minor issues**

Static analysis of CSS rules, media queries, and HTML structure at three target viewports (375px, 414px, 768px). All findings are inferred from code — visual confirmation recommended where noted.

---

## Media Queries & Breakpoints Currently Defined

Only **one breakpoint** is used: `max-width: 768px`, appearing twice:

1. **Lines 203-207** — Big Questions section only: collapses `.question-row` grid from 2-col to 1-col, resets `direction: ltr` on even rows, reduces `.question-figure` min-height.
2. **Lines 304-320** — General mobile rules: shrinks institution bar, repositions navbar, shows hamburger toggle, hides nav links (mobile menu), reduces hero `h1` font size, collapses `.questions-grid` and `.merch-grid` to 1-col, reduces section padding.

**No intermediate breakpoints exist** (e.g., no 480px, 576px, or 1024px queries). The site jumps from full desktop to a single mobile state at 768px.

---

## Critical Issues (breaks layout)

### C1. News Grid Overflows Viewport at 375px and 414px
- **Selector:** `.news-grid` (line 237)
- **Rule:** `grid-template-columns: repeat(auto-fit, minmax(320px, 1fr))`
- **Problem:** The `minmax(320px, 1fr)` means each card demands at least 320px. At 375px viewport with 24px padding on each side (`.container`), the available content width is 327px. This barely fits one column. However, at exactly 320px content width or below, the grid item will exceed the container and cause **horizontal scroll**. With slight variance in device rendering, this is a borderline overflow risk at 375px. At 414px (366px content width), one column fits but the card is nearly full-bleed with minimal margin.
- **Severity:** Critical — horizontal scroll is the single worst mobile UX failure.
- **Fix direction:** Add a mobile override: `.news-grid { grid-template-columns: 1fr; }` inside the 768px media query.

### C2. Alumni Grid Overflows Viewport at 375px
- **Selector:** `.alumni-grid` (line 248)
- **Rule:** `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))`
- **Problem:** Same pattern as news grid. At 375px with 48px total horizontal padding, content width is 327px. A 300px minimum fits, but barely. If any alumni card content (especially the long career path text in `.alumni-years`) forces wider rendering, overflow occurs. The `minmax(300px, ...)` is safer than 320px but still tight.
- **Severity:** Critical — potential horizontal overflow on smallest phones.
- **Fix direction:** Add `grid-template-columns: 1fr` in the mobile query, or reduce minmax to `minmax(250px, 1fr)`.

### C3. Nav Links Have No Mobile Tap Target Sizing
- **Selector:** `.nav-links a` (line 115-118)
- **Rule:** `font-size: 0.85rem` with no explicit padding or min-height
- **Problem:** When the mobile menu opens (`.nav-links.active`), the links are flex-column with `gap: 16px` (line 312). The `<a>` elements have no padding, so their touch target is only the text height (~14px tall at 0.85rem). Apple HIG and WCAG require **minimum 44px touch targets**. Users will mis-tap adjacent links.
- **Severity:** Critical — fails accessibility guidelines and causes frustration on every mobile visit.
- **Fix direction:** Add `padding: 12px 0` to `.nav-links a` inside the mobile query, bringing effective height to ~38-44px.

### C4. `.questions-grid` Selector in Mobile Query Does Not Match Any Element
- **Selector:** `.questions-grid` (line 317)
- **Problem:** The mobile media query at line 317 targets `.questions-grid { grid-template-columns: 1fr; }`, but the actual class used in the HTML is `.questions-list` (line 175, line 381). This rule is **dead CSS** — it does nothing. The actual Big Questions grid collapse is handled by the separate media query at lines 203-207 targeting `.question-row`, which works correctly. So the questions section does collapse properly, but this dead rule indicates potential confusion if future edits target the wrong selector.
- **Severity:** Critical (as a code defect) / Low (as a visual defect, since lines 203-207 handle it). Flagged as critical because it signals a mismatch that could cause real breakage if the working query at 203-207 is ever removed.

---

## Moderate Issues (usable but suboptimal)

### M1. Hero `h1` at 2.2rem May Be Too Large for 375px
- **Selector:** `.hero h1` mobile override (line 316)
- **Rule:** `font-size: 2.2rem` (reduced from 3.2rem desktop)
- **Problem:** At 375px, 2.2rem (~35px) is large for a heading with the word "Redefining" (11 characters). Combined with the `<em>Vitamin D</em>` on the same line, this likely wraps to 2-3 lines. Not a breakage, but the hero may feel cramped. The `<br>` tags in `.hero-subtitle` (line 366) also force specific line breaks that won't align with mobile text flow.
- **Severity:** Moderate — readable but visually awkward.
- **Recommendation:** Consider `font-size: 1.8rem` at 375px. Remove `<br>` tags from `.hero-subtitle` or wrap them in a `<span class="desktop-break">` hidden on mobile.

### M2. Section Header `h2` at 2.4rem Has No Mobile Override
- **Selector:** `.section-header h2` (line 166)
- **Rule:** `font-size: 2.4rem` (~38px) at all viewports
- **Problem:** At 375px, long headings like "Selected Papers" fit fine, but the font size is disproportionately large relative to the mobile viewport. No mobile reduction is defined.
- **Severity:** Moderate — not broken, but feels oversized on phone screens.
- **Recommendation:** Add `font-size: 1.6rem` to `.section-header h2` in the mobile query.

### M3. Team Grid May Display Awkwardly at 768px
- **Selector:** `.team-grid` (line 218)
- **Rule:** `grid-template-columns: repeat(auto-fit, minmax(260px, 1fr))`
- **Problem:** At 768px (content width ~720px after padding), `auto-fit` with `minmax(260px, ...)` yields 2 columns (~360px each). With 3 team cards, the third card sits alone on a second row, centered (due to `justify-items: center`). This creates a lopsided 2+1 layout. At 375px, it collapses to 1 column properly.
- **Severity:** Moderate — functional but aesthetically unbalanced at tablet width.
- **Recommendation:** Consider forcing 1-column at 768px or adjusting minmax to allow 3 columns at tablet width.

### M4. Contact Section Inline Grid Has No Mobile Override
- **Selector:** Inline style at line 665: `display:grid; grid-template-columns:repeat(auto-fit, minmax(280px,1fr))`
- **Problem:** At 375px (327px content width), `minmax(280px, ...)` fits one column — barely. The inline style cannot be overridden by a media query in the `<style>` block without `!important`. This is a maintainability issue.
- **Severity:** Moderate — works at all three viewports by luck (280px < 327px), but inline styles resist responsive overrides.
- **Recommendation:** Move to a CSS class.

### M5. Donate Section `::before` Pseudo-Element Extends Off-Screen
- **Selector:** `.donate-section::before` (lines 277-280)
- **Rule:** `right: -15%; width: 500px; height: 500px`
- **Problem:** The decorative radial gradient circle is positioned at `right: -15%` with a fixed 500px width. On a 375px viewport, `-15%` of 375px is -56px, and the element extends 500px from that point. Since the section has `overflow: hidden` (line 276), this won't cause horizontal scroll, but it does mean the decorative element is mostly off-screen on mobile — wasted rendering.
- **Severity:** Moderate — no visual breakage, but unnecessary paint on mobile.

### M6. Merch Grid Collapse Uses Wrong Selector Pattern
- **Selector:** `.merch-grid` (line 259 desktop, line 318 mobile)
- **Desktop rule:** `grid-template-columns: repeat(3, 1fr)` — fixed 3 columns
- **Mobile rule (768px):** `grid-template-columns: 1fr` — 1 column
- **Problem:** There is no intermediate breakpoint. At 769px, the grid is 3 columns. With 6 merch cards and a content width of ~721px, each card is ~230px wide. The `.merch-image-placeholder` has `height: 200px` — these will look nearly square and cramped at medium widths. Below 768px, it jumps directly to 1 column (full-width cards), which is fine but means no 2-column tablet layout.
- **Severity:** Moderate — functional but the 3-to-1 jump is visually jarring near the breakpoint.

---

## Minor Issues (polish items)

### m1. No `loading="lazy"` on Any Images
- **Lines:** 89-90 (institution bar), 113 (nav logo), 200-202 (question figures), 345 (nav logo), 458 (PI portrait), 464 (Mike Nguyen photo), 575 (lab group photo)
- **Problem:** No images use `loading="lazy"`. The lab group photo (`lab-group-hires.jpg`) and microscopy hero background are likely large files. On mobile connections, these will block rendering.
- **Severity:** Minor — performance issue, not layout breakage.
- **Recommendation:** Add `loading="lazy"` to all images below the fold (team photos, alumni group photo). The hero background image loaded via CSS `url()` cannot be lazy-loaded natively but could use an intersection observer.

### m2. `paper-link` Touch Targets Are Small
- **Selector:** `.question-text .paper-link` (lines 189-193)
- **Rule:** `font-size: 0.85rem`, `display: inline-block`, `margin-top: 12px`
- **Problem:** No padding defined. The "Read the paper" links are small inline-block elements. Touch target is approximately 14px tall by ~120px wide. Below the 44px minimum.
- **Severity:** Minor — these are secondary navigation, not primary CTAs.

### m3. Theme Indicator Overlaps Content on Small Screens
- **Selector:** `.theme-indicator` (lines 295-301)
- **Rule:** `position: fixed; bottom: 16px; right: 16px`
- **Problem:** The floating theme toggle pill sits in the bottom-right corner. On 375px, this could overlap the donate button or footer content when scrolled to those sections. No mobile hide or repositioning.
- **Severity:** Minor — this is likely a development-only UI element, not production.

### m4. Institution Bar Logo Height at Mobile (16px) May Be Too Small
- **Selector:** `.institution-bar img` mobile override (line 306)
- **Rule:** `height: 16px` (reduced from 22px desktop)
- **Problem:** CHOP and Penn Medicine logos at 16px height may be unreadable, especially on high-density mobile screens where 16px CSS is fine physically but the logos contain text. Needs visual confirmation.
- **Severity:** Minor — the logos are links to external sites, not primary content. But brand visibility matters for institutional credibility.

### m5. Hero Subtitle Uses `<br>` Tags for Line Breaks
- **Selector:** `.hero-subtitle` content (line 366)
- **HTML:** `Vitamin D is one of the most<br>recommended therapies in medicine &mdash;<br>and one of the least understood.`
- **Problem:** Hard `<br>` tags create desktop-optimized line breaks that produce awkward wrapping on mobile. At 375px, the natural word-wrap and the forced `<br>` breaks will conflict, creating lines of uneven length.
- **Severity:** Minor — readable, but visually rough.

---

## Section-by-Section Analysis

### Institution Bar
- **375px:** Bar shrinks to 32px height, logos to 16px. Fits without overflow — flexbox `space-between` handles left/right logos. The `inst-divider` (1px x 16px) and two left-side logos with 12px gap fit within ~180px, leaving room for Penn Medicine logo on right. **Functional but logos may be hard to read at 16px.**
- **414px:** Same as 375px — slightly more breathing room. No issues.
- **768px:** Desktop styles apply (40px height, 22px logos). Plenty of room. No issues.

### Nav Bar
- **375px:** Hamburger toggle appears (`display: block`). Nav links hidden until toggled. Logo at 55px height fits. Navbar repositioned to `top: 32px` (below shorter institution bar). **Works correctly.** Touch target concern on nav links when menu opens (see C3).
- **414px:** Same behavior as 375px. No issues beyond C3.
- **768px:** Hamburger toggle appears (breakpoint is `max-width: 768px`, so 768px exactly triggers mobile). With 9 nav links at `0.85rem` with `24px` gap, the desktop layout needs roughly `9 * 70px + 8 * 24px = 822px` for the links alone. At 768px, the nav would overflow **if** the desktop styles applied. Since the mobile query activates at exactly 768px, this is fine. **However, at 769px** the desktop nav would be extremely tight. This is a moderate concern for small tablets in landscape.
- **Note:** The nav link click handler (line 689) correctly closes the mobile menu after a link is tapped. Good.

### Hero Section
- **375px:** `min-height: 90vh` is fine. Padding `170px` top (for both bars: 32px + 70px = 102px) leaves 68px extra — generous. Hero `h1` at 2.2rem wraps "Redefining Vitamin D" to 2 lines. `<br>` tags in subtitle create awkward breaks (see m5, M1). Background image `center/cover` works. Overlay gradient via `::before` covers fully. **Functional but subtitle line breaks are suboptimal.**
- **414px:** Same as 375px with slightly better text flow. "Redefining Vitamin D" may fit on one line at 2.2rem. Still has `<br>` issue.
- **768px:** Hero `h1` stays at desktop 3.2rem (mobile query fires at 768px, reducing to 2.2rem). At exactly 768px, 2.2rem is comfortable. Background image scales well via `cover`. No issues.

### Big Questions (7 questions, 2-column grid)
- **375px:** `.question-row` collapses to `grid-template-columns: 1fr` (line 204). Even rows reset to `direction: ltr` (line 205). Figure min-height drops to 200px. **Works correctly.** Each question stacks as text-above-figure. Questions gap is 64px between rows (line 175) — may feel excessive on mobile but not broken.
- **414px:** Same as 375px. No issues.
- **768px:** The media query fires at `max-width: 768px`, so at exactly 768px, the grid collapses to 1 column. At 769px, it would be 2 columns with `gap: 48px` in ~720px content width = ~336px per column. Tight but functional.

### Team Cards
- **375px:** `.team-grid` uses `repeat(auto-fit, minmax(260px, 1fr))`. At 327px content width, `minmax(260px, ...)` produces 1 column. Cards center via `justify-items: center` with `max-width: 300px`. **Works correctly.** Photo circle at 180px is ~55% of viewport width — appropriate.
- **414px:** Content width ~366px. Still 1 column (366px > 260px, but not enough for 2 * 260px = 520px). **Works correctly.**
- **768px:** Content width ~720px. Two columns fit (2 * 260px + 40px gap = 560px < 720px). Third card orphaned on row 2 (see M3). **Functional but asymmetric.**

### Alumni Grid
- **375px:** `minmax(300px, 1fr)` in 327px content width. One column fits (300px < 327px). 9 alumni cards stack vertically. **Works, but tight** (see C2 for edge-case risk). The lab group photo above the grid uses `max-width:700px; width:100%` — scales down properly.
- **414px:** Content width ~366px. One column. No issues.
- **768px:** Content width ~720px. Two columns (2 * 300px + 20px gap = 620px < 720px). 9 cards = 5 rows (4 pairs + 1 orphan). **Functional.**

### Publications Section
- **375px:** `.pub-list` has `max-width: 800px` but sits inside `.container` (max-width 1100px, padding 24px). At 375px, content width is 327px. Publication text at `1rem` / `0.83rem` is readable. No filter buttons exist in this version — just a PubMed link. **Works correctly.**
- **414px:** Same. No issues.
- **768px:** Same. No issues.

### News Section
- **375px:** See C1. `minmax(320px, ...)` in 327px width. Barely fits. **Risk of horizontal overflow.**
- **414px:** Content width ~366px. One column fits with 46px margin. **OK.**
- **768px:** Content width ~720px. Two columns (2 * 320px + 28px gap = 668px < 720px). **Works.**

### Gear / Merch Section
- **375px:** Mobile query sets `grid-template-columns: 1fr`. 6 cards stack vertically. Image placeholders at 200px height, full-width. **Works correctly.**
- **414px:** Same. **Works.**
- **768px:** Mobile query fires (768px), so 1 column. At 769px, jumps to 3 columns (see M6). **Functional.**

### Donate Section
- **375px:** Text-only section with centered content. `.btn-donate` has `padding: 16px 48px` — button width is roughly 250px, fitting within 327px content width. No form inputs. **Works correctly.** Button touch target (16px * 2 + line-height = ~50px+) meets 44px minimum.
- **414px:** Same. No issues.
- **768px:** Same. No issues.

### Contact Section
- **375px:** Inline grid `minmax(280px, 1fr)` in 327px width. One column. **Works.**
- **414px:** Same. **Works.**
- **768px:** Content width inside `max-width:750px` container. Two columns (2 * 280px + 40px gap = 600px < 720px). **Works.**

### Footer
- **375px:** Simple centered text with `padding: 36px 24px`. `font-size: 0.85rem`. **Works correctly.** No stacking needed — content is just two short `<p>` tags.
- **414px:** Same. No issues.
- **768px:** Same. No issues.

---

## Additional Checks

### Viewport Meta Tag
Present and correct at line 5: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`. No issues.

### Horizontal Scroll Risk
- **Primary risks:** `.news-grid` (C1) and `.alumni-grid` (C2) at 375px.
- **Mitigated by `overflow: hidden`:** Only `.donate-section` and `.hero` have `overflow: hidden`. The news and alumni grids do NOT — overflow will escape to the body.
- **No global `overflow-x: hidden` on `body` or `html`.** If any element exceeds viewport width, the page scrolls horizontally.

### Text Contrast on Mobile
- Hero text over background image: overlay gradient ensures contrast. `rgba(59,31,110,0.82)` start opacity is strong. **Adequate.**
- Institution bar: white text/logos on `#3B1F6E` (dark purple). **Passes AA.**
- Nav links: `var(--primary)` (#3B1F6E) on white. **Passes AAA.**
- Body text: `#2C2C2C` on white. **Passes AAA.**

### Interactive Element Spacing
- Nav links in mobile menu: 16px gap, no padding (C3). **Fails 44px target.**
- "Read the paper" links: no padding, small font (m2). **Fails 44px target.**
- CTA buttons (`.btn`, `.btn-donate`): 14-16px vertical padding. **Meets 44px target.**
- Publication items: 22px padding, no interactive elements within (the section header has one `<a>` link to PubMed). **Adequate spacing.**

---

## Recommendations (prioritized)

1. **[C1/C2] Fix grid minimums for news and alumni grids.** Change `minmax(320px, ...)` and `minmax(300px, ...)` to `1fr` inside the 768px media query. This is the single highest-impact fix — prevents horizontal scroll on iPhones.

2. **[C3] Add padding to mobile nav links.** Add `padding: 12px 0; min-height: 44px;` to `.nav-links a` inside the mobile media query. This is an accessibility requirement.

3. **[C4] Remove or fix the dead `.questions-grid` selector** in the mobile media query (line 317). It targets a nonexistent class.

4. **[M1/m5] Adjust hero text for mobile.** Reduce `h1` to `1.8rem` at 375px. Remove or conditionally hide `<br>` tags in `.hero-subtitle`.

5. **[M2] Add mobile font-size reduction for `.section-header h2`.** Suggest `1.6rem` inside the 768px query.

6. **[M4] Extract contact section inline grid styles to a CSS class** so they can be overridden by media queries without `!important`.

7. **[M3/M6] Consider a 480px intermediate breakpoint** for team grid and merch grid to provide a 2-column tablet layout.

8. **[m1] Add `loading="lazy"` to below-fold images** (team photos, alumni group photo).

9. **[m3] Hide `.theme-indicator` on mobile** (or move to a less intrusive position). This is a dev-only control.

10. **[m4] Verify institution bar logo readability at 16px** with a visual test on an actual device.

---

*This audit was conducted via static CSS/HTML analysis. Items marked "needs visual confirmation" should be verified by rendering the page at each viewport width in a browser or device emulator.*

// T5 — R-6-mobile: 375px no-horizontal-overflow Playwright test (craft-uplift spec).
//
// Guards at a 375px viewport:
// - document.documentElement.scrollWidth <= 375 (class assertion — catches any overflow cause)
// - body.scrollWidth <= viewport width
// - content grids (.news-grid, .alumni-grid, .team-grid) render as single column
//   (no child element overflows its parent's width)
// - .questions-list section does not contribute to overflow
//   (dead .questions-grid selector must be corrected to the live element)
// - touch targets stay >= 44px (must not regress from the base tree)
//
// TDD RED on the current tree:
//   - .news-grid has grid-template-columns: repeat(auto-fit, minmax(320px, 1fr))
//     which forces a 320px minimum column at 375px viewport → overflow
//   - .alumni-grid has minmax(300px, 1fr) → same issue
//   - inline grid at line 895 has minmax(320px, 1fr) → overflow
// GREEN after: all content grids collapse to 1fr single-column at ≤ 375px.
//
// Run: npx playwright test tests/mobile-overflow.spec.js
const { test, expect } = require('@playwright/test');
const { spawn } = require('child_process');

const PORT = 8375; // Distinct from site-qa.spec.js (8767) to allow parallel runs
const BASE = `http://localhost:${PORT}/compare-purple-gold.html`;

// ---------------------------------------------------------------------------
// Server lifecycle
// ---------------------------------------------------------------------------

test.beforeAll(async () => {
  globalThis.__overflowServer = spawn('python3', ['-m', 'http.server', String(PORT)], {
    cwd: __dirname + '/..',
    stdio: 'ignore',
  });
  // Allow the HTTP server to start
  await new Promise((r) => setTimeout(r, 900));
});

test.afterAll(() => {
  if (globalThis.__overflowServer) {
    globalThis.__overflowServer.kill();
  }
});

// ---------------------------------------------------------------------------
// All tests run at the exact 375px viewport called out in the spec
// ---------------------------------------------------------------------------

test.describe('R-6-mobile: 375px viewport overflow (craft-uplift T5)', () => {
  test.use({ viewport: { width: 375, height: 812 } });

  // T5 primary assertion: no horizontal overflow at 375px
  test('ac6_no_horizontal_overflow_at_375px', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth
    );
    expect(
      overflow,
      `Horizontal overflow of ${overflow}px at 375px viewport — check grid minmax() values`
    ).toBeLessThanOrEqual(0);
  });

  // Body scrollWidth class check (catches any element wider than the viewport)
  test('ac6_body_scroll_width_within_viewport', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    const { viewport, bodyScrollWidth } = await page.evaluate(() => ({
      viewport: window.innerWidth,
      bodyScrollWidth: document.body.scrollWidth,
    }));
    expect(
      bodyScrollWidth,
      `body.scrollWidth (${bodyScrollWidth}px) exceeds viewport (${viewport}px) at 375px`
    ).toBeLessThanOrEqual(viewport);
  });

  // Content grids must be in single-column layout (no child overflows parent)
  test('ac6_named_grids_single_column_at_375px', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    const gridOverflows = await page.evaluate(() => {
      const grids = document.querySelectorAll('.news-grid, .alumni-grid, .team-grid, .merch-grid');
      const overflowing = [];
      for (const grid of grids) {
        const parentWidth = grid.offsetWidth;
        for (const child of grid.children) {
          // A single-column child should start at offsetLeft ~0 and fit within parent
          if (child.offsetWidth > parentWidth + 4) {
            overflowing.push(
              `${grid.className}: child offsetWidth=${child.offsetWidth}px > parent=${parentWidth}px`
            );
          }
        }
      }
      return overflowing;
    });
    expect(
      gridOverflows,
      `Grid children overflow their parent at 375px:\n${gridOverflows.join('\n')}`
    ).toEqual([]);
  });

  // Inline grids (elements with inline style display:grid) must also fit
  test('ac6_inline_grid_elements_do_not_overflow', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    const inlineGridOverflows = await page.evaluate(() => {
      const allEls = document.querySelectorAll('[style*="display:grid"], [style*="display: grid"]');
      const overflowing = [];
      for (const el of allEls) {
        if (el.scrollWidth > el.clientWidth + 2) {
          overflowing.push(
            `inline grid: scrollWidth=${el.scrollWidth}px > clientWidth=${el.clientWidth}px ` +
            `(${el.className || el.tagName})`
          );
        }
      }
      return overflowing;
    });
    expect(
      inlineGridOverflows,
      `Inline grid element(s) overflow at 375px:\n${inlineGridOverflows.join('\n')}`
    ).toEqual([]);
  });

  // Questions section: the dead .questions-grid selector must be corrected.
  // After fix, the questions section must not overflow the 375px viewport.
  test('ac6_questions_section_no_overflow_at_375px', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    const questionsOverflow = await page.evaluate(() => {
      // The questions section is identified by its ID or by the .questions-list class
      const section = document.querySelector('#questions') || document.querySelector('.questions-list');
      if (!section) return { overflow: 0, note: 'section not found' };
      const overflow = section.scrollWidth - section.clientWidth;
      return { overflow, note: '' };
    });
    expect(
      questionsOverflow.overflow,
      `Questions section overflows by ${questionsOverflow.overflow}px at 375px ` +
      `(dead .questions-grid selector may be uncorrected)`
    ).toBeLessThanOrEqual(1);
  });

  // Touch targets must not regress below 44px (already locked on base tree)
  test('ac6_touch_targets_not_regressed_below_44px', async ({ page }) => {
    const MIN = 44;
    await page.goto(BASE, { waitUntil: 'networkidle' });
    // Check the hamburger toggle (most vulnerable touch target on mobile)
    const toggle = page.locator('.nav-toggle');
    if (await toggle.count() > 0) {
      const tb = await toggle.boundingBox();
      if (tb) {
        expect(Math.round(tb.width),  `hamburger width ${tb.width}px < ${MIN}px`).toBeGreaterThanOrEqual(MIN);
        expect(Math.round(tb.height), `hamburger height ${tb.height}px < ${MIN}px`).toBeGreaterThanOrEqual(MIN);
      }
    }
  });
});

// ---------------------------------------------------------------------------
// Edge case: the overflow fix must not regress the 390px breakpoint
// (existing site-qa.spec.js test covers 390px; this test confirms 375px ≤ 390px)
// ---------------------------------------------------------------------------

test.describe('R-6-mobile: edge — 375px is the tighter constraint', () => {
  test.use({ viewport: { width: 375, height: 812 } });

  test('ac6_375px_tighter_than_390px_guard', async ({ page }) => {
    // If 375px passes, 390px should pass too (it has more room).
    // This is a structural sanity check on the fix, not an independent regression.
    await page.goto(BASE, { waitUntil: 'networkidle' });
    const overflow375 = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth
    );
    // At 375px the fix must hold; the assertion doubles as a note in the report.
    expect(overflow375, '375px is the binding constraint — this must pass').toBeLessThanOrEqual(0);
  });
});

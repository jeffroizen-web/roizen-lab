// Guards for the Big Questions rows whose figure does not exist yet (Q2/Q3/Q7).
// Rams craft ruling 2026-09-08 (6cbbc79) + build spec (2c4595a): keep all seven
// questions, drop the empty placeholder frame, let those three run as a single
// text column on the left editorial axis.
//
// WHY THESE ARE RENDERED TESTS AND NOT SOURCE ASSERTIONS: the whole defect class
// here is CASCADE, which source text cannot show. Both bugs below shipped green
// against the markup and were only visible in computed style:
//
//   1. `.question-row--no-figure` (0,1,0) LOSES to `.question-row:nth-child(even)`
//      (0,2,0 — a class plus a pseudo-class) no matter where it sits. Rams's spec
//      predicted a specificity TIE decided by source order; that was wrong, and
//      placing the rule after was not sufficient. Q2, an even row, kept
//      direction:rtl and its heading rendered at 599px hard against the right
//      edge with empty space beside it — worse than the placeholder it replaced,
//      and quiet enough to ship. Fixed by doubling the class to (0,2,0), which
//      does tie, so source order then decides.
//   2. Doubling the class then made the desktop rule beat the (0,1,0)
//      `.question-row { grid-template-columns: 1fr }` inside @media (max-width:768px),
//      so the 62ch cap leaked into mobile: 567px columns at 768 where every other
//      row used the full 720px. Fixed with an explicit same-specificity reset in
//      that block rather than relying on the cascade to stay inert.
//
// Both were caught by measuring, because Rams asked for the cascade claim to be a
// measurement rather than an argument. Keep them measurements.

const { test, expect } = require('@playwright/test');
const { resolveTarget, startServer, stopServer } = require('./target');

const { base: BASE, remote: REMOTE } = resolveTarget(8401);
const NO_FIG = ['q2', 'q3', 'q7'];

test.beforeAll(async () => {
  globalThis.__nfServer = await startServer(8401, REMOTE, 900);
});
test.afterAll(() => stopServer(globalThis.__nfServer));

async function probe(page, width) {
  await page.setViewportSize({ width, height: 900 });
  await page.goto(BASE, { waitUntil: 'networkidle' });
  return page.evaluate((ids) => {
    const row = (id) => document.getElementById(id);
    return {
      rows: ids.map((id) => {
        const el = row(id);
        const h = el && el.querySelector('h3');
        const cs = el && getComputedStyle(el);
        return {
          id,
          hasClass: !!el && el.classList.contains('question-row--no-figure'),
          direction: cs ? cs.direction : null,
          cols: cs ? cs.gridTemplateColumns : null,
          headLeft: h ? Math.round(h.getBoundingClientRect().left) : null,
        };
      }),
      residualPlaceholders: document.querySelectorAll('.question-figure-placeholder').length,
      pendingVisible: document.body.innerText.includes('Figure pending'),
      questionCount: document.querySelectorAll('.question-row').length,
      hScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth,
    };
  }, NO_FIG);
}

test('all seven questions survive — the section is the argument, not the figures', async ({ page }) => {
  const r = await probe(page, 1280);
  expect(r.questionCount).toBe(7);
});

test('no placeholder node and no "Figure pending" text remains', async ({ page }) => {
  const r = await probe(page, 1280);
  expect(r.residualPlaceholders).toBe(0);
  expect(r.pendingVisible).toBe(false);
});

test('BUG 1 GUARD: no-figure rows read left-to-right at 1280, including even rows', async ({ page }) => {
  const r = await probe(page, 1280);
  for (const row of r.rows) {
    expect(row.hasClass, `${row.id} missing the class`).toBe(true);
    expect(row.direction, `${row.id} lost the direction override to nth-child(even)`).toBe('ltr');
  }
});

test('BUG 1 GUARD: the three headings share one left edge with the odd text rows', async ({ page }) => {
  const r = await probe(page, 1280);
  const lefts = r.rows.map((x) => x.headLeft);
  expect(new Set(lefts).size, `heading left edges diverged: ${JSON.stringify(lefts)}`).toBe(1);
  const q1Left = await page.evaluate(
    () => Math.round(document.querySelector('#q1 h3').getBoundingClientRect().left));
  expect(lefts[0]).toBe(q1Left);
});

test('BUG 2 GUARD: the 62ch cap does NOT leak into mobile', async ({ page }) => {
  const wide = await probe(page, 1280);
  expect(wide.rows[0].cols).not.toBe('1fr');           // capped on desktop
  const narrow = await probe(page, 768);
  const others = await page.evaluate(
    () => getComputedStyle(document.getElementById('q1')).gridTemplateColumns);
  for (const row of narrow.rows) {
    expect(row.cols, `${row.id} kept the desktop cap at 768`).toBe(others);
  }
});

for (const w of [320, 768, 1280]) {
  test(`no horizontal overflow at ${w}px`, async ({ page }) => {
    const r = await probe(page, w);
    expect(r.hScroll).toBe(false);
  });
}

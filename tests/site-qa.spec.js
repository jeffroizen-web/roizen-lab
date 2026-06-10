// Site-wide QA gate for the canonical Roizen Lab page.
// Covers what the contact-form suite doesn't: console health, broken images,
// CLS (intrinsic dimensions), a11y (alt text + landmarks), and the SEO/JSON-LD
// block added 2026-06-10. Desktop + mobile viewports.
//
// Run: npx playwright test tests/site-qa.spec.js
const { test, expect } = require('@playwright/test');
const { spawn } = require('child_process');

const BASE = 'http://localhost:8767/compare-purple-gold.html';

test.beforeAll(async () => {
  globalThis.__qaServer = spawn('python3', ['-m', 'http.server', '8767'], {
    cwd: __dirname + '/..',
    stdio: 'ignore',
  });
  await new Promise((r) => setTimeout(r, 800));
});

test.afterAll(() => {
  if (globalThis.__qaServer) globalThis.__qaServer.kill();
});

test.describe('Site QA — desktop', () => {
  test('no console errors on load', async ({ page }) => {
    const errors = [];
    page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.goto(BASE, { waitUntil: 'networkidle' });
    expect(errors, `console errors:\n${errors.join('\n')}`).toEqual([]);
  });

  test('all images load (no broken src)', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    // Scroll slowly in small steps so every lazy image intersects the viewport
    // and starts loading (proven sequence: 400px steps, 80ms dwell).
    await page.evaluate(async () => {
      for (let y = 0; y <= document.body.scrollHeight; y += 400) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 80));
      }
    });
    // Let triggered images finish decoding (decode lags network-idle).
    await page.waitForTimeout(2000);
    const broken = await page.evaluate(() =>
      Array.from(document.querySelectorAll('img'))
        .filter((i) => !i.complete || i.naturalWidth === 0)
        .map((i) => i.getAttribute('src'))
    );
    expect(broken, `broken images: ${broken.join(', ')}`).toEqual([]);
  });

  test('every img has explicit width+height (CLS) and alt (a11y)', async ({ page }) => {
    await page.goto(BASE);
    const bad = await page.evaluate(() =>
      Array.from(document.querySelectorAll('img'))
        .filter((i) => !i.getAttribute('width') || !i.getAttribute('height') || i.getAttribute('alt') === null)
        .map((i) => i.getAttribute('src'))
    );
    expect(bad, `imgs missing width/height/alt: ${bad.join(', ')}`).toEqual([]);
  });

  test('semantic landmarks present (nav, main, footer)', async ({ page }) => {
    await page.goto(BASE);
    await expect(page.locator('main')).toHaveCount(1);
    expect(await page.locator('nav').count()).toBeGreaterThan(0);
    expect(await page.locator('footer').count()).toBeGreaterThan(0);
  });

  test('SEO: title, canonical, description, OG, and valid JSON-LD present', async ({ page }) => {
    await page.goto(BASE);
    await expect(page).toHaveTitle(/Roizen Lab/);
    expect(await page.locator('link[rel="canonical"]').getAttribute('href')).toContain('hypothesisdriven.org');
    expect(await page.locator('meta[name="description"]').getAttribute('content')).toBeTruthy();
    expect(await page.locator('meta[property="og:title"]').getAttribute('content')).toBeTruthy();
    const ld = await page.locator('script[type="application/ld+json"]').textContent();
    const data = JSON.parse(ld);
    expect(data['@type']).toBe('ResearchOrganization');
    expect(data.member.name).toBe('Jeffrey Roizen');
  });
});

test.describe('Site QA — mobile (390px)', () => {
  test.use({ viewport: { width: 390, height: 844 } });

  test('no horizontal overflow at 390px', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth
    );
    // allow 1px rounding slack
    expect(overflow, `horizontal overflow of ${overflow}px at 390px`).toBeLessThanOrEqual(1);
  });

  test('nav + hero render on mobile', async ({ page }) => {
    await page.goto(BASE);
    expect(await page.locator('nav').first().isVisible()).toBeTruthy();
    expect(await page.locator('#home').isVisible()).toBeTruthy();
  });
});

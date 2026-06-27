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

test.describe('Site QA — links & nav integrity', () => {
  // The 8 primary-nav anchors are the spine of the page. If one stops resolving
  // (a section id renamed, a link typo'd), navigation silently dead-ends.
  const EXPECTED_NAV = ['#home', '#questions', '#team', '#publications', '#news', '#alumni', '#donate', '#contact'];

  test('every internal anchor link resolves to an element with that id', async ({ page }) => {
    await page.goto(BASE);
    const dangling = await page.evaluate(() =>
      Array.from(document.querySelectorAll('a[href^="#"]'))
        .map((a) => a.getAttribute('href'))
        .filter((h) => h && h.length > 1) // skip a bare "#"
        .filter((h, i, arr) => arr.indexOf(h) === i)
        .filter((h) => !document.getElementById(decodeURIComponent(h.slice(1))))
    );
    expect(dangling, `internal anchors with no target element: ${dangling.join(', ')}`).toEqual([]);
  });

  test('primary nav contains exactly the expected anchors and every target exists', async ({ page }) => {
    await page.goto(BASE);
    const navAnchors = await page.evaluate(() =>
      Array.from(document.querySelectorAll('#primary-nav a[href^="#"]')).map((a) => a.getAttribute('href'))
    );
    expect(navAnchors).toEqual(EXPECTED_NAV);
    for (const href of EXPECTED_NAV) {
      await expect(page.locator(href), `nav target ${href} missing`).toHaveCount(1);
    }
  });

  test('no dead "#" hrefs (donate-live / merch-hidden launch regression guard)', async ({ page }) => {
    await page.goto(BASE);
    // Launch content made the donate button real and removed the merch link; a
    // regressed-to-"#" href is the signature of either being undone.
    const dead = await page.locator('a[href="#"]').count();
    expect(dead, `${dead} dead "#" href(s) present`).toBe(0);
  });

  test('external links are well-formed (format-only; no live fetch — sandbox-safe)', async ({ page }) => {
    await page.goto(BASE);
    const malformed = await page.evaluate(() =>
      Array.from(document.querySelectorAll('a[href]'))
        .map((a) => a.getAttribute('href'))
        .filter((h) => h && !h.startsWith('#'))
        .filter((h) => !(/^https:\/\/[^/]+\.[^/]+/.test(h) || /^mailto:[^@]+@[^@]+\.[^@]+/.test(h)))
    );
    expect(malformed, `malformed external hrefs: ${malformed.join(', ')}`).toEqual([]);
  });

  test('donate button points at a real giving URL (content regression guard)', async ({ page }) => {
    await page.goto(BASE);
    const href = await page.locator('#donate a[href*="giving"]').first().getAttribute('href');
    expect(href, 'donate link should be a live giving.chop.edu URL').toContain('giving.chop.edu');
  });
});

test.describe('Site QA — accessibility depth', () => {
  test('every image has a NON-EMPTY alt (credibility site: figures must describe)', async ({ page }) => {
    await page.goto(BASE);
    // Stricter than the CLS test (which only checks alt !== null): on a science
    // credibility site an alt="" figure is an information hole, not decoration.
    const emptyAlt = await page.evaluate(() =>
      Array.from(document.querySelectorAll('img'))
        .filter((i) => !(i.getAttribute('alt') || '').trim())
        .map((i) => i.getAttribute('src'))
    );
    expect(emptyAlt, `imgs with empty/whitespace alt: ${emptyAlt.join(', ')}`).toEqual([]);
  });

  test('skip-link target (#main-content) exists for keyboard users', async ({ page }) => {
    await page.goto(BASE);
    await expect(page.locator('#main-content')).toHaveCount(1);
  });
});

test.describe('Site QA — JSON-LD validity depth', () => {
  test('ResearchOrganization carries required schema.org fields', async ({ page }) => {
    await page.goto(BASE);
    const blocks = await page.locator('script[type="application/ld+json"]').allTextContents();
    expect(blocks.length, 'exactly one JSON-LD block expected').toBe(1);
    const data = JSON.parse(blocks[0]);
    expect(data['@context']).toBe('https://schema.org');
    expect(data['@type']).toBe('ResearchOrganization');
    expect(data.url).toContain('hypothesisdriven.org');
    expect(data.description, 'description must be non-empty').toBeTruthy();
    // parentOrganization must name both CHOP and Penn (the institution bar truth).
    const parents = JSON.stringify(data.parentOrganization || []);
    expect(parents).toContain('Pennsylvania');
    expect(parents).toContain('Children');
    expect(data.member.name).toBe('Jeffrey Roizen');
    expect(Array.isArray(data.member.affiliation), 'member.affiliation should be an array').toBeTruthy();
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

test.describe('Site QA — tablet breakpoint (768px)', () => {
  // lab-website.md pins the mobile breakpoint at 768px — the exact edge where the
  // desktop/mobile layout switch happens, so it's the most regression-prone width.
  test.use({ viewport: { width: 768, height: 1024 } });

  test('no horizontal overflow at the 768px breakpoint', async ({ page }) => {
    await page.goto(BASE, { waitUntil: 'networkidle' });
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth
    );
    expect(overflow, `horizontal overflow of ${overflow}px at 768px`).toBeLessThanOrEqual(1);
  });

  test('nav + hero render at 768px', async ({ page }) => {
    await page.goto(BASE);
    expect(await page.locator('nav').first().isVisible()).toBeTruthy();
    expect(await page.locator('#home').isVisible()).toBeTruthy();
  });
});

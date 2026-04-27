// Contact form integration tests
// Run: cd "Roizen Lab" && npx playwright test tests/contact-form.spec.js
//
// Prerequisites: npx playwright install chromium (one-time)
// These tests start a local HTTP server automatically.

const { test, expect } = require('@playwright/test');
const { spawn } = require('child_process');

const BASE = 'http://localhost:8766/compare-purple-gold.html';

test.describe('Contact Form', () => {

  test.beforeAll(async () => {
    // Start local server (port 8766 to avoid conflicts)
    globalThis.__server = spawn('python3', ['-m', 'http.server', '8766'], {
      cwd: __dirname + '/..',
      stdio: 'ignore'
    });
    await new Promise(r => setTimeout(r, 1000));
  });

  test.afterAll(async () => {
    if (globalThis.__server) globalThis.__server.kill();
  });

  test('has all required form fields with labels', async ({ page }) => {
    await page.goto(BASE + '#contact');
    const form = page.locator('#contact-form');
    await expect(form).toBeVisible();

    await expect(page.locator('label[for="contact-name"]')).toHaveText('Name');
    await expect(page.locator('label[for="contact-email"]')).toHaveText('Email');
    await expect(page.locator('label[for="contact-subject"]')).toHaveText('Subject');
    await expect(page.locator('label[for="contact-message"]')).toHaveText('Message');

    await expect(page.locator('#contact-name')).toHaveAttribute('required', '');
    await expect(page.locator('#contact-email')).toHaveAttribute('required', '');
    await expect(page.locator('#contact-subject')).toHaveAttribute('required', '');
    await expect(page.locator('#contact-message')).toHaveAttribute('required', '');

    await expect(page.locator('.contact-submit')).toBeVisible();
    await expect(page.locator('.contact-submit')).toHaveText('Send');
  });

  test('honeypot field is hidden from users', async ({ page }) => {
    await page.goto(BASE + '#contact');
    const honeypot = page.locator('.honeypot');
    await expect(honeypot).toHaveAttribute('aria-hidden', 'true');
    // Honeypot is positioned offscreen (-9999px), not display:none
    const box = await honeypot.boundingBox();
    expect(box.x).toBeLessThan(0);
  });

  test('status region has aria-live for screen readers', async ({ page }) => {
    await page.goto(BASE + '#contact');
    const status = page.locator('#contact-status');
    await expect(status).toHaveAttribute('role', 'status');
    await expect(status).toHaveAttribute('aria-live', 'polite');
  });

  test('shows not-configured error when FORMSPREE_ID_HERE is in action', async ({ page }) => {
    await page.goto(BASE + '#contact');

    await page.fill('#contact-name', 'Test User');
    await page.fill('#contact-email', 'test@example.com');
    await page.fill('#contact-subject', 'Test Subject');
    await page.fill('#contact-message', 'Test message body');

    await page.click('.contact-submit');
    await page.waitForTimeout(300);

    const status = page.locator('#contact-status');
    await expect(status).toContainText('not configured');
    await expect(status).toContainText('jeffroizen@gmail.com');
    await expect(status).toHaveClass(/error/);
  });

  test('adds was-submitted class on submit attempt', async ({ page }) => {
    await page.goto(BASE + '#contact');
    const form = page.locator('#contact-form');

    await expect(form).not.toHaveClass(/was-submitted/);
    await page.click('.contact-submit');
    await page.waitForTimeout(200);
    await expect(form).toHaveClass(/was-submitted/);
  });

  test('happy path: mocked Formspree 200 shows success', async ({ page }) => {
    await page.goto(BASE + '#contact');

    await page.route('**/formspree.io/**', route => {
      route.fulfill({ status: 200, contentType: 'application/json', body: '{"ok":true}' });
    });
    await page.route('**/ntfy.sh/**', route => {
      route.fulfill({ status: 200, body: '' });
    });

    await page.evaluate(() => {
      document.getElementById('contact-form').setAttribute('action', 'https://formspree.io/f/test1234');
    });

    await page.fill('#contact-name', 'Test User');
    await page.fill('#contact-email', 'test@example.com');
    await page.fill('#contact-subject', 'Test Subject');
    await page.fill('#contact-message', 'Test message body');
    await page.click('.contact-submit');

    await page.waitForTimeout(1000);

    const status = page.locator('#contact-status');
    await expect(status).toContainText('Thanks');
    await expect(status).toHaveClass(/success/);

    // Form should be reset after success
    await expect(page.locator('#contact-name')).toHaveValue('');
    await expect(page.locator('#contact-email')).toHaveValue('');
  });

  test('error path: mocked Formspree 422 shows error with fallback email', async ({ page }) => {
    await page.goto(BASE + '#contact');

    await page.route('**/formspree.io/**', route => {
      route.fulfill({
        status: 422,
        contentType: 'application/json',
        body: JSON.stringify({ errors: [{ message: 'Email not verified' }] })
      });
    });
    await page.route('**/ntfy.sh/**', route => {
      route.fulfill({ status: 200, body: '' });
    });

    await page.evaluate(() => {
      document.getElementById('contact-form').setAttribute('action', 'https://formspree.io/f/test1234');
    });

    await page.fill('#contact-name', 'Test User');
    await page.fill('#contact-email', 'test@example.com');
    await page.fill('#contact-subject', 'Test Subject');
    await page.fill('#contact-message', 'Test message body');
    await page.click('.contact-submit');

    await page.waitForTimeout(1000);

    const status = page.locator('#contact-status');
    await expect(status).toContainText('Email not verified');
    await expect(status).toContainText('jeffroizen@gmail.com');
    await expect(status).toHaveClass(/error/);

    // Form should NOT be reset on error
    await expect(page.locator('#contact-name')).toHaveValue('Test User');
  });

  test('network error shows fallback email', async ({ page }) => {
    await page.goto(BASE + '#contact');

    await page.route('**/formspree.io/**', route => {
      route.abort('connectionrefused');
    });
    await page.route('**/ntfy.sh/**', route => {
      route.abort('connectionrefused');
    });

    await page.evaluate(() => {
      document.getElementById('contact-form').setAttribute('action', 'https://formspree.io/f/test1234');
    });

    await page.fill('#contact-name', 'Test User');
    await page.fill('#contact-email', 'test@example.com');
    await page.fill('#contact-subject', 'Test Subject');
    await page.fill('#contact-message', 'Test message body');
    await page.click('.contact-submit');

    await page.waitForTimeout(1000);

    const status = page.locator('#contact-status');
    await expect(status).toContainText('Network error');
    await expect(status).toContainText('jeffroizen@gmail.com');
    await expect(status).toHaveClass(/error/);
  });

  test('submit button re-enables after error', async ({ page }) => {
    await page.goto(BASE + '#contact');

    await page.route('**/formspree.io/**', route => {
      route.abort('connectionrefused');
    });
    await page.route('**/ntfy.sh/**', route => {
      route.abort('connectionrefused');
    });

    await page.evaluate(() => {
      document.getElementById('contact-form').setAttribute('action', 'https://formspree.io/f/test1234');
    });

    await page.fill('#contact-name', 'Test User');
    await page.fill('#contact-email', 'test@example.com');
    await page.fill('#contact-subject', 'Test Subject');
    await page.fill('#contact-message', 'Test message body');
    await page.click('.contact-submit');

    await page.waitForTimeout(1000);
    await expect(page.locator('.contact-submit')).toBeEnabled();
  });

  test('ntfy receives correct payload on happy path', async ({ page }) => {
    await page.goto(BASE + '#contact');

    let ntfyBody = null;
    let ntfyHeaders = null;

    await page.route('**/formspree.io/**', route => {
      route.fulfill({ status: 200, contentType: 'application/json', body: '{"ok":true}' });
    });
    await page.route('**/ntfy.sh/**', route => {
      ntfyBody = route.request().postData();
      ntfyHeaders = route.request().headers();
      route.fulfill({ status: 200, body: '' });
    });

    await page.evaluate(() => {
      document.getElementById('contact-form').setAttribute('action', 'https://formspree.io/f/test1234');
    });

    await page.fill('#contact-name', 'Dr. Smith');
    await page.fill('#contact-email', 'smith@example.com');
    await page.fill('#contact-subject', 'Collaboration inquiry');
    await page.fill('#contact-message', 'I would like to discuss...');
    await page.click('.contact-submit');

    await page.waitForTimeout(1000);

    expect(ntfyBody).toContain('Dr. Smith');
    expect(ntfyBody).toContain('Collaboration inquiry');
    expect(ntfyHeaders['title']).toBe('Roizen Lab contact');
  });

  test('mobile: form renders correctly at 390px', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(BASE + '#contact');

    const form = page.locator('#contact-form');
    await expect(form).toBeVisible();

    await expect(page.locator('#contact-name')).toBeVisible();
    await expect(page.locator('#contact-email')).toBeVisible();
    await expect(page.locator('#contact-subject')).toBeVisible();
    await expect(page.locator('#contact-message')).toBeVisible();
    await expect(page.locator('.contact-submit')).toBeVisible();

    const formBox = await form.boundingBox();
    expect(formBox.width).toBeLessThanOrEqual(390);
  });
});

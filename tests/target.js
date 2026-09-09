// Shared target resolution for the Playwright suites.
//
// WHY THIS EXISTS (2026-09-08): I offered Rams my 38 Playwright tests as a
// regression net against the PREVIEW surface after its figure-pending change
// lands — then checked whether that offer was executable and found it was not.
// Every spec hardcoded `http://localhost:<port>/compare-purple-gold.html`, so
// the suite could only ever test the local working copy. The offer was inert:
// a capability promised without verifying it existed, which is the same class
// this fleet spent the night finding in seals, gates and archive pointers.
//
// USAGE
//   npx playwright test                        -> local working copy (unchanged)
//   ROIZEN_QA_TARGET=<url> npx playwright test -> that URL, no local server
//
// e.g. ROIZEN_QA_TARGET=https://jeffroizen-web.github.io/roizen-lab/preview/redesign/
//
// DEFAULT BEHAVIOUR IS BYTE-UNCHANGED when the env var is unset: same ports,
// same spawned server, same URL. A remote target skips the spawn entirely,
// because starting a local http.server while pointing the browser at a public
// URL would be a silent no-op that looks like it worked.

const { spawn } = require('child_process');

function resolveTarget(localPort) {
  const override = (process.env.ROIZEN_QA_TARGET || '').trim();
  if (override) {
    return { base: override, remote: true };
  }
  return {
    base: `http://localhost:${localPort}/compare-purple-gold.html`,
    remote: false,
  };
}

// Starts the local static server ONLY for a local target. Returns the child
// process, or null when remote. Pair with stopServer in afterAll.
async function startServer(localPort, remote, waitMs = 900) {
  if (remote) return null;
  const proc = spawn('python3', ['-m', 'http.server', String(localPort)], {
    cwd: __dirname + '/..',
    stdio: 'ignore',
  });
  await new Promise((r) => setTimeout(r, waitMs));
  return proc;
}

function stopServer(proc) {
  if (proc) proc.kill();
}


// Wait until every <img> that will affect layout has actually resolved.
//
// WHY (Rams, 2026-09-08): `waitUntil: 'networkidle'` is NOT enough on this page.
// The canonical carries 11 loading="lazy" images, and on a cold load Rams
// measured .questions-list at 2198px at networkidle against a settled 2459px —
// a 261px error, and a THIRD number matching neither of two people already
// disagreeing. Settled values are deterministic across runs; the variance comes
// entirely from reading too early. Any assertion about geometry must wait for
// this, or it is measuring a page mid-construction and will flake or, worse,
// pass against the wrong layout.
//
// Pairs with the other half of the discipline: quote the SELECTOR with the
// number. Either alone still lets two correct measurements read as a conflict.
async function settleImages(page, timeout = 5000) {
  // Force lazy images into view so they actually begin loading, then wait.
  await page.evaluate(() => {
    for (const img of document.querySelectorAll('img[loading="lazy"]')) {
      img.loading = 'eager';
      if (!img.complete && img.src) { const s = img.src; img.src = ''; img.src = s; }
    }
  });
  await page.waitForFunction(
    () => [...document.images].every((i) => i.complete && (i.naturalWidth > 0 || i.src === '')),
    null,
    { timeout }
  ).catch(() => { /* never block a run on one broken asset — geometry tests assert their own facts */ });
}

module.exports = { resolveTarget, startServer, stopServer, settleImages };

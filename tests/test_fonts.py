"""Self-hosted font guard for the Roizen Lab site (font-perf-fix, 2026-06-27).

The site previously loaded 4 families from https://fonts.googleapis.com via a
render-blocking external stylesheet — which also made the network-restricted
test sandbox's "no console errors" check flap. Fonts are now self-hosted
(latin-subset variable woff2 in fonts/, @font-face inlined in <style>).

These static guards lock that in:
- no external Google Fonts reference may return (regression to the render-
  blocking / sandbox-failing setup),
- every @font-face src and every font preload must resolve to a file on disk.

Runtime load (no 404, no external font request) is verified separately by the
Playwright test in tests/site-qa.spec.js.

Run: python3 -m pytest tests/test_fonts.py -q
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = (ROOT / "compare-purple-gold.html").read_text()


def test_no_external_google_fonts():
    for needle in ("fonts.googleapis.com", "fonts.gstatic.com"):
        assert needle not in HTML, f"external font reference {needle!r} regressed (should be self-hosted)"


def test_font_face_files_exist():
    srcs = re.findall(r"@font-face\{[^}]*src:url\('([^']+)'\)", HTML)
    assert len(srcs) >= 4, f"expected >=4 @font-face rules, found {len(srcs)}"
    missing = [s for s in srcs if not (ROOT / s).exists()]
    assert not missing, f"@font-face src files missing on disk: {missing}"


def test_preloaded_fonts_exist_and_are_woff2():
    preloads = re.findall(r'<link rel="preload" href="([^"]+)" as="font"[^>]*>', HTML)
    assert preloads, "no font preloads found (expected merriweather + open-sans above-the-fold)"
    for href in preloads:
        assert href.endswith(".woff2"), f"font preload is not woff2: {href}"
        assert (ROOT / href).exists(), f"preloaded font missing on disk: {href}"
        assert "crossorigin" in HTML.split(href)[1][:60], f"font preload {href} missing crossorigin (causes double-fetch)"


def test_all_themed_families_have_a_face():
    """Both themes' fonts must be self-hosted: purple-gold uses Merriweather +
    Open Sans, warm-slate uses Playfair Display + Inter."""
    families = set(re.findall(r"@font-face\{font-family:'([^']+)'", HTML))
    for fam in ("Merriweather", "Open Sans", "Inter", "Playfair Display"):
        assert fam in families, f"{fam} has no self-hosted @font-face"

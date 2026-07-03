#!/usr/bin/env python3
"""Publications-feed wiring guard (Inc-1 / R1, 2026-07-03).

The Archivist feed is counter-signed and wired into the served HTML at build
time by scripts/wire_publications.py. These lock the contract:
- the served HTML carries the fresh feed block (count + data_as_of stamp), not
  the old hand-typed "27 publications" literal,
- re-wiring is byte-stable (idempotent — safe for a refresh cron),
- a >14d-stale feed renders a LOUD banner (never a silent snapshot),
- a missing feed falls back to a notice + leaves the curated showcase intact,
- publication titles are in the served markup (SEO / build-time render).

Run: python3 -m pytest tests/test_publications_wire.py -q
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import wire_publications as wp  # noqa: E402

LIVE_HTML = (ROOT / "compare-purple-gold.html").read_text(encoding="utf-8")

_MIN_SECTION = (
    '<html><head><style>:root{}</style></head><body>'
    '<section id="publications" class="section"><div class="container">'
    '<h2>Selected Papers</h2><div class="pub-list">curated showcase</div>'
    "</div></section></body></html>"
)


def _feed(as_of_iso, pubs):
    return {"data_as_of": as_of_iso, "fetched_from": "test", "publications": pubs}


def _pub(pmid="1", arc="phenotype", **kw):
    base = {"pmid": pmid, "title": f"Title {pmid}", "authors": ["Roizen JD"],
            "venue": "J Test", "year": 2025, "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "research_arc": arc, "first_author": True, "senior_author": False}
    base.update(kw)
    return base


def _write_feed(tmp_path, payload):
    p = tmp_path / "publications.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return p


# ---- live served HTML (the actual wired state) --------------------------------

def test_live_html_has_feed_block_not_stale_literal():
    assert wp.SENTINEL_OPEN in LIVE_HTML, "publications-feed block missing from served HTML"
    assert "27 publications" not in LIVE_HTML, "stale hand-typed '27 publications' literal still present"
    assert "publications-feed-styles" in LIVE_HTML, "feed styles not injected"


def test_live_html_carries_provenance_stamp():
    # A data_as_of stamp + count must be in the served markup (Data Provenance).
    assert "Complete list —" in LIVE_HTML
    assert "publications, verified" in LIVE_HTML
    import re
    assert re.search(r"verified \d{4}-\d{2}-\d{2}", LIVE_HTML), "no ISO data_as_of stamp"


# ---- wiring behaviour ---------------------------------------------------------

def test_fresh_feed_renders_count_and_titles(tmp_path):
    feed = _write_feed(tmp_path, _feed(
        datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        [_pub("111", title="Vitamin D flagship"), _pub("222", arc="mechanism")]))
    out = wp.wire(_MIN_SECTION, feed)
    assert "2 publications, verified" in out
    assert "Vitamin D flagship" in out, "titles must be in served markup (SEO)"
    assert wp.SENTINEL_OPEN in out and wp.SENTINEL_CLOSE in out


def test_rewire_is_byte_stable(tmp_path):
    """Idempotency: wiring twice must be byte-identical (safe for a refresh cron)."""
    feed = _write_feed(tmp_path, _feed(
        datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        [_pub("111"), _pub("222", arc="mechanism")]))
    once = wp.wire(_MIN_SECTION, feed)
    twice = wp.wire(once, feed)
    assert once == twice, "re-wiring changed bytes — not idempotent"


def test_stale_feed_renders_loud_banner(tmp_path):
    old = (datetime.now(timezone.utc) - timedelta(days=40)).isoformat().replace("+00:00", "Z")
    feed = _write_feed(tmp_path, _feed(old, [_pub("111")]))
    out = wp.wire(_MIN_SECTION, feed)
    assert "freshness-banner" in out, "a >14d-stale feed must render the loud staleness banner"
    assert "verified through" in out


def test_missing_feed_falls_back_and_keeps_showcase(tmp_path):
    out = wp.wire(_MIN_SECTION, tmp_path / "does-not-exist.json")
    assert "freshness-banner" in out and "temporarily unavailable" in out
    assert "curated showcase" in out, "the curated showcase must remain on feed failure"
    assert wp.SENTINEL_OPEN in out


def _contrast(fg, bg):
    def lum(rgb):
        def f(c):
            c /= 255
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        r, g, b = rgb
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def test_badge_contrast_meets_wcag_aa_on_gold_tint():
    """Author badge is normal-size text → needs AA 4.5:1. --accent-dark was 4.43
    (FAIL) on the gold tint; --primary is 11.59 (WEB-QUALITY gate, 2026-07-03).
    Guard the generator AND the served HTML use the AA-passing token."""
    import re
    for src, name in ((wp.STYLE_BLOCK, "generator"), (LIVE_HTML, "served HTML")):
        rule = re.search(r"\.pub-feed \.pub-badge \{[^}]*\}", src)
        assert rule, f"pub-badge rule not found in {name}"
        assert "var(--primary)" in rule.group(0), f"badge not --primary in {name}"
        assert "var(--accent-dark)" not in rule.group(0), f"badge still --accent-dark in {name}"
    # Computed: --primary (#3B1F6E) on rgba(197,163,54,0.15)-over-white must clear AA.
    tint = tuple(0.15 * c + 0.85 * 255 for c in (197, 163, 54))
    assert _contrast((0x3B, 0x1F, 0x6E), tint) >= 4.5


def test_styles_inject_into_real_style_tag_not_a_comment(tmp_path):
    """Regression guard (2026-07-03): the style regex must target a REAL <style>
    element, not a '<style' substring inside an HTML comment (which buries the CSS
    in the comment, unparsed). Assert the injected styles land inside a <style>."""
    html = (
        "<html><head>"
        "<!-- @font-face inlined in <style> below -->"  # decoy <style substring
        "<style>:root{}</style>"
        "</head><body>"
        '<section id="publications"><div class="pub-list">x</div></section>'
        "</body></html>"
    )
    out = wp.ensure_style_block(html)
    idx = out.index(wp.STYLE_SENTINEL)
    open_before = out.rfind("<style>", 0, idx)
    close_before = out.rfind("</style>", 0, idx)
    # The sentinel must sit AFTER a real <style> open and NOT after a </style>
    # (i.e. genuinely inside the style element), and not inside the comment.
    assert open_before != -1 and open_before > out.index("-->"), \
        "styles injected before/into the comment, not into the real <style>"
    assert close_before < open_before, "styles injected outside a <style> element"


def test_empty_feed_falls_back(tmp_path):
    feed = _write_feed(tmp_path, _feed(
        datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), []))
    out = wp.wire(_MIN_SECTION, feed)
    assert "temporarily unavailable" in out or "could not be parsed" in out

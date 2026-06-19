#!/usr/bin/env python3
"""
Tests for scripts/wire_letter_writers.py

Run: python3 -m unittest tests.test_wire_letter_writers -v
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from wire_letter_writers import (  # noqa: E402
    build_paragraph,
    inject_record,
    strip_existing_foi,
    ensure_style_block,
    wire,
    SENTINEL_OPEN,
    SENTINEL_CLOSE,
    STYLE_SENTINEL,
)


def site_card(name: str, role: str = "Some Role") -> str:
    return f"""
    <div style="text-align:center;">
        <h3><a href="https://example.com/x" target="_blank">{name}</a></h3>
        <p style="color:var(--accent-dark);">{role}</p>
        <p style="color:var(--text-light);">University X</p>
    </div>
    """


def site_with_style(*cards):
    return "<html><head><style>:root{--primary:#3B1F6E;}</style></head><body>" + "".join(cards) + "</body></html>"


def make_record(name, conf=1.0, terms=None, pmids=10):
    return {
        "name": name,
        "confidence": conf,
        "field_terms": terms or ["vitamin", "asthma", "bone"],
        "recent_pmids": [str(i) for i in range(pmids)],
    }


class TestBuildParagraph(unittest.TestCase):
    def test_high_conf_paragraph_has_terms_and_pub_count(self):
        p = build_paragraph(make_record("Dr X", conf=0.9, terms=["alpha", "beta"], pmids=7))
        self.assertIn("alpha", p)
        self.assertIn("beta", p)
        self.assertIn("7 recent pubs", p)
        self.assertNotIn("low-conf", p)
        self.assertIn(SENTINEL_OPEN, p)
        self.assertIn(SENTINEL_CLOSE, p)

    def test_low_conf_paragraph_marked_verifying(self):
        p = build_paragraph(make_record("Dr Y", conf=0.4, terms=["gamma"], pmids=2))
        self.assertIn("low-conf", p)
        self.assertIn("verifying", p.lower())
        self.assertIn("gamma", p)

    def test_low_conf_with_no_terms_still_safe(self):
        p = build_paragraph(make_record("Dr Z", conf=0.2, terms=[], pmids=0))
        self.assertIn("low-conf", p)
        self.assertIn("verifying", p.lower())

    def test_escapes_quote_in_name(self):
        p = build_paragraph(make_record('Dr "Quoted" X', conf=0.9))
        self.assertNotIn('data-name="Dr "Quoted" X"', p)
        self.assertIn("&quot;", p)


class TestInject(unittest.TestCase):
    def test_injects_after_role_paragraph(self):
        html = site_card("Louis J. Muglia, MD, PhD", role="President")
        new_html, did = inject_record(html, make_record("Louis J. Muglia, MD, PhD"))
        self.assertTrue(did)
        self.assertIn("field-of-interest", new_html)
        self.assertGreater(new_html.index("field-of-interest"), new_html.index("President"))

    def test_no_match_returns_unchanged(self):
        html = site_card("Other Person")
        new_html, did = inject_record(html, make_record("Missing Name"))
        self.assertFalse(did)
        self.assertEqual(html, new_html)

    def test_idempotent_strip_and_reinject(self):
        html = site_card("Dr X")
        first, _ = inject_record(html, make_record("Dr X", terms=["foo"]))
        second, _ = inject_record(first, make_record("Dr X", terms=["bar"]))
        # The second injection should remove the first foi and inject bar
        self.assertNotIn("foo", second)
        self.assertIn("bar", second)
        # And only one foi block remains
        self.assertEqual(second.count(SENTINEL_OPEN), 1)

    def test_reinject_same_record_is_byte_stable(self):
        # Regression: cron ran daily and orphaned a "\n<indent>" run each time,
        # accumulating blank lines in the canonical file (found 2026-06-18, 7 runs deep).
        # Re-injecting the SAME record must be a fixed point — byte-identical, no growth.
        html = site_card("Dr X")
        once, _ = inject_record(html, make_record("Dr X", terms=["foo"]))
        twice, _ = inject_record(once, make_record("Dr X", terms=["foo"]))
        self.assertEqual(once, twice, "re-injecting identical record must be byte-stable")

    def test_repeated_inject_does_not_grow_blank_lines(self):
        html = site_card("Dr X")
        cur = html
        blank_counts = []
        for _ in range(5):
            cur, _ = inject_record(cur, make_record("Dr X", terms=["foo"]))
            blank_counts.append(sum(1 for L in cur.splitlines() if L.strip() == ""))
        self.assertEqual(len(set(blank_counts)), 1, f"blank lines grew across runs: {blank_counts}")

    def test_does_not_double_inject(self):
        html = site_card("Dr X")
        once, _ = inject_record(html, make_record("Dr X"))
        twice, _ = inject_record(once, make_record("Dr X"))
        self.assertEqual(twice.count(SENTINEL_OPEN), 1)


class TestStripExistingFoi(unittest.TestCase):
    def test_strips_only_named_record(self):
        html = (
            site_card("Dr X")
            + f'{SENTINEL_OPEN}<p class="field-of-interest" data-name="Dr X" data-conf="0.9">x</p>{SENTINEL_CLOSE}'
            + f'{SENTINEL_OPEN}<p class="field-of-interest" data-name="Dr Y" data-conf="0.9">y</p>{SENTINEL_CLOSE}'
        )
        stripped = strip_existing_foi(html, "Dr X")
        self.assertNotIn('data-name="Dr X"', stripped)
        self.assertIn('data-name="Dr Y"', stripped)

    def test_no_match_returns_unchanged(self):
        html = "<p>no foi here</p>"
        self.assertEqual(strip_existing_foi(html, "Dr Whoever"), html)


class TestEnsureStyleBlock(unittest.TestCase):
    def test_injects_style_once(self):
        html = "<html><head><style>:root{--primary:#000;}</style></head></html>"
        once = ensure_style_block(html)
        twice = ensure_style_block(once)
        self.assertEqual(once.count(STYLE_SENTINEL), 1)
        self.assertEqual(twice.count(STYLE_SENTINEL), 1)

    def test_no_style_block_returns_unchanged(self):
        html = "<html><body>no style</body></html>"
        self.assertEqual(ensure_style_block(html), html)


class TestWireEndToEnd(unittest.TestCase):
    def test_multi_person_injection(self):
        html = site_with_style(
            site_card("Dr A", role="Prof A"),
            site_card("Dr B", role="Prof B"),
        )
        data = {"records": [
            make_record("Dr A", terms=["alpha"]),
            make_record("Dr B", conf=0.3, terms=["beta"]),
        ]}
        new_html, n, missing = wire(html, data)
        self.assertEqual(n, 2)
        self.assertEqual(missing, [])
        self.assertIn("alpha", new_html)
        self.assertIn("beta", new_html)
        self.assertIn("low-conf", new_html)
        self.assertIn(STYLE_SENTINEL, new_html)

    def test_records_with_no_matching_card_reported_as_missing(self):
        html = site_with_style(site_card("Only Dr A"))
        data = {"records": [
            make_record("Only Dr A"),
            make_record("Dr Ghost"),
        ]}
        _, n, missing = wire(html, data)
        self.assertEqual(n, 1)
        self.assertEqual(missing, ["Dr Ghost"])


class TestLiveSite(unittest.TestCase):
    def test_can_inject_into_real_site_dry(self):
        site = ROOT / "compare-purple-gold.html"
        data_path = ROOT / "docs" / "letter_writers.json"
        if not site.exists() or not data_path.exists():
            self.skipTest("live site or data missing")
        import json
        html = site.read_text(encoding="utf-8")
        data = json.loads(data_path.read_text(encoding="utf-8"))
        new_html, n, missing = wire(html, data)
        self.assertGreater(n, 0, "should inject at least one foi into the real site")


if __name__ == "__main__":
    unittest.main(verbosity=2)

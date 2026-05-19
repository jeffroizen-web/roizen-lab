#!/usr/bin/env python3
"""
Tests for scripts/tenure_readiness.py

Run: python3 -m unittest tests.test_tenure_readiness -v
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from tenure_readiness import scan, diff, Findings  # noqa: E402


def html(body: str, head: str = "") -> str:
    return f"<!DOCTYPE html><html><head>{head}</head><body>{body}</body></html>"


class TestScan(unittest.TestCase):
    def test_dead_hash_href_caught(self):
        f = scan(html('<a href="#">Read the paper</a>'))
        self.assertEqual(len(f.dead_hash_hrefs), 1)
        self.assertIn("Read the paper", f.dead_hash_hrefs[0])

    def test_donate_hash_href_ignored(self):
        f = scan(html('<a href="#">Donate to the Lab</a>'))
        self.assertEqual(f.dead_hash_hrefs, [])

    def test_figure_pending_counted(self):
        body = (
            '<div class="question-row" id="q1"><div class="question-text"></div>'
            '<div class="question-figure question-figure-placeholder"></div></div>'
            '<div class="question-row" id="q2"><div class="question-text"></div>'
            '<div class="question-figure"><img src="real.png" alt="real"></div></div>'
        )
        f = scan(html(body))
        self.assertEqual(f.figure_pending_count, 1)
        self.assertEqual(f.figure_pending_ids, ["q1"])

    def test_img_missing_alt_caught(self):
        f = scan(html('<img src="foo.png">'))
        self.assertEqual(f.img_missing_alt, ["foo.png"])

    def test_img_with_alt_passes(self):
        f = scan(html('<img src="foo.png" alt="A foo">'))
        self.assertEqual(f.img_missing_alt, [])

    def test_svg_excluded_from_dimensions_check(self):
        f = scan(html('<img src="logo.svg" alt="logo">'))
        self.assertEqual(f.imgs_missing_dimensions, [])

    def test_png_without_dimensions_caught(self):
        f = scan(html('<img src="foo.png" alt="foo">'))
        self.assertEqual(f.imgs_missing_dimensions, ["foo.png"])

    def test_png_with_dimensions_passes(self):
        f = scan(html('<img src="foo.png" alt="foo" width="100" height="50">'))
        self.assertEqual(f.imgs_missing_dimensions, [])

    def test_skip_link_detected(self):
        f = scan(html('<a href="#main-content" class="skip-link">Skip</a>'))
        self.assertTrue(f.has_skip_link)

    def test_main_landmark_detected(self):
        f = scan(html('<main id="main-content"></main>'))
        self.assertTrue(f.has_main_landmark)

    def test_pi_funding_signal_detected(self):
        f = scan(html('<p>NIH-funded · 27 publications</p>'))
        self.assertTrue(f.has_pi_funding_signal)

    def test_pi_funding_signal_missing(self):
        f = scan(html('<p>Assistant Professor</p>'))
        self.assertFalse(f.has_pi_funding_signal)

    def test_banned_phrase_caught(self):
        f = scan(html('<p>We are fortunate to work with great scientists.</p>'))
        self.assertIn("fortunate to work with", f.banned_phrases_found)

    def test_clean_html_no_banned_phrases(self):
        f = scan(html('<p>Scientists we talk to.</p>'))
        self.assertEqual(f.banned_phrases_found, [])


class TestGrade(unittest.TestCase):
    def test_clean_site_gets_a(self):
        f = Findings(
            has_skip_link=True,
            has_main_landmark=True,
            has_pi_funding_signal=True,
        )
        self.assertEqual(f.grade(), "A")

    def test_pending_figures_drops_to_a_minus(self):
        f = Findings(
            has_skip_link=True,
            has_main_landmark=True,
            has_pi_funding_signal=True,
            figure_pending_count=2,
            figure_pending_ids=["q2", "q3"],
        )
        self.assertEqual(f.grade(), "A-")

    def test_missing_funding_signal_drops_grade(self):
        f = Findings(
            has_skip_link=True,
            has_main_landmark=True,
            has_pi_funding_signal=False,
        )
        self.assertIn(f.grade(), ("B", "C"))

    def test_multiple_failures_gets_c(self):
        f = Findings(
            dead_hash_hrefs=["x", "y"],
            banned_phrases_found=["leverage", "synergy"],
            img_missing_alt=["foo.png"],
        )
        self.assertEqual(f.grade(), "C")


class TestDiff(unittest.TestCase):
    def test_no_changes_no_regressions(self):
        old = {"dead_hash_hrefs": ["a"], "banned_phrases_found": []}
        new = {"dead_hash_hrefs": ["a"], "banned_phrases_found": []}
        self.assertEqual(diff(old, new), [])

    def test_new_issue_is_regression(self):
        old = {"dead_hash_hrefs": []}
        new = {"dead_hash_hrefs": ["new dead link"]}
        regressions = diff(old, new)
        self.assertEqual(len(regressions), 1)
        self.assertEqual(regressions[0]["field"], "dead_hash_hrefs")
        self.assertEqual(regressions[0]["new_issues"], ["new dead link"])

    def test_resolved_issue_is_not_regression(self):
        old = {"dead_hash_hrefs": ["old issue"]}
        new = {"dead_hash_hrefs": []}
        self.assertEqual(diff(old, new), [])

    def test_scalar_fields_ignored(self):
        old = {"has_skip_link": True}
        new = {"has_skip_link": False}
        self.assertEqual(diff(old, new), [])


class TestLiveSite(unittest.TestCase):
    """Smoke test against the actual working file."""

    def test_live_site_scans_without_error(self):
        site = ROOT / "compare-purple-gold.html"
        if not site.exists():
            self.skipTest("working file missing")
        text = site.read_text(encoding="utf-8")
        f = scan(text)
        self.assertGreater(f.total_imgs, 0, "should find at least one img")
        self.assertTrue(f.has_main_landmark, "live site should have <main id=main-content>")
        self.assertTrue(f.has_skip_link, "live site should have skip link")


if __name__ == "__main__":
    unittest.main(verbosity=2)

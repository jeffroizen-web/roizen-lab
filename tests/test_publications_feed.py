#!/usr/bin/env python3
"""
Consumer-side contract tests for the publications feed.

Contract: docs/contracts/archivist-publications.md
Run: python3 -m unittest tests.test_publications_feed -v
"""
import json
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from publications_feed import (  # noqa: E402
    parse_feed,
    load_feed,
    render_html,
    Publication,
    FeedResult,
)


def valid_pub(**overrides):
    pub = {
        "pmid": "12345678",
        "title": "Example title",
        "authors": ["Roizen JD", "Other A"],
        "venue": "J Clin Endocrinol Metab",
        "year": 2025,
        "pubmed_url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
        "research_arc": "phenotype",
        "publication_date": "2025-08-14",
        "doi": "10.1210/clinem/dgae123",
        "first_author": False,
        "senior_author": True,
        "open_access": True,
    }
    pub.update(overrides)
    return pub


def envelope(*pubs, data_as_of=None):
    return {
        "data_as_of": data_as_of or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "fetched_from": "ncbi_mybibliography_50863673",
        "publications": list(pubs),
    }


class TestParseFeed(unittest.TestCase):
    def test_valid_publication_parsed(self):
        result = parse_feed(envelope(valid_pub()))
        self.assertEqual(len(result.publications), 1)
        self.assertEqual(result.publications[0].pmid, "12345678")
        self.assertEqual(result.dropped_count, 0)

    def test_missing_required_field_drops_publication(self):
        bad = valid_pub()
        del bad["title"]
        result = parse_feed(envelope(bad))
        self.assertEqual(len(result.publications), 0)
        self.assertEqual(result.dropped_count, 1)
        self.assertTrue(any("missing" in r and "title" in r for r in result.dropped_reasons))

    def test_unknown_arc_falls_back_to_other(self):
        result = parse_feed(envelope(valid_pub(research_arc="weird")))
        self.assertEqual(len(result.publications), 1)
        self.assertEqual(result.publications[0].research_arc, "other")
        self.assertTrue(any("weird" in r for r in result.dropped_reasons))

    def test_one_bad_does_not_kill_the_rest(self):
        good = valid_pub()
        bad = valid_pub(pmid="99999999")
        del bad["venue"]
        result = parse_feed(envelope(good, bad))
        self.assertEqual(len(result.publications), 1)
        self.assertEqual(result.dropped_count, 1)

    def test_non_dict_envelope_returns_error(self):
        result = parse_feed("not a dict")
        self.assertIsNotNone(result.error)

    def test_publications_field_must_be_list(self):
        result = parse_feed({"publications": "not a list"})
        self.assertIsNotNone(result.error)

    def test_stale_data_as_of_flagged(self):
        old = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat().replace("+00:00", "Z")
        result = parse_feed(envelope(valid_pub(), data_as_of=old))
        self.assertTrue(result.is_stale)

    def test_fresh_data_as_of_not_flagged(self):
        result = parse_feed(envelope(valid_pub()))
        self.assertFalse(result.is_stale)

    def test_invalid_data_as_of_logged_but_does_not_crash(self):
        env = envelope(valid_pub(), data_as_of="not-a-date")
        result = parse_feed(env)
        self.assertEqual(len(result.publications), 1)
        self.assertTrue(any("invalid data_as_of" in r for r in result.dropped_reasons))

    def test_year_coerced_to_int(self):
        result = parse_feed(envelope(valid_pub(year="2025")))
        self.assertEqual(result.publications[0].year, 2025)

    def test_optional_fields_default_to_false(self):
        pub = valid_pub()
        del pub["first_author"]
        del pub["senior_author"]
        del pub["open_access"]
        result = parse_feed(envelope(pub))
        p = result.publications[0]
        self.assertFalse(p.first_author)
        self.assertFalse(p.senior_author)
        self.assertFalse(p.open_access)


class TestLoadFeed(unittest.TestCase):
    def test_missing_file_returns_none(self):
        result = load_feed(Path("/tmp/definitely-does-not-exist-roizen.json"))
        self.assertIsNone(result)

    def test_invalid_json_returns_error_result(self):
        with NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write("{not valid json")
            tmp = f.name
        try:
            result = load_feed(Path(tmp))
            self.assertIsNotNone(result.error)
        finally:
            Path(tmp).unlink()

    def test_round_trip_valid_envelope(self):
        with NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(envelope(valid_pub()), f)
            tmp = f.name
        try:
            result = load_feed(Path(tmp))
            self.assertEqual(len(result.publications), 1)
        finally:
            Path(tmp).unlink()


class TestRenderHtml(unittest.TestCase):
    def test_renders_publication_link(self):
        result = parse_feed(envelope(valid_pub()))
        html = render_html(result)
        self.assertIn("pubmed.ncbi.nlm.nih.gov/12345678", html)
        self.assertIn("Example title", html)

    def test_groups_by_arc(self):
        result = parse_feed(envelope(
            valid_pub(pmid="1", research_arc="phenotype"),
            valid_pub(pmid="2", research_arc="mechanism"),
        ))
        html = render_html(result)
        self.assertIn("Phenotype", html)
        self.assertIn("Mechanism", html)
        self.assertLess(html.index("Phenotype"), html.index("Mechanism"))

    def test_senior_author_badge_present(self):
        result = parse_feed(envelope(valid_pub(senior_author=True, first_author=False)))
        html = render_html(result)
        self.assertIn("senior author", html)

    def test_first_author_badge_present(self):
        result = parse_feed(envelope(valid_pub(first_author=True, senior_author=False)))
        html = render_html(result)
        self.assertIn("first author", html)

    def test_staleness_banner_when_stale(self):
        old = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat().replace("+00:00", "Z")
        result = parse_feed(envelope(valid_pub(), data_as_of=old))
        html = render_html(result)
        self.assertIn("verified through", html)

    def test_no_staleness_banner_when_fresh(self):
        result = parse_feed(envelope(valid_pub()))
        html = render_html(result)
        self.assertNotIn("verified through", html)

    def test_truncates_author_list_with_et_al(self):
        many_authors = ["Roizen JD"] + [f"Author{i} X" for i in range(10)]
        result = parse_feed(envelope(valid_pub(authors=many_authors)))
        html = render_html(result)
        self.assertIn("et al.", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)

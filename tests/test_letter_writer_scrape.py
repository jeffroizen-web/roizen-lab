#!/usr/bin/env python3
"""
Tests for scripts/letter_writer_scrape.py

Run: python3 -m unittest tests.test_letter_writer_scrape -v

Network tests (PubMed e-utils) are gated by NET=1 env var to keep the
default suite hermetic. Default run = offline tests only.
"""
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from letter_writer_scrape import (  # noqa: E402
    normalize_name_for_pubmed,
    parse_display_name,
    parse_pubdate_year,
    extract_field_terms,
    extract_people_from_site,
    compute_confidence,
    probe_pubmed,
    probe_orcid,
    probe_with_fallback,
    orcid_disambiguate,
    PersonProbe,
)


class TestNormalizeName(unittest.TestCase):
    def test_strips_degrees(self):
        self.assertEqual(normalize_name_for_pubmed("Louis J. Muglia, MD, PhD"), "Muglia LJ")

    def test_single_middle_initial(self):
        self.assertEqual(normalize_name_for_pubmed("Michael A. Levine, MD"), "Levine MA")

    def test_no_middle(self):
        self.assertEqual(normalize_name_for_pubmed("Hakon Hakonarson"), "Hakonarson H")

    def test_single_name_passes_through(self):
        self.assertEqual(normalize_name_for_pubmed("Onename"), "Onename")

    def test_dots_stripped(self):
        # Initials should not leak the dot
        self.assertNotIn(".", normalize_name_for_pubmed("J. R. R. Tolkien"))


class TestParsePubdateYear(unittest.TestCase):
    def test_full_date(self):
        self.assertEqual(parse_pubdate_year("2026 Apr 28"), 2026)

    def test_year_month_range(self):
        self.assertEqual(parse_pubdate_year("2025 Jan-Feb"), 2025)

    def test_year_only(self):
        self.assertEqual(parse_pubdate_year("2024"), 2024)

    def test_empty_returns_none(self):
        self.assertIsNone(parse_pubdate_year(""))

    def test_garbage_returns_none(self):
        self.assertIsNone(parse_pubdate_year("not a date"))


class TestExtractFieldTerms(unittest.TestCase):
    def test_basic_term_extraction(self):
        titles = [
            "Vitamin D and bone mineralization in children",
            "Mendelian randomization of vitamin D",
            "Vitamin D status and asthma",
        ]
        terms = extract_field_terms(titles)
        self.assertIn("vitamin", terms)

    def test_stopwords_removed(self):
        terms = extract_field_terms(["the study of the role of the the the"])
        self.assertEqual(terms, [])

    def test_short_tokens_removed(self):
        terms = extract_field_terms(["a b c de ef gh"])
        # All <=3 chars, all should be excluded
        self.assertEqual(terms, [])

    def test_max_terms_cap(self):
        titles = [" ".join(f"word{i}" for i in range(20))]
        terms = extract_field_terms(titles, max_terms=5)
        self.assertLessEqual(len(terms), 5)

    def test_empty_titles_safe(self):
        self.assertEqual(extract_field_terms([]), [])
        self.assertEqual(extract_field_terms([None, "", "  "]), [])


class TestExtractPeopleFromSite(unittest.TestCase):
    def test_finds_people_with_h3_anchor(self):
        html = """
        <section id="mentors" class="section">
          <h3><a href="https://example.com/muglia">Louis J. Muglia, MD, PhD</a></h3>
          <h3><a href="https://example.com/levine">Michael A. Levine, MD</a></h3>
        </section>
        """
        people = extract_people_from_site(html)
        self.assertEqual(len(people), 2)
        self.assertEqual(people[0]["section"], "mentors")
        self.assertEqual(people[0]["name"], "Louis J. Muglia, MD, PhD")

    def test_missing_section_skipped(self):
        html = "<section id='nothing'></section>"
        self.assertEqual(extract_people_from_site(html), [])

    def test_real_site_yields_people(self):
        site = ROOT / "compare-purple-gold.html"
        if not site.exists():
            self.skipTest("working site missing")
        people = extract_people_from_site(site.read_text(encoding="utf-8"))
        self.assertGreater(len(people), 0)
        self.assertTrue(all("name" in p and "url" in p and "section" in p for p in people))


class TestConfidence(unittest.TestCase):
    def test_no_pubs_zero_confidence(self):
        p = PersonProbe(name="X", pubmed_query="X")
        score, notes = compute_confidence(p)
        self.assertEqual(score, 0.0)
        self.assertTrue(any("no recent" in n for n in notes))

    def test_many_recent_pubs_high_confidence(self):
        from datetime import datetime as dt
        p = PersonProbe(
            name="X", pubmed_query="X",
            recent_pmids=list("0123456789"),
            recent_years=[dt.now().year] * 10,
            field_terms=["vitamin", "asthma", "mendelian"],
        )
        score, _ = compute_confidence(p)
        self.assertGreaterEqual(score, 0.8)

    def test_old_pubs_low_recency(self):
        p = PersonProbe(
            name="X", pubmed_query="X",
            recent_pmids=["1", "2"],
            recent_years=[1990, 1995],
            field_terms=[],
        )
        score, _ = compute_confidence(p)
        self.assertLess(score, 0.5)

    def test_score_capped_at_one(self):
        from datetime import datetime as dt
        p = PersonProbe(
            name="X", pubmed_query="X",
            recent_pmids=list("0" * 50),
            recent_years=[dt.now().year] * 50,
            field_terms=["a", "b", "c", "d", "e"],
        )
        score, _ = compute_confidence(p)
        self.assertLessEqual(score, 1.0)


class TestParseDisplayName(unittest.TestCase):
    def test_basic_extraction(self):
        self.assertEqual(parse_display_name("Neil D. Romberg, MD"), ("Neil", "Romberg"))

    def test_drops_degrees(self):
        self.assertEqual(parse_display_name("Louis J. Muglia, MD, PhD"), ("Louis", "Muglia"))

    def test_single_token_passes_through(self):
        first, last = parse_display_name("Onename")
        self.assertEqual(first, "Onename")
        self.assertEqual(last, "")


class TestFallbackLogic(unittest.TestCase):
    """probe_with_fallback's L1→L2 decision logic, with both probes mocked."""

    def test_strong_l1_skips_l2(self):
        from unittest.mock import patch
        strong_l1 = PersonProbe(
            name="Dr Strong", pubmed_query="Strong D",
            recent_pmids=list("0123456789"),
            confidence=0.95, layer_used="L1_pubmed",
        )
        with patch("letter_writer_scrape.probe_pubmed", return_value=strong_l1) as mock_l1, \
             patch("letter_writer_scrape.probe_orcid") as mock_l2:
            result = probe_with_fallback("Dr Strong")
            mock_l1.assert_called_once()
            mock_l2.assert_not_called()
            self.assertEqual(result.layer_used, "L1_pubmed")

    def test_weak_l1_triggers_l2(self):
        from unittest.mock import patch
        weak_l1 = PersonProbe(
            name="Dr Weak", pubmed_query="Weak D",
            recent_pmids=["1", "2"],
            confidence=0.4, layer_used="L1_pubmed",
        )
        strong_l2 = PersonProbe(
            name="Dr Weak", pubmed_query="orcid:0000",
            recent_titles=["t1", "t2", "t3"],
            confidence=0.85, layer_used="L2_orcid",
        )
        with patch("letter_writer_scrape.probe_pubmed", return_value=weak_l1), \
             patch("letter_writer_scrape.probe_orcid", return_value=strong_l2):
            result = probe_with_fallback("Dr Weak")
            self.assertEqual(result.layer_used, "L2_orcid")

    def test_weak_l1_falls_back_when_l2_fails(self):
        from unittest.mock import patch
        weak_l1 = PersonProbe(
            name="Dr Ghost", pubmed_query="Ghost D",
            recent_pmids=["1"], confidence=0.3, layer_used="L1_pubmed",
        )
        with patch("letter_writer_scrape.probe_pubmed", return_value=weak_l1), \
             patch("letter_writer_scrape.probe_orcid", return_value=None):
            result = probe_with_fallback("Dr Ghost")
            self.assertEqual(result.layer_used, "L1_pubmed")
            self.assertTrue(any("L2 ORCID attempted" in n for n in result.confidence_notes))

    def test_l2_with_lower_confidence_not_chosen(self):
        from unittest.mock import patch
        l1 = PersonProbe(name="X", pubmed_query="X X", recent_pmids=["1", "2"],
                         confidence=0.55, layer_used="L1_pubmed")
        l2 = PersonProbe(name="X", pubmed_query="orcid:0",
                         recent_titles=[], confidence=0.40, layer_used="L2_orcid")
        with patch("letter_writer_scrape.probe_pubmed", return_value=l1), \
             patch("letter_writer_scrape.probe_orcid", return_value=l2):
            result = probe_with_fallback("X X")
            self.assertEqual(result.layer_used, "L1_pubmed")


@unittest.skipUnless(os.environ.get("NET") == "1", "set NET=1 to enable PubMed network test")
class TestPubmedNetwork(unittest.TestCase):
    def test_muglia_probe_returns_pmids(self):
        probe = probe_pubmed("Louis J. Muglia, MD, PhD")
        self.assertIsNone(probe.error)
        self.assertGreater(len(probe.recent_pmids), 0)
        self.assertGreater(probe.total_pubmed_count, 50)
        self.assertGreater(probe.confidence, 0.0)


@unittest.skipUnless(os.environ.get("NET") == "1", "set NET=1 to enable ORCID network test")
class TestOrcidNetwork(unittest.TestCase):
    def test_romberg_orcid_disambiguation(self):
        iid = orcid_disambiguate("Neil D. Romberg, MD")
        self.assertEqual(iid, "0000-0002-1881-5318")

    def test_romberg_l2_supersedes_l1(self):
        result = probe_with_fallback("Neil D. Romberg, MD")
        self.assertEqual(result.layer_used, "L2_orcid")
        self.assertGreater(len(result.recent_titles), 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)

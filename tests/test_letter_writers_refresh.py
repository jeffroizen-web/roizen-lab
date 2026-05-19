#!/usr/bin/env python3
"""
Tests for scripts/letter_writers_refresh.py — confidence-regression detection.

Run: python3 -m unittest tests.test_letter_writers_refresh -v
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from letter_writers_refresh import find_regressions, confidence_map  # noqa: E402


class TestConfidenceMap(unittest.TestCase):
    def test_extracts_name_to_conf_pairs(self):
        payload = {"records": [
            {"name": "Dr A", "confidence": 0.9},
            {"name": "Dr B", "confidence": 0.5},
        ]}
        self.assertEqual(confidence_map(payload), {"Dr A": 0.9, "Dr B": 0.5})

    def test_missing_confidence_defaults_to_zero(self):
        payload = {"records": [{"name": "Dr X"}]}
        self.assertEqual(confidence_map(payload), {"Dr X": 0.0})

    def test_no_records_returns_empty(self):
        self.assertEqual(confidence_map({}), {})


class TestFindRegressions(unittest.TestCase):
    def test_no_change_no_regression(self):
        self.assertEqual(find_regressions({"Dr A": 0.9}, {"Dr A": 0.9}), [])

    def test_small_drop_below_threshold_ignored(self):
        # default threshold = 0.2
        self.assertEqual(find_regressions({"Dr A": 0.9}, {"Dr A": 0.75}), [])

    def test_large_drop_caught(self):
        regs = find_regressions({"Dr A": 0.9}, {"Dr A": 0.5})
        self.assertEqual(len(regs), 1)
        self.assertEqual(regs[0]["name"], "Dr A")
        self.assertAlmostEqual(regs[0]["prior"], 0.9)
        self.assertAlmostEqual(regs[0]["new"], 0.5)

    def test_threshold_boundary_inclusive(self):
        # exactly 0.2 drop should count as regression
        self.assertEqual(len(find_regressions({"Dr A": 0.9}, {"Dr A": 0.7})), 1)

    def test_just_below_threshold_excluded(self):
        self.assertEqual(find_regressions({"Dr A": 0.9}, {"Dr A": 0.71}), [])

    def test_missing_person_caught(self):
        regs = find_regressions({"Dr A": 0.9, "Dr B": 0.8}, {"Dr A": 0.9})
        self.assertEqual(len(regs), 1)
        self.assertEqual(regs[0]["name"], "Dr B")
        self.assertIsNone(regs[0]["new"])
        self.assertEqual(regs[0]["reason"], "missing")

    def test_improvement_is_not_regression(self):
        self.assertEqual(find_regressions({"Dr A": 0.5}, {"Dr A": 0.9}), [])

    def test_custom_threshold_honored(self):
        # tighter threshold catches a smaller drop
        self.assertEqual(len(find_regressions({"Dr A": 0.9}, {"Dr A": 0.85}, threshold=0.05)), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)

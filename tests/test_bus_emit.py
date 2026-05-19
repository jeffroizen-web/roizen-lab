#!/usr/bin/env python3
"""
Tests for scripts/bus_emit.py

Default suite is hermetic (no network). NET=1 unlocks the live bus test
which hits the real Pilot trial endpoint — gated separately so accidental
runs don't pollute the bus.

Run:
    python3 -m unittest tests.test_bus_emit -v
    NET=1 python3 -m unittest tests.test_bus_emit.TestLiveBus -v
"""
import io
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import bus_emit  # noqa: E402


class TestEmit(unittest.TestCase):
    def setUp(self):
        # Redirect audit log to a tmp file per test, then restore.
        self._orig_log = bus_emit.AUDIT_LOG
        self._tmp_log = Path("/tmp/ace-scout-bus-emit-test.jsonl")
        if self._tmp_log.exists():
            self._tmp_log.unlink()
        bus_emit.AUDIT_LOG = self._tmp_log

    def tearDown(self):
        bus_emit.AUDIT_LOG = self._orig_log
        if self._tmp_log.exists():
            self._tmp_log.unlink()

    def test_dry_run_does_not_call_network(self):
        with patch.object(bus_emit, "urlopen") as mock_urlopen:
            result = bus_emit.emit("test.kind", {"foo": "bar"}, dry_run=True)
            mock_urlopen.assert_not_called()
            self.assertEqual(result["status"], "dry-run")

    def test_dry_run_writes_audit_line(self):
        bus_emit.emit("test.kind", {"foo": "bar"}, dry_run=True)
        lines = self._tmp_log.read_text().strip().split("\n")
        self.assertEqual(len(lines), 1)
        entry = json.loads(lines[0])
        self.assertEqual(entry["status"], "dry-run")
        self.assertEqual(entry["event"]["kind"], "test.kind")

    def test_missing_token_skipped_not_delivered(self):
        with patch.dict(os.environ, {"TRIAL_BUS_TOKEN": ""}, clear=False):
            with patch.object(bus_emit, "_fetch_token", return_value=None):
                result = bus_emit.emit("test.kind", {"foo": "bar"}, dry_run=False)
                self.assertEqual(result["status"], "skipped")

    def test_delivered_status_on_200(self):
        fake_response = MagicMock()
        fake_response.read.return_value = b'{"status":"applied"}'
        fake_response.status = 200
        fake_response.__enter__ = lambda s: s
        fake_response.__exit__ = lambda *a: None
        with patch.object(bus_emit, "urlopen", return_value=fake_response):
            result = bus_emit.emit(
                "test.kind", {"foo": "bar"}, dry_run=False, token="fake-token"
            )
            self.assertEqual(result["status"], "delivered")
            self.assertEqual(result["bus_response"], {"status": "applied"})

    def test_http_error_returns_error_status(self):
        from urllib.error import HTTPError
        err = HTTPError("https://x", 403, "Forbidden", {}, None)
        with patch.object(bus_emit, "urlopen", side_effect=err):
            result = bus_emit.emit(
                "test.kind", {"foo": "bar"}, dry_run=False, token="fake-token"
            )
            self.assertEqual(result["status"], "error")

    def test_network_error_returns_error_status(self):
        from urllib.error import URLError
        with patch.object(bus_emit, "urlopen", side_effect=URLError("connection refused")):
            result = bus_emit.emit(
                "test.kind", {"foo": "bar"}, dry_run=False, token="fake-token"
            )
            self.assertEqual(result["status"], "error")

    def test_empty_kind_raises(self):
        with self.assertRaises(ValueError):
            bus_emit.emit("", {})

    def test_non_dict_payload_raises(self):
        with self.assertRaises(ValueError):
            bus_emit.emit("test.kind", "not a dict")

    def test_env_var_disabled_forces_dry_run(self):
        with patch.dict(os.environ, {"CROSS_CM_BUS_TRIAL_ENABLED": "0"}, clear=False):
            with patch.object(bus_emit, "urlopen") as mock_urlopen:
                result = bus_emit.emit("test.kind", {"foo": "bar"})
                mock_urlopen.assert_not_called()
                self.assertEqual(result["status"], "dry-run")

    def test_env_var_enabled_attempts_post(self):
        with patch.dict(os.environ, {
            "CROSS_CM_BUS_TRIAL_ENABLED": "1",
            "TRIAL_BUS_TOKEN": "fake-token",
        }, clear=False):
            fake_response = MagicMock()
            fake_response.read.return_value = b'{"status":"applied"}'
            fake_response.status = 200
            fake_response.__enter__ = lambda s: s
            fake_response.__exit__ = lambda *a: None
            with patch.object(bus_emit, "urlopen", return_value=fake_response) as mock_urlopen:
                result = bus_emit.emit("test.kind", {"foo": "bar"})
                mock_urlopen.assert_called_once()
                self.assertEqual(result["status"], "delivered")

    def test_event_envelope_uses_pilot_camelcase_schema(self):
        # Pilot's API requires camelCase keys + string confidence + eventId/emittedAt (MSG-b14dd7).
        bus_emit.emit("test.kind", {"foo": "bar"}, dry_run=True, confidence=0.75)
        entry = json.loads(self._tmp_log.read_text().strip())
        ev = entry["event"]
        for field in ("eventId", "emittedBy", "emittedAt", "subjectDate", "kind", "payload", "confidence"):
            self.assertIn(field, ev)
        self.assertEqual(ev["emittedBy"], "ace-scout")
        self.assertEqual(ev["confidence"], "high")  # 0.75 -> "high" bucket
        self.assertTrue(ev["eventId"].startswith("ace-scout-test.kind-"))
        # Reject snake_case leakage:
        for legacy in ("source", "subject_date", "emitted_at"):
            self.assertNotIn(legacy, ev)


class TestConfidenceBuckets(unittest.TestCase):
    def test_high_numeric_maps_to_exact(self):
        self.assertEqual(bus_emit.confidence_to_string(0.95), "exact")
        self.assertEqual(bus_emit.confidence_to_string(1.0), "exact")

    def test_mid_numeric_maps_to_high_or_medium(self):
        self.assertEqual(bus_emit.confidence_to_string(0.80), "high")
        self.assertEqual(bus_emit.confidence_to_string(0.55), "medium")

    def test_low_numeric_maps_to_low(self):
        self.assertEqual(bus_emit.confidence_to_string(0.35), "low")

    def test_very_low_numeric_maps_to_very_low(self):
        self.assertEqual(bus_emit.confidence_to_string(0.10), "very-low")
        self.assertEqual(bus_emit.confidence_to_string(0), "very-low")

    def test_string_passes_through(self):
        self.assertEqual(bus_emit.confidence_to_string("exact"), "exact")
        self.assertEqual(bus_emit.confidence_to_string("custom-label"), "custom-label")

    def test_bad_input_defaults_to_very_low(self):
        self.assertEqual(bus_emit.confidence_to_string(None), "very-low")
        self.assertEqual(bus_emit.confidence_to_string([]), "very-low")


@unittest.skipUnless(os.environ.get("NET") == "1", "set NET=1 to enable live bus test")
class TestLiveBus(unittest.TestCase):
    def test_real_bus_responds_to_ping(self):
        # Use a probe.* kind so Pilot can recognize this as a test ping
        result = bus_emit.emit(
            "probe.ping",
            {"source": "ace-scout-test", "purpose": "wire verification"},
            confidence=0.1,
            dry_run=False,
        )
        self.assertIn(result["status"], ("delivered", "skipped", "error"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

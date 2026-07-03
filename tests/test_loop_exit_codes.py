#!/usr/bin/env python3
"""Loop exit-code contract (R2 / exit-code-outcome-mismatch fix, 2026-07-03).

Both launchd loops used to `return 1` when they SUCCESSFULLY detected drift, which
launchd reads as a crash (the registered `exit-code-outcome-mismatch` failure class).
The fix: drift is a FINDING carried in the JSON `outcome` field + the emitted bus
event; the process exits 0 on any successful run and nonzero ONLY on genuine
execution failure.

These tests are the acceptance proof: a forced-regression run exits 0 while the
outcome/event carries the regression.

Run: python3 -m pytest tests/test_loop_exit_codes.py -q
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

TENURE = ROOT / "scripts" / "tenure_readiness.py"

_CLEAN_HTML = (
    "<!DOCTYPE html><html><head></head><body>"
    '<a href="#main-content" class="skip-link">Skip</a>'
    '<main id="main-content">'
    "<p>NIH-funded · 27 publications</p>"
    '<img src="x.png" alt="x" width="10" height="10">'
    "</main></body></html>"
)
# Same page + one NEW dead hash link => a regression vs the clean baseline.
_DRIFT_HTML = _CLEAN_HTML.replace(
    "</main>", '<a href="#">Read the paper</a></main>'
)


def _run_tenure(html_path, baseline_path):
    """Run the watcher in --json mode; return (returncode, parsed_json)."""
    proc = subprocess.run(
        [sys.executable, str(TENURE), "--json",
         "--file", str(html_path), "--baseline-file", str(baseline_path)],
        capture_output=True, text=True,
    )
    payload = json.loads(proc.stdout) if proc.stdout.strip() else {}
    return proc.returncode, payload


def _write(tmp_path, name, content):
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


# ---- tenure_readiness watcher -------------------------------------------------

def test_tenure_drift_exits_zero_and_flags_outcome(tmp_path):
    """The acceptance proof: detected drift => exit 0, outcome carries it."""
    clean = _write(tmp_path, "clean.html", _CLEAN_HTML)
    drift = _write(tmp_path, "drift.html", _DRIFT_HTML)
    bl = tmp_path / "baseline.json"
    # Establish a clean baseline, then scan the drifted page against it.
    subprocess.run(
        [sys.executable, str(TENURE), "--baseline",
         "--file", str(clean), "--baseline-file", str(bl)],
        capture_output=True, text=True, check=True,
    )
    rc, payload = _run_tenure(drift, bl)
    assert rc == 0, f"drift-detect must exit 0 (was {rc}) — launchd reads nonzero as crash"
    assert payload["outcome"] == "drift-detected"
    assert payload["regressions"], "the regression must be carried in the payload"


def test_tenure_clean_exits_zero(tmp_path):
    clean = _write(tmp_path, "clean.html", _CLEAN_HTML)
    bl = tmp_path / "baseline.json"
    subprocess.run(
        [sys.executable, str(TENURE), "--baseline",
         "--file", str(clean), "--baseline-file", str(bl)],
        capture_output=True, text=True, check=True,
    )
    rc, payload = _run_tenure(clean, bl)
    assert rc == 0
    assert payload["outcome"] == "clean"
    assert payload["regressions"] == []


def test_tenure_no_baseline_exits_zero(tmp_path):
    clean = _write(tmp_path, "clean.html", _CLEAN_HTML)
    bl = tmp_path / "missing-baseline.json"  # does not exist
    rc, payload = _run_tenure(clean, bl)
    assert rc == 0, "a missing baseline is a setup state, not a crash"
    assert payload["outcome"] == "no-baseline"


def test_tenure_execution_failure_exits_nonzero(tmp_path):
    """A genuine failure (unreadable HTML) is the ONLY nonzero case."""
    bl = tmp_path / "baseline.json"
    proc = subprocess.run(
        [sys.executable, str(TENURE), "--json",
         "--file", str(tmp_path / "does-not-exist.html"),
         "--baseline-file", str(bl)],
        capture_output=True, text=True,
    )
    assert proc.returncode != 0, "an unreadable input file must exit nonzero"


# ---- letter_writers_refresh loop ---------------------------------------------

def test_letter_writers_refresh_regression_exits_zero(tmp_path, monkeypatch):
    """A detected confidence-regression is a successful run => exit 0, drift in
    the summary + the emitted regression event (never the exit code)."""
    import letter_writers_refresh as lw

    data = tmp_path / "letter_writers.json"
    prev = tmp_path / "letter_writers_prev.json"
    monkeypatch.setattr(lw, "DATA", data)
    monkeypatch.setattr(lw, "PREV", prev)

    # Prior state: one person at high confidence.
    data.write_text(json.dumps({"generated_at": "2026-07-03T00:00:00Z",
                                "records": [{"name": "Dr A", "confidence": 0.9}]}))

    emitted = []
    monkeypatch.setattr(lw, "emit",
                        lambda *a, **k: (emitted.append((a, k)) or {"status": "skipped"}))

    def fake_run(cmd, *a, **k):
        joined = " ".join(cmd)
        if "letter_writer_scrape.py" in joined:
            # "Scrape" writes a NEW state with the same person at LOW confidence
            # (a >=0.2 drop => a regression).
            data.write_text(json.dumps({"generated_at": "2026-07-03T01:00:00Z",
                                        "records": [{"name": "Dr A", "confidence": 0.5}]}))
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(lw.subprocess, "run", fake_run)

    rc = lw.main()
    assert rc == 0, f"a successful regression-detect must exit 0 (was {rc})"
    # The regression rode the emitted event, not the exit code.
    assert any(
        args and isinstance(args[1], dict) and args[1].get("outcome") == "confidence-regression"
        for args, _ in emitted
    ), "a confidence-regression event must be emitted"


def test_letter_writers_refresh_scrape_failure_exits_nonzero(tmp_path, monkeypatch):
    """Genuine scrape failure is the nonzero case (unchanged)."""
    import letter_writers_refresh as lw
    data = tmp_path / "letter_writers.json"
    prev = tmp_path / "letter_writers_prev.json"
    monkeypatch.setattr(lw, "DATA", data)
    monkeypatch.setattr(lw, "PREV", prev)
    monkeypatch.setattr(lw, "emit", lambda *a, **k: {"status": "skipped"})

    def fake_run(cmd, *a, **k):
        return subprocess.CompletedProcess(cmd, 1, stdout="", stderr="scrape blew up")

    monkeypatch.setattr(lw.subprocess, "run", fake_run)
    assert lw.main() == 1, "a failed scrape must exit nonzero"

#!/usr/bin/env python3
"""Gated auto-redeploy guard — scripts/deploy_publish.sh (Kleiber MSG-006188).

Every path here runs the deploy script WITHOUT a real force-push:
- DISARMED (ROIZEN_AUTO_DEPLOY unset/!=1) → the script exits before any network,
- ROIZEN_DEPLOY_DRY_RUN=1 → the change/gate logic runs but the push is stubbed.
State + log are redirected to a tmp dir, so the test never touches the real
deploy state and never fires a live push (test-fired-prod-side-effect guard).

Run: python3 -m pytest tests/test_deploy_publish.py -q
"""
import json
import os
import subprocess
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "deploy_publish.sh"
CANONICAL = ROOT / "compare-purple-gold.html"


def _run(env_extra, tmp_path):
    """Run deploy_publish.sh with state+log redirected into tmp_path."""
    env = dict(os.environ)
    env.pop("ROIZEN_AUTO_DEPLOY", None)
    env.update({
        "ROIZEN_DEPLOY_STATE": str(tmp_path / "last_hash"),
        "ROIZEN_DEPLOY_LOG": str(tmp_path / "deploy.jsonl"),
    })
    env.update(env_extra)
    proc = subprocess.run(
        ["bash", str(SCRIPT)], cwd=str(ROOT), env=env,
        capture_output=True, text=True, timeout=120,
    )
    log = tmp_path / "deploy.jsonl"
    rows = [json.loads(l) for l in log.read_text().splitlines()] if log.exists() else []
    return proc, rows


def _canon_hash():
    return hashlib.sha256(CANONICAL.read_bytes()).hexdigest()


def test_disarmed_by_default_never_deploys(tmp_path):
    """No ROIZEN_AUTO_DEPLOY → outcome=disarmed, exit 0, no state written."""
    proc, rows = _run({}, tmp_path)
    assert proc.returncode == 0, proc.stderr
    assert rows and rows[-1]["outcome"] == "disarmed"
    assert not (tmp_path / "last_hash").exists(), "disarmed run must not write deploy state"


def test_armed_dry_run_deploys_and_records_hash(tmp_path):
    """Armed + dry-run + fresh state (no last hash) → change detected, gate runs,
    outcome=deployed-dry-run, canonical hash persisted, NO real push."""
    proc, rows = _run(
        {"ROIZEN_AUTO_DEPLOY": "1", "ROIZEN_DEPLOY_DRY_RUN": "1"}, tmp_path)
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert rows[-1]["outcome"] == "deployed-dry-run"
    assert (tmp_path / "last_hash").read_text().strip() == _canon_hash()


def test_change_detect_skips_when_hash_unchanged(tmp_path):
    """Armed, but last-deployed hash == current canonical → outcome=no-change,
    gate NOT run, no push."""
    (tmp_path / "last_hash").write_text(_canon_hash())
    proc, rows = _run(
        {"ROIZEN_AUTO_DEPLOY": "1", "ROIZEN_DEPLOY_DRY_RUN": "1"}, tmp_path)
    assert proc.returncode == 0, proc.stderr
    assert rows[-1]["outcome"] == "no-change"


def test_change_detect_fires_when_hash_differs(tmp_path):
    """A stale last-deployed hash → change detected → dry-run deploy path."""
    (tmp_path / "last_hash").write_text("deadbeef" * 8)
    proc, rows = _run(
        {"ROIZEN_AUTO_DEPLOY": "1", "ROIZEN_DEPLOY_DRY_RUN": "1"}, tmp_path)
    assert proc.returncode == 0, proc.stderr
    assert rows[-1]["outcome"] == "deployed-dry-run"


def test_every_path_writes_an_observable_outcome(tmp_path):
    """Daily-Fire Route-Side-Gate: no silent no-ops — every run logs a row."""
    proc, rows = _run({}, tmp_path)
    assert len(rows) >= 1 and "outcome" in rows[-1]

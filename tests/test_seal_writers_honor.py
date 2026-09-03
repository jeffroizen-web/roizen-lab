"""Seal-sweep guards: every writer behind a sealed env READS+HONORS it.

Class (Kleiber MSG-4f32b9, fleet sweep 2026-09-03; memory
reference_seal_env_registered_but_writer_never_reads): a seal env is set in
conftest while the writer never consults it (hardcoded path, or env read once
at import before the seal ran) — the seal is decoration, the test writes LIVE.

These tests are EMPIRICAL (redirect env → run writer → assert the sink moved),
never an env-name grep. Two findings from the 9/03 probe, both fixed:
  1. scripts/bus_emit.py captured PRODUCER_READBACK_LEDGER at IMPORT time
     (probe: env changed after import → row still landed at the pre-import path).
  2. scripts/deploy_publish.sh had NO seal floor: a bare disarmed run appended a
     row to the live docs/reports/deploy-publish.jsonl. conftest now floors
     ROIZEN_DEPLOY_{STATE,LOG} into tmp and forces ROIZEN_AUTO_DEPLOY=0.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import bus_emit  # noqa: E402

LIVE_DEPLOY_LOG = ROOT / "docs" / "reports" / "deploy-publish.jsonl"
LIVE_DEPLOY_STATE = ROOT / "docs" / "reports" / ".deploy_last_hash"
LIVE_AUDIT_LOG = ROOT / "decisions" / "bus_emit_log.jsonl"
LIVE_READBACK_LEDGER = Path("~/.kleiber/logs/producer_readback_writes.jsonl").expanduser()


def _size(p: Path) -> int:
    return p.stat().st_size if p.exists() else -1


# ---- bus_emit: PRODUCER_READBACK_LEDGER (fleet registry env) ---------------

def test_readback_ledger_env_is_read_at_call_time_not_import(monkeypatch, tmp_path):
    """Changing the env AFTER import must move the sink (kills ENV-AT-IMPORT)."""
    monkeypatch.setattr(bus_emit, "READBACK_LEDGER", None)
    a, b = tmp_path / "a.jsonl", tmp_path / "b.jsonl"
    monkeypatch.setenv("PRODUCER_READBACK_LEDGER", str(a))
    assert bus_emit._readback_ledger_path() == a
    monkeypatch.setenv("PRODUCER_READBACK_LEDGER", str(b))
    assert bus_emit._readback_ledger_path() == b


def test_readback_ledger_write_lands_at_sealed_path_live_untouched(monkeypatch, tmp_path):
    monkeypatch.setattr(bus_emit, "READBACK_LEDGER", None)
    sink = tmp_path / "ledger.jsonl"
    monkeypatch.setenv("PRODUCER_READBACK_LEDGER", str(sink))
    before = _size(LIVE_READBACK_LEDGER)
    bus_emit._ledger_write({"probe": "seal-sweep"})
    assert json.loads(sink.read_text().strip()) == {"probe": "seal-sweep"}
    assert _size(LIVE_READBACK_LEDGER) == before, "writer ignored the seal and wrote LIVE"


def test_readback_ledger_patch_point_beats_env(monkeypatch, tmp_path):
    patched = tmp_path / "patched.jsonl"
    monkeypatch.setenv("PRODUCER_READBACK_LEDGER", str(tmp_path / "env.jsonl"))
    monkeypatch.setattr(bus_emit, "READBACK_LEDGER", patched)
    assert bus_emit._readback_ledger_path() == patched


def test_readback_ledger_default_is_the_expanded_home_path(monkeypatch):
    monkeypatch.setattr(bus_emit, "READBACK_LEDGER", None)
    monkeypatch.delenv("PRODUCER_READBACK_LEDGER", raising=False)
    assert bus_emit._readback_ledger_path() == LIVE_READBACK_LEDGER


# ---- bus_emit: ACE_BUS_AUDIT_LOG (repo floor env) ---------------------------

def test_audit_log_honors_env_at_call_time_live_untouched(monkeypatch, tmp_path):
    monkeypatch.setattr(bus_emit, "AUDIT_LOG", None)
    sink = tmp_path / "audit.jsonl"
    monkeypatch.setenv("ACE_BUS_AUDIT_LOG", str(sink))
    before = _size(LIVE_AUDIT_LOG)
    returned = bus_emit._audit_write({"probe": "audit"})
    assert returned == sink and sink.exists()
    assert _size(LIVE_AUDIT_LOG) == before


# ---- conftest floor: deploy_publish.sh sinks + kill-switch -------------------

def test_repo_floor_forces_deploy_kill_switch_off_and_sinks_into_tmp():
    assert os.environ.get("ROIZEN_AUTO_DEPLOY") == "0"
    assert os.environ.get("ROIZEN_DEPLOY_DRY_RUN") == "1"
    for name in ("ROIZEN_DEPLOY_STATE", "ROIZEN_DEPLOY_LOG", "ACE_BUS_AUDIT_LOG",
                 "PRODUCER_READBACK_LEDGER"):
        val = os.environ.get(name, "")
        assert val, f"{name} not sealed"
        assert not Path(val).resolve().is_relative_to(ROOT), f"{name} points inside the repo"
        assert Path(val) != LIVE_READBACK_LEDGER


@pytest.mark.skipif(not (ROOT / "scripts" / "deploy_publish.sh").exists(), reason="no deploy script")
def test_deploy_publish_bare_run_under_floor_never_touches_live_log():
    """The gold-standard probe: run the writer with ONLY the session floor
    (no per-test redirect) and assert the live outcome log is untouched."""
    live_before = (_size(LIVE_DEPLOY_LOG), _size(LIVE_DEPLOY_STATE))
    floor_log = Path(os.environ["ROIZEN_DEPLOY_LOG"])
    floor_rows_before = len(floor_log.read_text().splitlines()) if floor_log.exists() else 0

    proc = subprocess.run(["bash", str(ROOT / "scripts" / "deploy_publish.sh")],
                          cwd=str(ROOT), env=dict(os.environ),
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr

    rows = [json.loads(l) for l in floor_log.read_text().splitlines()]
    assert len(rows) == floor_rows_before + 1
    assert rows[-1]["outcome"] == "disarmed"
    assert (_size(LIVE_DEPLOY_LOG), _size(LIVE_DEPLOY_STATE)) == live_before, \
        "deploy_publish.sh wrote the LIVE outcome log/state under the seal"

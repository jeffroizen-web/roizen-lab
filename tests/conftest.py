"""Pytest session seal (security-standards rule 1 / toolchain-arc finding 2).

Redirects the failure-ledger + Jeff-notify paths away from their shared
production defaults BEFORE any test runs, so no FUTURE test can fire a prod
side effect (the test-fired-prod-side-effect class). This repo had 24 python
test files and NO conftest at any depth (Kleiber MSG-377bf4, Jeff-directed
review MSG-2393a3) — the 3 side-effect-shaped tests use per-test mocks today,
so the risk this closes is forward-looking: a harness-level seal every new
test inherits by default.

Prefers the distributed canonical seal (imported by absolute path, so it
always runs CURRENT logic — no vendored fork to drift); falls back to an
explicit tmp redirect if the canonical is unreachable. Mirrors the triready
reference shape.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

_DISTRIBUTED_SEAL_DIR = Path(
    "/Users/roizenj/Code/Claude Apps/Claude coding Asst/scripts"
)


def _seal() -> None:
    if _DISTRIBUTED_SEAL_DIR.exists() and str(_DISTRIBUTED_SEAL_DIR) not in sys.path:
        sys.path.insert(0, str(_DISTRIBUTED_SEAL_DIR))
    try:
        from conftest_env_seal import seal_test_env  # type: ignore

        seal_test_env()
        return
    except Exception:
        pass
    # Explicit fallback (security-standards rule 1: "else set the redirect env explicitly").
    tmp = _tmp_dir()
    os.environ["KLEIBER_FAILURE_LEDGER"] = str(tmp / "failure_ledger.jsonl")
    os.environ["NOTIFY_JEFF_DISABLE"] = "1"
    # The canonical registry also seals this; the fallback must too, because
    # scripts/bus_emit.py writes it on every non-dry-run emit (seal-sweep 9/03).
    os.environ["PRODUCER_READBACK_LEDGER"] = str(tmp / "producer_readback_writes.jsonl")


_TMP: Path | None = None


def _tmp_dir() -> Path:
    global _TMP
    if _TMP is None:
        _TMP = Path(tempfile.mkdtemp(prefix="roizen-lab-test-seal-"))
    return _TMP


# Repo-specific sinks NOT in the fleet SEAL_REGISTRY (seal-sweep 2026-09-03,
# Kleiber MSG-4f32b9). Empirically proven: a bare `bash scripts/deploy_publish.sh`
# under pytest with no floor appended a row to the LIVE outcome log
# docs/reports/deploy-publish.jsonl. Every env here is read at call time by
# its writer (tests/test_seal_writers_honor.py probes each one).
REPO_SEAL_FLOOR = {
    "ROIZEN_AUTO_DEPLOY": "0",        # kill-switch forced OFF: no test can arm a real push
    "ROIZEN_DEPLOY_DRY_RUN": "1",     # belt-and-braces: even an armed path never pushes
    "ROIZEN_DEPLOY_STATE": "deploy_last_hash",
    "ROIZEN_DEPLOY_LOG": "deploy-publish.jsonl",
    "ACE_BUS_AUDIT_LOG": "bus_emit_log.jsonl",
}
_FLAG_ENVS = {"ROIZEN_AUTO_DEPLOY", "ROIZEN_DEPLOY_DRY_RUN"}


def _seal_repo_floor() -> None:
    tmp = _tmp_dir()
    for name, value in REPO_SEAL_FLOOR.items():
        os.environ[name] = value if name in _FLAG_ENVS else str(tmp / value)


_seal()
_seal_repo_floor()

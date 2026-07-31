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
    tmp = Path(tempfile.mkdtemp(prefix="roizen-lab-test-seal-"))
    os.environ["KLEIBER_FAILURE_LEDGER"] = str(tmp / "failure_ledger.jsonl")
    os.environ["NOTIFY_JEFF_DISABLE"] = "1"


_seal()

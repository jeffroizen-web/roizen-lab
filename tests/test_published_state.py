"""Guards for docs/state.json — the copy OTHER CMs actually read.

Kleiber's fleet measurement (MSG-fc8143) split the fleet in two, and this repo is
in the TRACKED group: docs/state.json is committed, not gitignored. That posture
has a specific failure mode he named — **editing the working copy without
committing publishes NOTHING while looking done**. Maestro hit exactly that state
today.

So these assert the property that actually matters, which is not "my file is
fine" but "the copy a reader gets is fine":

  * the file is TRACKED, so a git-reader path exists at all
  * the committed (HEAD) copy — not the working copy — passes the canonical
    freshness reader on every key

Note the consumers (query_cm_at_path, state_staleness_brief) currently read the
FILESYSTEM, so both postures work today. They work because everything lives on
one machine; four CMs' published state exists nowhere but this disk. These tests
guard the git-reader path on the assumption that will not always hold.

CANONICAL, NEVER VENDORED, and FAILS OPEN — same rule as
tests/test_decision_queue_nudge.py: import Kleiber's reader by path and skip
rather than fail if his repo moves.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "docs" / "state.json"
QUERY_CM = Path(
    "/Users/roizenj/Code/Claude Apps/Claude coding Asst/scripts/query_cm.py"
)


def _load_reader():
    if not QUERY_CM.exists():
        pytest.skip(f"canonical reader not present at {QUERY_CM}")
    spec = importlib.util.spec_from_file_location("query_cm", QUERY_CM)
    mod = importlib.util.module_from_spec(spec)
    # MUST register before exec_module: the module defines @dataclass classes,
    # and dataclasses resolves field types via sys.modules[cls.__module__].
    # Without this the import dies with a bare AttributeError on NoneType —
    # which my first version caught in the fail-open handler and turned into a
    # SKIP. The guard read "1 passed, 1 skipped" and was entirely inert.
    sys.modules[spec.name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception as exc:
        # Fail OPEN only for THEIR repo being gone — never for my own loader
        # being broken, which is what the skip was hiding.
        del sys.modules[spec.name]
        raise AssertionError(
            f"canonical reader exists at {QUERY_CM} but failed to import: {exc!r}. "
            "This is a defect in this test's loader, not a reason to skip."
        ) from exc
    return mod


def test_state_json_is_tracked_so_a_git_reader_gets_something():
    out = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "docs/state.json"],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    assert out.returncode == 0, (
        "docs/state.json is NOT tracked. This repo is in the tracked group; if "
        "that changes deliberately, the published state becomes local-only and "
        "this guard should be retired on purpose, not silently."
    )


def test_committed_copy_is_fresh_on_every_key(tmp_path):
    """The published copy is HEAD's, not the working copy. A state fix that is
    edited but never committed leaves readers on the old row while the author
    believes it is done."""
    mod = _load_reader()
    blob = subprocess.run(
        ["git", "show", "HEAD:docs/state.json"],
        cwd=str(ROOT), capture_output=True, text=True, check=True,
    ).stdout
    head_copy = tmp_path / "state.json"
    head_copy.write_text(blob, encoding="utf-8")

    keys = json.loads(blob)["keys"]
    assert keys, "committed state.json has no keys"
    stale = {
        k: mod.query_cm_at_path(head_copy, k, as_cm="kleiber").status
        for k in keys
    }
    bad = {k: v for k, v in stale.items() if v != "ok"}
    assert not bad, (
        f"the COMMITTED copy is not ok on {len(bad)} key(s): {bad}. "
        "Re-verify each at source and commit — a restamp is a claim the fact "
        "was re-confirmed, not that it was retyped."
    )

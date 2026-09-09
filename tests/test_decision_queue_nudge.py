"""Insurance: my Jeff-blocking asks stay visible to Kleiber's aging nudge.

WHY THIS EXISTS. `kleiber_briefing._scan_decision_aging` is the only automatic
Jeff-facing nudge in the system. It surfaces Decision Queue items past 7 days —
and it silently skips anything that misses its format. That is how a
perfectly-stamped WAITING-ON sat unnoticed for 173 days. My four asks now
conform, but nothing stops a future edit (a reformat, a heading rename, dropping
a checkbox) from making them invisible again with no error anywhere.

THE FOUR CONDITIONS, each read from the consumer's source, not from a
description of it (Kleiber MSG-3c6d13 gave only #3; #2 was found by reading the
code and independently by Hermes; #1 and #4 are in the same function):
  1. SECTION  the line sits under a literal "## Decision Queue" heading
  2. PREFIX   the line starts with "- ["   <- checked BEFORE the date regex
  3. STAMP    "(added: YYYY-MM-DD)", closing paren IMMEDIATELY after the date;
              "(added: 2026-09-08; note)" does NOT match
  4. AGE      surfaces only once age >= 7 days

CANONICAL, NEVER VENDORED (Hermes's shape, and the same rule as log_failure.py
and tmux_send.py): this imports Kleiber's module BY PATH and calls HIS function.
It deliberately does NOT copy his regex — a local copy would drift and then agree
with itself forever, which is precisely the bug class this guards against.

FAILS OPEN. If Kleiber's repo moves or the module cannot be imported, these skip
rather than fail: a Kleiber-side path change must never redden my suite.
"""
from __future__ import annotations

import datetime
import importlib.util
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = ROOT / "CLAUDE.md"
KLEIBER_BRIEFING = Path(
    "/Users/roizenj/Code/Claude Apps/Claude coding Asst/kleiber_briefing.py"
)
# primary_projects() keys are CAPITALISED — Hermes nearly reported its project
# unscanned because it probed for the lowercase nick. Match the exact key.
MY_PROJECT_KEY = "Ace Scout"


def _load_briefing():
    if not KLEIBER_BRIEFING.exists():
        pytest.skip(f"canonical briefing module not present at {KLEIBER_BRIEFING}")
    sys.path.insert(0, str(KLEIBER_BRIEFING.parent))
    spec = importlib.util.spec_from_file_location("kleiber_briefing", KLEIBER_BRIEFING)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as exc:  # fail OPEN — never redden my suite for their repo
        pytest.skip(f"canonical briefing module unimportable: {exc}")
    return mod


class _ClockAhead:
    """datetime shim advancing only date.today(), so aged items surface."""

    def __init__(self, real, days):
        self._real, self._days = real, days

    def __getattr__(self, name):
        return getattr(self._real, name)

    @property
    def date(self):
        real_date, days = self._real.date, self._days

        class _D(real_date):
            @classmethod
            def today(cls):
                return real_date.today() + datetime.timedelta(days=days)
        return _D


def _scan_with_clock_ahead(mod, days=30):
    original = mod.datetime
    mod.datetime = _ClockAhead(original, days)
    try:
        return [i for i in mod._scan_decision_aging()
                if i.get("project") == MY_PROJECT_KEY]
    finally:
        mod.datetime = original


# ---- the container: a stamp in an unregistered file nudges forever-never -----

def test_my_repo_is_a_registered_primary_project():
    """Third silent-failure surface, invisible from inside the repo being
    stamped: the scanner only walks primary_projects()."""
    mod = _load_briefing()
    projects = mod.primary_projects()
    assert MY_PROJECT_KEY in projects, (
        f"{MY_PROJECT_KEY!r} not in primary_projects(); keys are CAPITALISED and "
        f"case-sensitive. Present: {sorted(projects)}"
    )
    assert Path(projects[MY_PROJECT_KEY]["claude_md"]).resolve() == CLAUDE_MD.resolve()


# ---- the content: my asks actually come back from HIS function ---------------

def test_my_asks_surface_from_the_real_scanner_once_aged():
    mod = _load_briefing()
    mine = _scan_with_clock_ahead(mod)
    assert mine, (
        "the real scanner returned NOTHING for this project even with the clock "
        "advanced — a Decision Queue item lost one of the four conditions"
    )
    texts = " || ".join(str(i.get("text", "")) for i in mine)
    for expected in ("Production flip", "hypothesisdriven.org DNS",
                     "Big-Questions figures", "Q5 figure"):
        assert expected in texts, f"{expected!r} no longer surfaces: {texts[:400]}"


def test_items_do_not_surface_before_seven_days():
    """Condition 4, and the reason the stamps are today's date: they must stay
    quiet through Kleiber's 9/14 batch and race week."""
    mod = _load_briefing()
    assert _scan_with_clock_ahead(mod, days=0) == []


# ---- the bite: a check that has never failed is theatre ----------------------

@pytest.mark.parametrize("break_it,label", [
    (lambda s: s.replace("(added: 2026-09-09) — open since",
                         "(added: 2026-09-09; note) — open since"),
     "semicolon inside the stamp parens"),
    (lambda s: s.replace("- [ ] **hypothesisdriven.org DNS cutover**",
                         "- **hypothesisdriven.org DNS cutover**"),
     "checkbox prefix removed"),
])
def test_bite_each_condition_is_load_bearing(break_it, label, tmp_path):
    """Break one condition at a time on a COPY and confirm the DNS row stops
    surfacing. Never mutates the real CLAUDE.md."""
    mod = _load_briefing()
    original = CLAUDE_MD.read_text(encoding="utf-8")
    broken = break_it(original)
    assert broken != original, f"bite {label!r} did not change the file"
    backup = tmp_path / "CLAUDE.md.bak"
    backup.write_text(original, encoding="utf-8")
    try:
        CLAUDE_MD.write_text(broken, encoding="utf-8")
        texts = " || ".join(str(i.get("text", ""))
                            for i in _scan_with_clock_ahead(mod))
        assert "hypothesisdriven.org DNS" not in texts, (
            f"bite {label!r} did NOT break the nudge — the condition is not "
            "load-bearing, or the scanner changed"
        )
    finally:
        CLAUDE_MD.write_text(backup.read_text(encoding="utf-8"), encoding="utf-8")
        assert CLAUDE_MD.read_text(encoding="utf-8") == original


def test_the_real_file_is_restored_and_still_conformant():
    mod = _load_briefing()
    assert _scan_with_clock_ahead(mod), "CLAUDE.md not restored after the bites"

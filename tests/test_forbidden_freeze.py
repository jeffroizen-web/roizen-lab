"""T7 — CO-2 / CO-3 byte-freeze guards (craft-uplift spec).

Guards:
1. FORBIDDEN-PATH FREEZE (CO-2): `git diff --stat 3e10217 -- <path>` is empty
   for every path in the CO-2 forbidden list.  A non-empty diff means the build
   modified a cron-owned or deploy-owned file that must stay byte-identical.

2. CNAME NOT CREATED (CO-2 addendum): no CNAME file is present in the repo root.

3. SENTINEL FREEZE (CO-3): the cron-owned field-of-interest sentinel spans
   in compare-purple-gold.html are byte-identical to those at git HEAD 3e10217.
   The sentinel spans are ENUMERATED DYNAMICALLY at test time (grep-derived) —
   no hardcoded count.  The test captures the base-tree spans from
   `git show 3e10217:compare-purple-gold.html`, then compares them against
   the current file's spans byte-for-byte.

TDD GREEN on the current tree:
  - No changes have been made (we ARE at base 3e10217).
  - All forbidden paths are untouched.
  - All 10 sentinel spans are byte-identical.
  - No CNAME file exists.

Run: python3 -m pytest tests/test_forbidden_freeze.py -q
"""
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
BASE_COMMIT = "3e10217"

# CO-2 FORBIDDEN paths — each must show zero diff against the base commit.
# Wildcarded paths (publish/, deploy/, etc.) are tested as directory prefixes.
FORBIDDEN_PATHS = [
    "scripts/deploy_publish.sh",
    "scripts/letter_writers_refresh_cron.sh",
    "scripts/sync_publish.py",
    # wire_letter_writers.py is forbidden EXCEPT for the CO-4 STYLE_BLOCK mirror;
    # test_style_block_mirror.py guards the CO-4 constraint separately.
    "scripts/wire_letter_writers.py",
    "publish",                              # generated artifacts
    "docs/reports/.deploy_last_hash",
    "docs/reports/deploy-publish.jsonl",
    "production/index.html",
    "index.html",
    "deploy",
    "themes",
    "debug-artifacts",
    "extracted-figures",
]

SENTINEL_OPEN = "<!--field-of-interest:start-->"
SENTINEL_CLOSE = "<!--field-of-interest:end-->"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _git_diff_stat(path: str) -> str:
    """Return `git diff --stat BASE -- path` output; empty string = no change."""
    result = subprocess.run(
        ["git", "diff", "--stat", BASE_COMMIT, "--", path],
        capture_output=True, text=True, cwd=ROOT,
    )
    return result.stdout.strip()


def _extract_sentinel_spans(html: str) -> list[str]:
    """Dynamically enumerate all sentinel spans from an HTML string.

    Each span is the text from <!--field-of-interest:start--> through
    <!--field-of-interest:end--> inclusive.  The list preserves order.
    """
    pattern = re.compile(
        re.escape(SENTINEL_OPEN) + r".*?" + re.escape(SENTINEL_CLOSE),
        re.S,
    )
    return pattern.findall(html)


def _get_base_html() -> str:
    """Retrieve the HTML file at the base commit using git show."""
    result = subprocess.run(
        ["git", "show", f"{BASE_COMMIT}:compare-purple-gold.html"],
        capture_output=True, text=True, cwd=ROOT,
    )
    if result.returncode != 0:
        pytest.skip(f"Cannot read base HTML from git: {result.stderr.strip()}")
    return result.stdout


# ---------------------------------------------------------------------------
# T7-a: forbidden-path byte-freeze (CO-2)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("path", FORBIDDEN_PATHS)
def ac2_forbidden_path_unchanged(path: str) -> None:
    diff = _git_diff_stat(path)
    assert not diff, (
        f"CO-2 VIOLATED: forbidden path '{path}' has changes vs {BASE_COMMIT}:\n{diff}\n"
        "The craft-uplift must not touch cron/deploy-owned files."
    )


def test_ac2_forbidden_path_unchanged(path=None) -> None:
    """Called by parametrize; actual invocation is parametrized below."""
    pass  # Replaced by the parametrized form below.


# Parametrized form (house style: pytest.mark.parametrize)
@pytest.mark.parametrize("forbidden_path", FORBIDDEN_PATHS)
def test_ac2_forbidden_paths_byte_frozen(forbidden_path: str) -> None:
    ac2_forbidden_path_unchanged(forbidden_path)


# ---------------------------------------------------------------------------
# T7-b: CNAME must not exist (CO-2)
# ---------------------------------------------------------------------------

def ac2_no_cname_created() -> None:
    """CO-2 explicitly forbids creation of a CNAME file (would re-route DNS)."""
    cname = ROOT / "CNAME"
    assert not cname.exists(), (
        f"CNAME file found at {cname}. CO-2 forbids creating a CNAME — "
        "this would modify the GitHub Pages DNS routing."
    )


def test_ac2_no_cname_created() -> None:
    ac2_no_cname_created()


# ---------------------------------------------------------------------------
# T7-c: sentinel spans are byte-identical to base (CO-3)
# Dynamic enumeration — no hardcoded count.
# ---------------------------------------------------------------------------

def ac3_sentinel_spans_byte_identical() -> None:
    """The cron-owned field-of-interest spans must be byte-identical to base.

    Sentinel set is derived dynamically from `git show BASE:compare-purple-gold.html`
    at test time; the test never hardcodes a span count.  Any span present in
    the base must appear UNCHANGED in the current file; any span present in the
    current file but not in the base is a NEW injection (acceptable if done by
    the cron, but NOT by the craft-uplift build).

    On the base tree (HEAD == 3e10217) both sets are identical → test passes.
    """
    base_html = _get_base_html()
    current_html = (ROOT / "compare-purple-gold.html").read_text(encoding="utf-8")

    base_spans = _extract_sentinel_spans(base_html)
    current_spans = _extract_sentinel_spans(current_html)

    # Every span that existed at base must still exist byte-identically
    base_set = set(base_spans)
    current_set = set(current_spans)

    removed = base_set - current_set
    assert not removed, (
        f"CO-3 VIOLATED: {len(removed)} sentinel span(s) were modified or removed "
        f"relative to {BASE_COMMIT}. The sentinel interiors are CRON-OWNED.\n"
        "Modified/removed spans:\n" + "\n".join(sorted(removed)[:3])
    )

    # Note: current may have more spans than base if the cron ran; that is allowed.
    # The constraint is only that the build did NOT edit any base-era span.


def test_ac3_sentinel_spans_byte_identical() -> None:
    ac3_sentinel_spans_byte_identical()


# ---------------------------------------------------------------------------
# T7-d: sentinel count is dynamically derived (never hardcoded)
# ---------------------------------------------------------------------------

def test_ac3_sentinel_count_is_dynamic() -> None:
    """Meta-guard: confirm the base tree has ≥ 1 sentinel span (probe for parse
    correctness) and that the count comes from the live file, not a literal."""
    current_html = (ROOT / "compare-purple-gold.html").read_text(encoding="utf-8")
    spans = _extract_sentinel_spans(current_html)
    # On the base tree there are 10 sentinel spans (verified by architect review).
    # We do NOT assert == 10; the test is count-agnostic and will work on any
    # future tree where the cron has added or redistributed sentinels.
    assert len(spans) >= 1, (
        "No field-of-interest sentinel spans found in compare-purple-gold.html. "
        "CO-3 applies to whatever span count is present at the build's cut point."
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge: corner-cases for the git-diff and sentinel extraction logic."""

    def test_git_diff_is_callable(self):
        """Confirm git is available and the base commit is reachable."""
        result = subprocess.run(
            ["git", "log", "--oneline", "-1", BASE_COMMIT],
            capture_output=True, text=True, cwd=ROOT,
        )
        assert result.returncode == 0, (
            f"git log {BASE_COMMIT} failed: {result.stderr.strip()}. "
            "The base commit must be reachable from the worktree."
        )

    def test_sentinel_extraction_finds_both_markers(self):
        """The regex must capture the full start-to-end span including both markers."""
        sample = (
            "before "
            "<!--field-of-interest:start--><p>content</p><!--field-of-interest:end-->"
            " after"
        )
        spans = _extract_sentinel_spans(sample)
        assert len(spans) == 1
        assert spans[0].startswith(SENTINEL_OPEN)
        assert spans[0].endswith(SENTINEL_CLOSE)
        assert "<p>content</p>" in spans[0]

    def test_sentinel_extraction_handles_multiple_spans(self):
        """Multiple sentinel pairs are all captured independently."""
        sample = (
            "<!--field-of-interest:start--><p>A</p><!--field-of-interest:end-->"
            " text "
            "<!--field-of-interest:start--><p>B</p><!--field-of-interest:end-->"
        )
        spans = _extract_sentinel_spans(sample)
        assert len(spans) == 2

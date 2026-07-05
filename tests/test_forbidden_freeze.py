"""T7 — CO-2 / CO-3 byte-freeze guards (craft-uplift spec).

Guards:
1. FORBIDDEN-PATH FREEZE (CO-2): `git diff --stat 3e10217 -- <path>` is empty
   for every path in the CO-2 forbidden list.  A non-empty diff means the build
   modified a cron-owned or deploy-owned file that must stay byte-identical.

2. CNAME NOT CREATED (CO-2 addendum): no CNAME file is present in the repo root.

3. SENTINEL EMITTER-PROVENANCE (CO-3): the field-of-interest sentinel spans in
   compare-purple-gold.html must be EXACTLY what wire_letter_writers.py emits for
   the current docs/letter_writers.json (structural well-formedness is the cheap
   first assert). Re-baselined 2026-07-05 (Kleiber MSG-cc0950 / MSG-18e49f) from
   the former byte-identity-to-3e10217 check, which was cron-fragile — it went red
   the moment the letter-writer cron wrote new data. Provenance is both
   cron-refresh-proof and hand-edit-proof (only the emitter may write interiors).
   CO-4 (base-pinned confined-diff) retired same day; T6 mirror stays standing.

TDD GREEN on the current tree:
  - All forbidden paths are untouched.
  - Every sentinel span matches the emitter output for the current data.
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
    # wire_letter_writers.py: NOT in the full byte-freeze list — CO-4 permits
    # STYLE_BLOCK mirror edits; test_wire_letter_writers_diff_confined_to_style_block
    # below enforces that any diff is CONFINED to the STYLE_BLOCK region, and
    # test_style_block_mirror.py guards mirror consistency (D-2 fix, gate
    # amendment 2026-07-05 per delta CO-4 authority).
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

def ac3_sentinel_spans_match_emitter() -> None:
    """CO-3 (emitter-provenance): the field-of-interest sentinel spans in the
    canonical must be EXACTLY what wire_letter_writers.py emits for the CURRENT
    docs/letter_writers.json.

    This replaces the former byte-identity-to-BASE_COMMIT check (Kleiber guard
    re-baseline 2026-07-05, MSG-cc0950 / MSG-18e49f). Byte-identity-to-base was
    cron-FRAGILE — it went red the moment the letter-writer cron did its job and
    wrote new data into the spans. Emitter-provenance is hardened in BOTH
    directions: cron-refresh-proof (the cron writes via this same emitter, so a
    legit refresh always matches) AND build/hand-edit-proof (an edit to a span
    interior diverges from the emitter output → caught; the who-may-write
    invariant a structural-only check would lose).
    """
    import sys
    import json

    sys.path.insert(0, str(ROOT / "scripts"))
    import wire_letter_writers as wlw

    current_html = (ROOT / "compare-purple-gold.html").read_text(encoding="utf-8")
    current_spans = _extract_sentinel_spans(current_html)

    # Cheap first assert: structural well-formedness (sentinel-bounded foi <p>).
    assert current_spans, "CO-3: no field-of-interest sentinel spans found."
    for span in current_spans:
        assert span.startswith(SENTINEL_OPEN) and span.endswith(SENTINEL_CLOSE), (
            "CO-3: a sentinel span is not fully sentinel-bounded."
        )
        assert '<p class="field-of-interest' in span, (
            "CO-3: a sentinel span is missing its field-of-interest <p>."
        )

    # Provenance assert: re-emit via the generator on the CURRENT data; the
    # canonical's spans must equal the emitter's output (only the emitter writes
    # span interiors). A hand edit to any interior diverges here and fails.
    if not wlw.DATA.exists():
        pytest.skip(f"letter-writer data not present: {wlw.DATA}")
    data = json.loads(wlw.DATA.read_text(encoding="utf-8"))
    reemitted_html, _, _ = wlw.wire(current_html, data)
    reemitted_spans = _extract_sentinel_spans(reemitted_html)
    assert current_spans == reemitted_spans, (
        "CO-3 (provenance) VIOLATED: the canonical field-of-interest spans differ "
        "from wire_letter_writers.py's emitter output for the current data. Only "
        "the emitter may write span interiors — a hand edit or drift was detected."
    )


def test_ac3_sentinel_spans_match_emitter() -> None:
    ac3_sentinel_spans_match_emitter()


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


# ---------------------------------------------------------------------------
# CO-4 RETIRED (2026-07-05, Kleiber guard re-baseline MSG-cc0950 / MSG-18e49f).
# The base-pinned test_wire_letter_writers_diff_confined_to_style_block was a
# one-shot pipe4-BUILD-window guard (asserting generator changes stay confined
# to STYLE_BLOCK vs 3e10217). That build is merged / accepted / live, and the
# F1 increment legitimately changes the emitter (inline style -> a semantic
# .person-pubcount class). The STANDING generator guard is
# test_style_block_mirror.py (T6 mirror, token consistency); the span interiors
# are now guarded in both directions by CO-3 emitter-provenance above.
# ---------------------------------------------------------------------------

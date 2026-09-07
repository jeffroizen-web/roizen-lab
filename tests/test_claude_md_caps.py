"""CLAUDE.md house-limit gate — BLOCKING (Kleiber fleet ruling MSG-f76a07).

Asserts BOTH documented limits and FAILS the suite when either is exceeded:
  * CLAUDE.md total          <= 40,960 B
  * the "## Quick Status" live block <= 5,120 B

WHY THIS LIVES IN THE TEST BATTERY, not a gate script: this repo runs under
Jeff's standing "no remote push without Jeff", so a pre-push hook is the wrong
surface — over-cap text would sit in the tree for weeks before anything looked
at it. The suite runs on every increment, so that is where the check belongs.
Shape cited from the fleet ruling; deliberately NOT copied from a sibling repo
(repo-local gate scripts drift — the speclint / --touches precedent).

Properties, each earned by a receipt in the 2026-09-07 census:
 1. It BLOCKS. Pilot's gate warned at 40,000 and blocked only at 145,000, so a
    116.6KB CLAUDE.md rode green for weeks while the check told the truth every
    run. Anything that must not drift BLOCKS; warn is for what you will let drift.
 2. BOTH limits, each named in its own assertion, so a failure says WHICH cap
    broke. Edge enforced the total but not the sub-cap and read downstream as
    "the limits are enforced"; from outside, one-of-two looks like both.
 3. The Quick Status heading is matched by PREFIX, and a heading that cannot be
    found is a FINDING that fails — never silently 0 bytes. Kleiber's own census
    read triready as 0 B because its heading carries a date suffix, and a
    vacuous measurement is a perfect pass.
 4. Two-sided bite proof: each cap is padded ALONE and asserted red, including
    an over-cap Quick Status under a compliant total (what a total-only gate
    misses). See the bite tests below.
 5. Regions are re-measured FROM THE FILE, never from arithmetic carried in the
    caller's head. Ledger's trim script rejoined sections so that a whole
    heading was swallowed INTO Quick Status; the disagreement between the
    script's arithmetic and a from-file re-read is what surfaced it.

MEASUREMENT DEFINITION (stated so downstream readers cannot misread a number):
a section runs from its own heading line through the last line before the next
top-level `## ` heading, counted as UTF-8 bytes INCLUDING the heading line and
the newlines. Including the heading is the conservative side — it measures
slightly more than the body alone, so it can never under-report a breach.
"""
from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = ROOT / "CLAUDE.md"

TOTAL_CAP = 40_960
QUICK_STATUS_CAP = 5_120
QUICK_STATUS_PREFIX = "## Quick Status"


class HeadingNotFound(AssertionError):
    """Property 3: an unmatched heading is a FINDING, never a zero-byte pass."""


def measure_total(path: Path) -> int:
    """Total bytes, read from the file (property 5)."""
    return len(path.read_bytes())


def measure_section(path: Path, heading_prefix: str) -> tuple[str, int]:
    """Bytes of the section whose heading STARTS WITH heading_prefix.

    Prefix-matched so a heading with a date or status suffix still measures
    (property 3). Raises HeadingNotFound rather than returning 0 — a section we
    cannot locate is a finding, because 0 would silently pass every cap.
    Re-reads the file each call (property 5).
    """
    lines = path.read_text(encoding="utf-8").split("\n")
    start = None
    for i, line in enumerate(lines):
        if line.startswith(heading_prefix):
            start = i
            break
    if start is None:
        raise HeadingNotFound(
            f"no heading starting with {heading_prefix!r} in {path.name} — "
            "the section was renamed or removed. Fix the heading or this "
            "constant; do NOT treat an unmatched section as 0 bytes."
        )
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    body = "\n".join(lines[start:end])
    return lines[start], len(body.encode("utf-8"))


def section_text(path: Path, heading_prefix: str) -> str:
    """The section's actual text, for callers that need to inspect it.

    Exists because the obvious shortcut — slicing the document by the BYTE
    size returned above — is wrong the moment the file contains a multibyte
    character (this file is full of em-dashes and arrows), and overshoots into
    the following section. Caught by the boundary test below on its first run.
    """
    lines = path.read_text(encoding="utf-8").split("\n")
    start = next((i for i, l in enumerate(lines) if l.startswith(heading_prefix)), None)
    if start is None:
        raise HeadingNotFound(heading_prefix)
    end = next((j for j in range(start + 1, len(lines)) if lines[j].startswith("## ")),
               len(lines))
    return "\n".join(lines[start:end])


# ---- the two blocking assertions (property 1 + 2: both caps, each named) ----

def test_claude_md_total_within_house_cap():
    total = measure_total(CLAUDE_MD)
    assert total <= TOTAL_CAP, (
        f"CLAUDE.md TOTAL cap breached: {total:,} B > {TOTAL_CAP:,} B "
        f"(over by {total - TOTAL_CAP:,}). Archive fully-closed Instruction "
        "Register entries VERBATIM into session_archive.md under a dated "
        "header, then re-run. Never summarize on the way out — the text must "
        "stay greppable."
    )


def test_quick_status_block_within_sub_cap():
    heading, size = measure_section(CLAUDE_MD, QUICK_STATUS_PREFIX)
    assert size <= QUICK_STATUS_CAP, (
        f"Quick Status SUB-cap breached: {size:,} B > {QUICK_STATUS_CAP:,} B "
        f"(over by {size - QUICK_STATUS_CAP:,}) under heading {heading!r}. "
        "Quick Status is the live block only: current-stint headline, next "
        "queue, waits, canary. Narrative belongs in the Session Log; closed "
        "work belongs in session_archive.md."
    )


def test_quick_status_heading_is_present_and_prefix_matched():
    """Property 3: prove the section is actually FOUND, so the cap test above
    is measuring something real rather than passing vacuously."""
    heading, size = measure_section(CLAUDE_MD, QUICK_STATUS_PREFIX)
    assert heading.startswith(QUICK_STATUS_PREFIX)
    assert size > 0, "Quick Status measured 0 B — vacuous pass, investigate"


# ---- property 4: two-sided bite proof, each cap padded ALONE ----------------

def _write_variant(tmp_path: Path, *, pad_total: int = 0, pad_quick_status: int = 0) -> Path:
    """Write a padded copy, then RE-MEASURE FROM THAT FILE (property 5)."""
    lines = CLAUDE_MD.read_text(encoding="utf-8").split("\n")
    if pad_quick_status:
        for i, line in enumerate(lines):
            if line.startswith(QUICK_STATUS_PREFIX):
                lines.insert(i + 1, "- pad " + "x" * pad_quick_status)
                break
    if pad_total:
        lines.append("<!-- pad " + "y" * pad_total + " -->")
    variant = tmp_path / "CLAUDE.md"
    variant.write_text("\n".join(lines), encoding="utf-8")
    return variant


def test_bite_total_cap_fires_when_only_the_total_is_over(tmp_path):
    """Pad past the TOTAL cap while Quick Status stays compliant."""
    variant = _write_variant(tmp_path, pad_total=TOTAL_CAP)
    total = measure_total(variant)
    _, qs = measure_section(variant, QUICK_STATUS_PREFIX)
    assert total > TOTAL_CAP, f"bite did not breach the total: {total:,}"
    assert qs <= QUICK_STATUS_CAP, "this bite must isolate the TOTAL cap"


def test_bite_sub_cap_fires_under_a_compliant_total(tmp_path):
    """THE case a total-only gate misses: Quick Status over its sub-cap while
    the file total is still comfortably legal."""
    variant = _write_variant(tmp_path, pad_quick_status=QUICK_STATUS_CAP)
    total = measure_total(variant)
    _, qs = measure_section(variant, QUICK_STATUS_PREFIX)
    assert qs > QUICK_STATUS_CAP, f"bite did not breach the sub-cap: {qs:,}"
    assert total <= TOTAL_CAP, (
        "this bite must isolate the SUB-cap: the total has to stay legal, "
        f"got {total:,} B"
    )


def test_bite_unmatched_heading_is_a_finding_not_a_zero(tmp_path):
    """Property 3, proven: a renamed heading must RAISE, not measure 0."""
    variant = tmp_path / "CLAUDE.md"
    variant.write_text(CLAUDE_MD.read_text(encoding="utf-8").replace(
        QUICK_STATUS_PREFIX, "## Status Quo Vadis"), encoding="utf-8")
    with pytest.raises(HeadingNotFound):
        measure_section(variant, QUICK_STATUS_PREFIX)


def test_prefix_match_survives_a_heading_suffix(tmp_path):
    """The triready bug: a dated heading must still be measured, not missed."""
    variant = tmp_path / "CLAUDE.md"
    variant.write_text(CLAUDE_MD.read_text(encoding="utf-8").replace(
        QUICK_STATUS_PREFIX, QUICK_STATUS_PREFIX + " — 2026-09-07", 1),
        encoding="utf-8")
    heading, size = measure_section(variant, QUICK_STATUS_PREFIX)
    assert heading.endswith("2026-09-07") and size > 0


def test_section_boundary_is_not_swallowed_by_a_rejoin(tmp_path):
    """Ledger's receipt: a trim rejoin glued the NEXT heading inside Quick
    Status. Measuring from the file must stop at the next top-level heading."""
    section = section_text(CLAUDE_MD, QUICK_STATUS_PREFIX)
    following = [l for l in section.split("\n")[1:] if l.startswith("## ")]
    assert not following, f"Quick Status swallowed a heading: {following}"
    # and the measured size must agree with the text we just read back
    _, size = measure_section(CLAUDE_MD, QUICK_STATUS_PREFIX)
    assert size == len(section.encode("utf-8"))

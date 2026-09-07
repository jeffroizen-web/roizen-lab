"""Guards for scripts/archive_verify.py — the trim complement check.

Two-sided: it must FIRE on a real loss and must NOT fire on an in-place
rewrite. The second half is as load-bearing as the first — Ledger's naive form
produced seven false hits, all in-place rewrites, and a check that cries wolf
gets waved off, which is worse than not having one.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from archive_verify import find_losses, main, MIN_SUBSTANTIVE  # noqa: E402

BEFORE = "\n".join([
    "## Quick Status",
    "- a closed row with a distinctive sha d607729 and a print-font flag 8f85b87",
    "- a MIXED row: PR-3 WebGL still waits on Jeff, and PR-1 landed at 8678346",
    "- a row that will be reworded in place, keeping its meaning intact",
    "- short",
])


def test_fires_on_a_compressed_away_line():
    """The MIXED-row trap: live part kept, dead part dropped, archived nowhere."""
    live = "## Quick Status\n- PR-3 WebGL still waits on Jeff\n"
    archive = "- a closed row with a distinctive sha d607729 and a print-font flag 8f85b87\n"
    losses = find_losses(BEFORE, live, archive)
    assert len(losses) == 2, losses
    nums = [n for n, _ in losses]
    assert 3 in nums, "the compressed-away MIXED row must be flagged"


def test_silent_when_every_removed_line_is_archived():
    live = "## Quick Status\n- rewritten headline\n"
    archive = BEFORE  # everything moved verbatim
    assert find_losses(BEFORE, live, archive) == []


def test_does_not_flag_a_line_still_present_live():
    """In-place survival is not a loss."""
    live = BEFORE
    assert find_losses(BEFORE, live, "") == []


def test_short_structural_lines_are_ignored():
    """'short' (< MIN_SUBSTANTIVE) must never be reported as lost."""
    losses = find_losses(BEFORE, "", "")
    assert all(len(l.strip()) >= MIN_SUBSTANTIVE for _, l in losses)
    assert "short" not in [l.strip() for _, l in losses]


def test_exit_code_is_nonzero_on_loss_and_zero_when_clean(tmp_path, monkeypatch, capsys):
    """The script must BLOCK by exit code, not merely print."""
    import archive_verify as av
    monkeypatch.setattr(av, "_git_show", lambda ref, path: BEFORE)
    monkeypatch.setattr(av, "LIVE", tmp_path / "CLAUDE.md")
    monkeypatch.setattr(av, "ARCHIVE", tmp_path / "session_archive.md")

    (tmp_path / "CLAUDE.md").write_text("nothing here", encoding="utf-8")
    (tmp_path / "session_archive.md").write_text("", encoding="utf-8")
    assert av.main(["dummysha"]) == 1
    assert "NOT EMPTY" in capsys.readouterr().out

    (tmp_path / "session_archive.md").write_text(BEFORE, encoding="utf-8")
    assert av.main(["dummysha"]) == 0
    assert "EMPTY" in capsys.readouterr().out


def test_real_repo_trim_verifies_clean():
    """The live receipt: today's trim (3e27645 -> working tree) loses nothing."""
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "archive_verify.py"), "3e27645"],
        cwd=str(ROOT), capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "EMPTY" in proc.stdout

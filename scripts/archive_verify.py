#!/usr/bin/env python3
"""Complement check for a CLAUDE.md trim — proves nothing was lost.

    python3 scripts/archive_verify.py <sha-before-trim> [<sha-after>]

Compares the PRE-TRIM CLAUDE.md against the COMPLEMENT (live CLAUDE.md +
session_archive.md). For every substantive line removed, that line must be
present in one of them. Exit 0 when the difference is empty, 1 when it is not,
naming every loss with its pre-trim line number so it can be recovered from the
git object.

RUN IT BEFORE THE TRIM COMMIT. Then verification gates the landing and the
verify-then-delete ordering stops mattering, because nothing lands until the
check passes (Ledger's shape, MSG-b83829 via Kleiber MSG-2f9db4; shape cited,
implementation deliberately repo-local — sibling gate scripts drift).

WHY THIS AND NOT A PHRASE GREP (Kleiber MSG-bb7ded, corrected by MSG-2f9db4):
a phrase grep audits WHAT YOU MOVED, so it is structurally blind to what you
REPLACED or COMPRESSED. It passed Kleiber's own file while a 2,518-char register
row sat lost, and it passed this repo's 16 archived blocks while 9 pre-trim
lines were in neither file — PR-1/PR-2 shas, a CWV read-back, the Pages
root-cause breakdown. Probe SELECTION is itself a place to fool yourself: our
first pass picked a phrase for a register line that matched from a Decision
Queue section never touched, so a bad probe read as a pass.

THE DISCRIMINATOR IS LOAD-BEARING (Ledger's, and the reason this is usable):
a removed line is a LOSS only when it is in NEITHER file. A line rewritten IN
PLACE in the same commit is not a loss, and the naive form flags it — Ledger
got seven hits, all false. Without this clause a reader either panics or, worse,
learns to wave the check off.

THE CLASS — `archive-pointer-is-a-claim-not-evidence`: the dangerous entry is
not the CLOSED one, it is the MIXED one. A row with a live part and a dead part
invites you to keep the live part and drop the rest, and the drop is invisible
to any check that only audits what you moved.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE = ROOT / "CLAUDE.md"
ARCHIVE = ROOT / "session_archive.md"

# Lines shorter than this are structure (blank, "---", a bare heading) rather
# than content, and match incidentally all over the file. Substance is what we
# are protecting.
MIN_SUBSTANTIVE = 40


def _git_show(ref: str, path: str) -> str:
    proc = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"archive_verify: cannot read {ref}:{path}\n{proc.stderr.strip()}")
    return proc.stdout


def find_losses(before_text: str, live_text: str, archive_text: str,
                min_len: int = MIN_SUBSTANTIVE) -> list[tuple[int, str]]:
    """Substantive pre-trim lines present in NEITHER the live file nor the archive."""
    losses = []
    for n, line in enumerate(before_text.split("\n"), 1):
        if len(line.strip()) < min_len:
            continue
        if line not in live_text and line not in archive_text:
            losses.append((n, line))
    return losses


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("sha_before", help="commit BEFORE the trim")
    ap.add_argument("sha_after", nargs="?", default=None,
                    help="commit after the trim (default: the working tree)")
    ap.add_argument("--min-len", type=int, default=MIN_SUBSTANTIVE)
    args = ap.parse_args(argv)

    before = _git_show(args.sha_before, "CLAUDE.md")
    if args.sha_after:
        live = _git_show(args.sha_after, "CLAUDE.md")
        archive = _git_show(args.sha_after, "session_archive.md")
    else:
        live = LIVE.read_text(encoding="utf-8")
        archive = ARCHIVE.read_text(encoding="utf-8")

    losses = find_losses(before, live, archive, args.min_len)
    examined = sum(1 for l in before.split("\n") if len(l.strip()) >= args.min_len)

    print(f"archive_verify: {examined} substantive pre-trim lines examined "
          f"(>= {args.min_len} chars), base {args.sha_before}")
    if not losses:
        print("COMPLEMENT CHECK: EMPTY — every removed line is in the live file "
              "or the archive. Nothing lost.")
        return 0

    print(f"COMPLEMENT CHECK: NOT EMPTY — {len(losses)} line(s) in NEITHER file.\n")
    for n, line in losses:
        print(f"  [pre-trim L{n}] {line[:160]}")
    print(f"\nRecover verbatim from the git object, nothing is gone while the "
          f"commit exists:\n    git show {args.sha_before}:CLAUDE.md\n"
          "Append the lines to session_archive.md under a dated header, then re-run.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

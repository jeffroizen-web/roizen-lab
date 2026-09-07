#!/usr/bin/env python3
"""Trim-loss checker for CLAUDE.md — FINAL FORM (Kleiber MSG-b5bbdd).

    python3 scripts/archive_verify.py <sha-before-trim> [--head <ref>]

Proves that a CLAUDE.md trim lost nothing, by checking every substantive line
and every interior FACT-TOKEN from every VERSION in the window against the
corpus that may legitimately hold it. Exit 0 when clean, 1 when not.

RUN IT BEFORE THE TRIM COMMIT. Verification then gates the landing and the
verify-then-delete ordering stops mattering, because nothing lands until the
check passes.

Written in Python deliberately. The bash form of this check is BOOBY-TRAPPED:
`grep -Fxq "$line"` without `--` parses any line starting with '-' (i.e. every
register bullet) as an OPTION, exits 2, and a naive loop scores nonzero as
ABSENT — Tempo's first run produced 100+ false hits reading as catastrophic
loss. Python substring membership is immune, and no probe here can error into
looking like either a finding or a pass.

THE SEVEN CLAUSES, each paid for by somebody being wrong first:
 1. VERSIONS, not endpoints (Maestro). A two-endpoint diff cannot see a line
    CREATED and then REPLACED inside the window: it is in neither endpoint, so
    it is never examined. We walk every commit that touched CLAUDE.md in the
    range, plus the working tree.
 2. Corpus = live ∪ archive ∪ COMMITTED DOCS (Ledger). Content legitimately
    lives in docs/ too; live-OR-archive alone calls those losses, and
    "recovering" them re-bloats the file the trim existed to shrink. We print
    WHERE each hit was found.
 3. TWO GRANULARITIES (Pilot). The line pass over-reports compressed text —
    Pilot got 42 line hits and the in-place discriminator would have tempted
    them to wave all 42 off, while buried inside were shas, file paths, MSG ids
    and env vars recorded NOWHERE else. So a second pass runs at FACT-TOKEN
    granularity, which survives paraphrase.
 4. The discriminator cuts BOTH ways (Ledger). A removed line is a LOSS only
    when in NEITHER — in-place rewrites are false positives. But a token that
    is a FILE PATH needs exists(), not text membership: a file does not contain
    its own path, and Kleiber's token pass flagged six records that were all
    present on disk and merely no longer cited.
 5. Narrow an unmatched line to CLAUSE FRAGMENTS before reporting it (Ledger).
    Printing a 2,500-character bullet whole is technically true and unreadable,
    which is how a check gets waved off.
 6. NO STRING CHECK CAN DECIDE whether a fact survived IN OTHER WORDS. That is
    a human read. This tool says so out loud rather than implying otherwise.
 7. INVERSE DIRECTION (Ledger), which no membership check catches: a standing
    RULE swept INTO the archive inside the dead status text it sat in is not
    LOST and is functionally GONE, because a fresh session reads CLAUDE.md, not
    the archive. We flag archived blocks carrying rule-shaped language for a
    human decision.

CLASS: `archive-pointer-is-a-claim-not-evidence`. The trap in all five faces of
it is the MIXED entry — a row with a live part and a dead part invites you to
keep the live part and drop the rest, and the drop is invisible to any check
that only audits what you nominated to move.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE_NAME = "CLAUDE.md"
ARCHIVE_NAME = "session_archive.md"

MIN_SUBSTANTIVE = 40

# Interior facts that survive paraphrase. A sentence can be rewritten freely;
# a sha or a message id cannot be, so its disappearance is real signal.
TOKEN_PATTERNS = {
    "sha":     re.compile(r"\b[0-9a-f]{7,40}\b"),
    "msg-id":  re.compile(r"\bMSG-[0-9a-f]{6}\b"),
    "path":    re.compile(r"\b(?:scripts|tests|docs|production)/[\w./-]+\b"),
    "url":     re.compile(r"https?://[^\s<>()\"'`]+"),
    "env-var": re.compile(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+){1,}\b"),
}
# Words that are ALL_CAPS_WITH_UNDERSCORES but are prose emphasis, not env vars.
ENV_NOISE = {"PASS_WITH_FLAG", "WAITING_ON", "NOT_EMPTY", "READ_BACK"}

RULE_MARKERS = re.compile(
    r"\b(ALWAYS|NEVER|do NOT|DO NOT|must not|MUST|standing|Standing|"
    r"never silently|reserved|forbidden)\b")


def _git(*args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=str(ROOT),
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"archive_verify: git {' '.join(args)} failed\n{proc.stderr.strip()}")
    return proc.stdout


def _show(ref: str, path: str) -> str | None:
    proc = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=str(ROOT),
                          capture_output=True, text=True)
    return proc.stdout if proc.returncode == 0 else None


def versions_in_window(sha_before: str, head: str) -> list[str]:
    """Clause 1: every commit that touched CLAUDE.md in the window, oldest
    first, so a line created AND replaced inside the window is still examined."""
    out = _git("rev-list", "--reverse", f"{sha_before}^..{head}", "--", LIVE_NAME)
    return [sha_before] + [l for l in out.split("\n") if l.strip()]


def build_corpus(head: str) -> dict[str, str]:
    """Clause 2: live ∪ archive ∪ committed docs. Keyed by where it was found.

    Honours `head`: with the default "HEAD" the WORKING TREE is read, which is
    what you want when verifying a trim BEFORE committing it. With an explicit
    ref the corpus is read AT THAT REF, so a historical pair can be audited
    honestly. Reading the working tree while claiming to audit an old ref made
    this checker silently pass a known loss — caught by the historical bite
    test, which is precisely why that test uses a real defect and not a fixture.
    """
    corpus: dict[str, str] = {}
    at_ref = head != "HEAD"

    for name in (LIVE_NAME, ARCHIVE_NAME):
        if at_ref:
            text = _show(head, name)
            if text is not None:
                corpus[name] = text
        else:
            p = ROOT / name
            if p.exists():
                corpus[name] = p.read_text(encoding="utf-8")

    listing = _git("ls-tree", "-r", "--name-only", head, "docs") if at_ref \
        else _git("ls-files", "docs")
    for rel in listing.split("\n"):
        rel = rel.strip()
        if not rel.endswith((".md", ".json", ".txt")):
            continue
        if at_ref:
            text = _show(head, rel)
            if text is not None:
                corpus[rel] = text
        else:
            p = ROOT / rel
            if p.exists():
                try:
                    corpus[rel] = p.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    pass
    return corpus


def locate(needle: str, corpus: dict[str, str]) -> str | None:
    for where, text in corpus.items():
        if needle in text:
            return where
    return None


def clause_fragments(line: str, limit: int = 3) -> list[str]:
    """Clause 5: narrow a long bullet to readable fragments."""
    parts = [p.strip() for p in re.split(r"[;.]\s+|\s+—\s+|\s+\|\s+", line) if p.strip()]
    parts = [p for p in parts if len(p) >= 25] or [line]
    return parts[:limit]


def extract_tokens(text: str) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {k: set() for k in TOKEN_PATTERNS}
    for kind, pat in TOKEN_PATTERNS.items():
        for m in pat.findall(text):
            if kind == "sha" and not re.search(r"[0-9]", m):
                continue          # all-letter words like "deadbeef" prose
            if kind == "sha" and len(m) < 7:
                continue
            if kind == "env-var" and (m in ENV_NOISE or len(m) < 8):
                continue
            found[kind].add(m)
    return found


def run(sha_before: str, head: str) -> int:
    versions = versions_in_window(sha_before, head)
    corpus = build_corpus(head)

    print(f"archive_verify FINAL FORM — base {sha_before}, head {head}")
    print(f"  versions walked : {len(versions)} (clause 1: versions, not endpoints)")
    print(f"  corpus surfaces : {len(corpus)} "
          f"(live + archive + {len(corpus) - 2} committed docs)")

    # ---- pass 1: line complement over every version ------------------------
    line_losses: dict[str, tuple[str, int]] = {}
    seen_lines: set[str] = set()
    for ref in versions:
        text = _show(ref, LIVE_NAME)
        if text is None:
            continue
        for n, line in enumerate(text.split("\n"), 1):
            if len(line.strip()) < MIN_SUBSTANTIVE or line in seen_lines:
                continue
            seen_lines.add(line)
            if locate(line, corpus) is None:
                line_losses[line] = (ref[:7], n)

    # ---- pass 2: interior fact-tokens over every version -------------------
    token_losses: list[tuple[str, str, str]] = []   # (kind, token, first-seen ref)
    seen_tokens: set[tuple[str, str]] = set()
    for ref in versions:
        text = _show(ref, LIVE_NAME)
        if text is None:
            continue
        for kind, toks in extract_tokens(text).items():
            for tok in toks:
                if (kind, tok) in seen_tokens:
                    continue
                seen_tokens.add((kind, tok))
                if kind == "path":
                    # Clause 4, the other edge: a file does not contain its own
                    # path. Presence on disk is what matters, not citation.
                    if (ROOT / tok).exists():
                        continue
                    if locate(tok, corpus) is not None:
                        continue
                    token_losses.append((kind, tok, ref[:7]))
                else:
                    if locate(tok, corpus) is None:
                        token_losses.append((kind, tok, ref[:7]))

    print(f"  lines examined  : {len(seen_lines)}")
    print(f"  tokens examined : {len(seen_tokens)}")
    print()

    ok = True
    if line_losses:
        ok = False
        print(f"LINE COMPLEMENT: NOT EMPTY — {len(line_losses)} line(s) in no surface.\n")
        for line, (ref, n) in line_losses.items():
            print(f"  [{ref} L{n}]")
            for frag in clause_fragments(line):
                print(f"      · {frag[:150]}")
    else:
        print("LINE COMPLEMENT: EMPTY — every substantive line from every version "
              "is in the live file, the archive, or committed docs.")

    if token_losses:
        ok = False
        print(f"\nFACT-TOKENS: NOT EMPTY — {len(token_losses)} token(s) in no surface.\n")
        for kind, tok, ref in sorted(token_losses):
            print(f"  {kind:8} {tok:<48} (first seen {ref})")
    else:
        print("FACT-TOKENS: EMPTY — every sha, MSG-id, path, URL and env var "
              "from every version is still recorded somewhere.")

    # ---- clause 7: the inverse direction -----------------------------------
    archive = corpus.get(ARCHIVE_NAME, "")
    live = corpus.get(LIVE_NAME, "")
    swept: list[str] = []
    for block in archive.split("\n"):
        if len(block.strip()) < MIN_SUBSTANTIVE or not RULE_MARKERS.search(block):
            continue
        if block not in live:
            swept.append(block)
    print(f"\nINVERSE (clause 7) — archived blocks carrying RULE-shaped language "
          f"and NOT also stated live: {len(swept)}")
    if swept:
        print("  A standing rule swept into the archive is not LOST but is functionally")
        print("  GONE: a fresh session reads CLAUDE.md, not the archive. HUMAN CALL —")
        print("  for each, decide whether the rule still binds and if so restate it live.")
        for b in swept[:12]:
            print(f"    · {clause_fragments(b)[0][:150]}")
        if len(swept) > 12:
            print(f"    … and {len(swept) - 12} more")

    print("\nCLAUSE 6 — what this tool CANNOT decide: whether a fact survived IN")
    print("OTHER WORDS. Membership checks see strings, not meaning. An EMPTY result")
    print("means nothing was dropped verbatim; it does NOT certify that a paraphrase")
    print("kept the substance. That read stays human.")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("sha_before")
    ap.add_argument("--head", default="HEAD")
    args = ap.parse_args(argv)
    return run(args.sha_before, args.head)


if __name__ == "__main__":
    sys.exit(main())

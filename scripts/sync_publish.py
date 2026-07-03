#!/usr/bin/env python3
"""Assemble the lean GitHub Pages publish artifact from the canonical source.

WHY (Kleiber ruling, 2026-07-03): the serving tree must NOT be the 543M source
repo — ~293M of unused figure iterations + 27M of logo iterations choke the Pages
build (it hangs indefinitely). `publish/` is a DERIVED artifact: the byte-for-byte
canonical page + ONLY the assets the page actually references, in their relative
structure. A few MB → a fast, reliable Pages build. Deployed to the `gh-pages`
branch (Pages source), so main stays pure source.

This is regenerated mechanically — never hand-copied (a hand-copied publish dir
rots = the dual-path-drift class). Re-run after any content/asset change.
`tests/test_publish_sync.py` asserts publish/index.html == the canonical page by
hash + every referenced local asset is present.

Run:
    python3 scripts/sync_publish.py            # (re)build publish/
    python3 scripts/sync_publish.py --check    # build + fail if any asset missing
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "compare-purple-gold.html"
PUBLISH = ROOT / "publish"

_ASSET_RE = re.compile(r"\.(css|js|woff2|webp|png|jpe?g|svg|ico)$", re.I)


def referenced_assets(html: str) -> list:
    """Every LOCAL asset the page references (src/href/srcset/url()), relative."""
    refs = set()
    for m in re.finditer(r'(?:src|href|srcset|content)="([^"]+)"', html):
        for tok in m.group(1).split(","):
            refs.add(tok.strip().split(" ")[0])
    for m in re.finditer(r"url\('?([^')]+)'?\)", html):
        refs.add(m.group(1))
    out = set()
    for r in refs:
        if not r or r.startswith(("http://", "https://", "//", "#", "mailto:", "data:")):
            continue
        if _ASSET_RE.search(r):
            out.add(r.lstrip("/"))
    return sorted(out)


def build() -> list:
    """Rebuild publish/ from the canonical page. Returns the list of MISSING assets."""
    html = CANONICAL.read_text(encoding="utf-8")
    if PUBLISH.exists():
        shutil.rmtree(PUBLISH)
    PUBLISH.mkdir()
    # index.html is a byte-for-byte copy of the canonical page (the hash-match invariant).
    (PUBLISH / "index.html").write_bytes(CANONICAL.read_bytes())
    (PUBLISH / ".nojekyll").write_text("")
    missing = []
    for asset in referenced_assets(html):
        src = ROOT / asset
        if not src.exists():
            missing.append(asset)
            continue
        dst = PUBLISH / asset
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="exit nonzero if any asset missing")
    args = ap.parse_args()
    missing = build()
    n_files = sum(1 for p in PUBLISH.rglob("*") if p.is_file())
    total_kb = sum(p.stat().st_size for p in PUBLISH.rglob("*") if p.is_file()) // 1024
    print(f"publish/ built: {n_files} files, {total_kb} KB")
    if missing:
        print(f"MISSING (referenced but not on disk): {missing}", file=sys.stderr)
        return 1 if args.check else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

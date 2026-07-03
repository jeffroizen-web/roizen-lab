#!/usr/bin/env python3
"""Publish-artifact sync guard (deploy hardening, Kleiber ruling 2026-07-03).

publish/ is a DERIVED artifact assembled by scripts/sync_publish.py — the lean
GitHub Pages serving tree (the 543M source repo chokes the Pages build). These lock
it against dual-path-drift:
- publish/index.html is BYTE-FOR-BYTE the canonical page (hash match),
- every LOCAL asset the canonical page references is present in publish/,
- publish/ carries .nojekyll,
- publish/ excludes the heavy source dirs (no 293M extracted-figures tree).

Run: python3 -m pytest tests/test_publish_sync.py -q
"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import sync_publish as sp  # noqa: E402


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_publish_index_is_byte_identical_to_canonical():
    sp.build()
    canonical = ROOT / "compare-purple-gold.html"
    published = sp.PUBLISH / "index.html"
    assert published.exists(), "publish/index.html not generated"
    assert _sha(published) == _sha(canonical), \
        "publish/index.html drifted from the canonical page (regenerate via sync_publish.py)"


def test_all_referenced_local_assets_present():
    missing = sp.build()
    assert missing == [], f"referenced assets missing from publish/: {missing}"


def test_publish_has_nojekyll():
    sp.build()
    assert (sp.PUBLISH / ".nojekyll").exists(), "publish/.nojekyll missing (Pages would run Jekyll)"


def test_publish_excludes_heavy_source_tree():
    """The whole point: the 293M extracted-figures iteration tree must NOT be shipped
    wholesale — only the handful of referenced figures."""
    sp.build()
    figs = list((sp.PUBLISH).rglob("extracted-figures/**/*"))
    fig_files = [f for f in figs if f.is_file()]
    # The page references 4 figures (png+webp = 8 files); a wholesale copy would be hundreds.
    assert len(fig_files) < 40, f"publish/ shipped too many figures ({len(fig_files)}) — heavy tree leaked in"

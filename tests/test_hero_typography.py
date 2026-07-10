"""Hallmark gate 38a guard (Jeff "All" 2026-07-09).

Display/hero headings are ROMAN — no italic. An italicized emphasis word inside
an otherwise-upright hero heading (the `Built to <em>think</em>` pattern) is
Hallmark's single most reliable AI-generated tell, and here it also rendered
faux-slanted (no italic Merriweather face is loaded). Emphasis on the hero
headline is carried by the gold accent (`var(--accent)`), not slant.

INVARIANT: `<em>` is italic by the browser UA-default, so the hero em rule must
EXPLICITLY set `font-style: normal` to be roman — merely omitting a `font-style:
italic` declaration is NOT enough (it falls back to the UA default italic; the
rendered read-back caught exactly this). This guard therefore requires the
explicit normal override, and fails if a future edit re-italicizes it or drops
the override. Body-copy italic (running paragraphs) is allowed and untouched.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = (ROOT / "compare-purple-gold.html").read_text(encoding="utf-8")


def _rule_body(selector: str) -> str | None:
    """Return the declaration block for a CSS selector, or None if absent."""
    m = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", HTML)
    return m.group(1) if m else None


def test_hero_heading_em_is_roman_not_italic() -> None:
    body = _rule_body(".hero h1 em")
    assert body is not None, "`.hero h1 em` rule not found — verify the hero markup/CSS."
    assert "italic" not in body, (
        "Hallmark gate 38a: `.hero h1 em` sets font-style:italic — an italicized word "
        "in an upright hero heading is the #1 AI tell. Carry emphasis with the gold "
        "accent (var(--accent)) or weight, not slant. (Jeff 'All' 2026-07-09.)"
    )
    assert re.search(r"font-style:\s*normal", body), (
        "Hallmark gate 38a: `.hero h1 em` must EXPLICITLY set font-style:normal — <em> "
        "is italic by UA default, so omitting the declaration renders faux-slanted "
        "anyway. Keep `font-style: normal` on the hero em. (Jeff 'All' 2026-07-09.)"
    )

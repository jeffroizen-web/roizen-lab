"""Hallmark majors #2 + #3 guard — left editorial axis + earned eyebrow
(Rams design 2026-07-09 `lab-site-hallmark-majors-2-3-design`; Jeff "All").

The design principle: a confident LEFT editorial axis, with CENTERED reserved
for the one deliberate "moment" surface (Donate). This guard locks the intent
so a future edit cannot silently re-center the site or re-sprinkle eyebrows.

#3: `.section-header` is left; `.donate-section .section-header` is the centered
    exception; the hero block is left.
#2: exactly ONE rendered eyebrow ("Research" on Big Questions); the 3 bare-H2
    Rhythm-B sections (Team/News/Contact) carry no gold-line.
Tokens/palette/fonts unchanged (out of scope, Jeff-decided).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = (ROOT / "compare-purple-gold.html").read_text(encoding="utf-8")


def _rule_body(selector: str) -> str | None:
    m = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", HTML)
    return m.group(1) if m else None


def _rendered_html() -> str:
    """HTML with the commented-out (hidden) Gear section stripped."""
    return re.sub(r"<!-- Gear section HIDDEN.*?-->", "", HTML, flags=re.S)


def test_section_header_is_left_axis() -> None:
    body = _rule_body(".section-header")
    assert body is not None and "text-align: left" in body, (
        "#3: `.section-header` must be text-align:left (the confident left editorial "
        "axis). Re-centering the whole site is the templated-symmetry tell. (Rams 2-3.)"
    )


def test_donate_is_the_centered_exception() -> None:
    body = _rule_body(".donate-section .section-header")
    assert body is not None and "text-align: center" in body, (
        "#3: the Donate section-header must stay text-align:center — the ONE deliberate "
        "centered 'moment' exception against the global left axis. (Rams 2-3.)"
    )


def test_hero_block_is_left() -> None:
    body = _rule_body(".hero-inner")
    assert body is not None and "text-align: left" in body, (
        "#3: `.hero-inner` must be text-align:left — a full-left editorial hero clears "
        "Hallmark gate 6 (centered-hero auto-fail). (Rams 2-3.)"
    )


def test_exactly_one_rendered_eyebrow() -> None:
    n = len(re.findall(r'<p class="eyebrow">', _rendered_html()))
    assert n == 1, (
        f"#2: expected exactly 1 rendered eyebrow ('Research' on Big Questions), found {n}. "
        "Eyebrows are default-OFF, capped at the one earned chapter-opener — re-sprinkling "
        "them is the macrostructure-monotony tell. (Rams 2-3.)"
    )
    assert re.search(r'<p class="eyebrow">Research</p>', _rendered_html()), (
        "#2: the one surviving eyebrow must be 'Research' (Big Questions). (Rams 2-3.)"
    )


def test_rhythm_b_sections_have_no_gold_line() -> None:
    """Team/News/Contact are bare-H2 openers — no gold rule (the two-rhythm variety)."""
    for h2 in ["Our Team", "Lab News", "Get in Touch"]:
        # the gold-line, if present, would sit immediately before this h2
        assert not re.search(
            r'<div class="gold-line"></div>\s*<h2>' + re.escape(h2) + r"</h2>", HTML
        ), (
            f"#2: the Rhythm-B section with '<h2>{h2}</h2>' must NOT carry a gold-line "
            "(bare-H2 opener). (Rams 2-3.)"
        )

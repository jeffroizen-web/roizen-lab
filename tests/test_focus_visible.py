"""T3 — R-7 focus-visible universality guard (craft-uplift spec).

Guards:
- Every interactive element CLASS in the CSS has a corresponding :focus-visible rule.
- The interactive class set includes: elements with `a`, `button`, `input`,
  `textarea`, and `.skip-link` styling rules.
- The count of :focus-visible-covered classes exceeds the baseline of 2.
- No interactive type is missing focus-visible coverage.

TDD RED on the current tree: only 2 selectors have :focus-visible coverage
(.question-text .paper-link and .contact-info a). nav links, buttons, form
inputs/textarea, and skip-link are uncovered.

GREEN after the craft-uplift adds universal :focus-visible coverage to all
interactive element classes.

Run: python3 -m pytest tests/test_focus_visible.py -q
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "compare-purple-gold.html"

# Interactive element types that MUST have :focus-visible coverage after uplift.
# Each maps to a CSS selector fragment that should appear alongside :focus-visible.
REQUIRED_INTERACTIVE_TYPES = {
    "a": r"\ba\b",          # any `a` selector (nav links, general links)
    "button": r"\bbutton\b",
    "input": r"\binput\b",
    "textarea": r"\btextarea\b",
    "skip-link": r"\.skip-link",
}

BASELINE_FOCUS_VISIBLE_COUNT = 2  # count on the base tree (base spec verified)


def _get_style_block(html: str) -> str:
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    return m.group(1) if m else ""


def _extract_focus_visible_selectors(css: str) -> list[str]:
    """Return all selector strings that include :focus-visible."""
    # A :focus-visible rule is a CSS rule where the selector chain contains
    # :focus-visible and is followed by a { declarations } block.
    # We extract the selector portion before the { in such rules.
    rules = re.findall(r"([^{};]+):focus-visible\s*\{", css)
    return [r.strip() for r in rules]


@pytest.fixture(scope="module")
def style_block() -> str:
    return _get_style_block(HTML_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def focus_visible_selectors(style_block: str) -> list[str]:
    return _extract_focus_visible_selectors(style_block)


# ---------------------------------------------------------------------------
# T3-a: count exceeds baseline
# ---------------------------------------------------------------------------

def ac3_focus_visible_count_exceeds_baseline(selectors: list[str]) -> None:
    """The number of :focus-visible rules must exceed the baseline of 2.

    The baseline is 2 (base tree). After universal uplift, every interactive
    class has coverage → count >> 2.
    """
    assert len(selectors) > BASELINE_FOCUS_VISIBLE_COUNT, (
        f"Only {len(selectors)} :focus-visible rule(s) found (baseline = "
        f"{BASELINE_FOCUS_VISIBLE_COUNT}). Universal focus-visible coverage "
        f"requires all interactive element types to be covered."
    )


def test_ac3_focus_visible_count_exceeds_baseline(focus_visible_selectors: list[str]) -> None:
    ac3_focus_visible_count_exceeds_baseline(focus_visible_selectors)


# ---------------------------------------------------------------------------
# T3-b: each required interactive type has :focus-visible coverage
# ---------------------------------------------------------------------------

def ac3_all_interactive_types_have_focus_visible(
    selectors: list[str], style_block: str
) -> None:
    """Every required interactive type must appear in at least one :focus-visible rule."""
    # Build a combined string of all :focus-visible rule regions for matching.
    # Strategy: for each required type, check whether any :focus-visible selector
    # string in the CSS contains a pattern matching that type.
    missing: list[str] = []
    for type_name, pattern in REQUIRED_INTERACTIVE_TYPES.items():
        covered = any(re.search(pattern, sel, re.I) for sel in selectors)
        if not covered:
            missing.append(type_name)

    assert not missing, (
        f"Interactive types missing :focus-visible coverage: {missing}. "
        f"Add :focus-visible rules for each in the craft-uplift."
    )


def test_ac3_all_interactive_types_have_focus_visible(
    focus_visible_selectors: list[str], style_block: str
) -> None:
    ac3_all_interactive_types_have_focus_visible(focus_visible_selectors, style_block)


# ---------------------------------------------------------------------------
# T3-c: skip-link has :focus-visible (critical for keyboard accessibility)
# ---------------------------------------------------------------------------

def ac3_skip_link_has_focus_visible(selectors: list[str]) -> None:
    """The skip-link is the first keyboard-reachable element; it MUST have
    a :focus-visible rule so keyboard users can see it on Tab keypress."""
    covered = any(re.search(r"\.skip-link", sel) for sel in selectors)
    assert covered, (
        "'.skip-link' does not have a :focus-visible rule. "
        "The skip-link is the first tab stop — add a :focus-visible style so "
        "keyboard users can see it when it receives focus."
    )


def test_ac3_skip_link_has_focus_visible(focus_visible_selectors: list[str]) -> None:
    ac3_skip_link_has_focus_visible(focus_visible_selectors)


# ---------------------------------------------------------------------------
# T3-d: button has :focus-visible (theme toggle + contact submit)
# ---------------------------------------------------------------------------

def ac3_button_has_focus_visible(selectors: list[str]) -> None:
    """All buttons (theme-toggle, contact-submit, nav-toggle) must have
    :focus-visible styling."""
    covered = any(re.search(r"\bbutton\b", sel) for sel in selectors)
    assert covered, (
        "'button' selector missing :focus-visible rule. "
        "Buttons (theme-toggle, nav-toggle, contact submit) must show a visible "
        "focus indicator on keyboard navigation."
    )


def test_ac3_button_has_focus_visible(focus_visible_selectors: list[str]) -> None:
    ac3_button_has_focus_visible(focus_visible_selectors)


# ---------------------------------------------------------------------------
# T3-e: form inputs + textarea have :focus-visible
# ---------------------------------------------------------------------------

def ac3_form_controls_have_focus_visible(selectors: list[str]) -> None:
    """input and textarea elements must have :focus-visible rules."""
    for elem in ("input", "textarea"):
        covered = any(re.search(rf"\b{elem}\b", sel) for sel in selectors)
        assert covered, (
            f"'{elem}' selector missing :focus-visible rule. "
            f"Contact form {elem} elements must show a focus indicator."
        )


def test_ac3_form_controls_have_focus_visible(focus_visible_selectors: list[str]) -> None:
    ac3_form_controls_have_focus_visible(focus_visible_selectors)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge: validate :focus-visible selector extraction accuracy."""

    def test_focus_visible_selector_extraction_finds_existing(self, style_block: str):
        """The current tree has exactly 2 :focus-visible rules; extraction must
        find them (regression guard on the parsing logic itself)."""
        selectors = _extract_focus_visible_selectors(style_block)
        # Extraction-regression guard: the two selectors present at base
        # (3e10217) must always be found; the LIVE count grows under AC-3,
        # so assert superset-of-base, never an exact live count (D-1 fix,
        # gate amendment 2026-07-05 per delta authority).
        base_selectors = {".paper-link", ".contact-info"}
        # boundary-aware match: the base class must appear as a whole compound
        # anywhere in some selector (substring matching passed a renamed
        # .paper-link-bitten and final-compound matching missed ancestor
        # position .contact-info a - both bite-caught 2026-07-05)
        joined = " || ".join(selectors)
        missing = {
            b for b in base_selectors
            if not re.search(re.escape(b) + r"(?![\w-])", joined)
        }
        assert not missing, (
            f"Extraction lost base selectors {missing}; extracted={selectors}"
        )
        assert len(selectors) >= BASELINE_FOCUS_VISIBLE_COUNT

    def test_focus_visible_selector_extraction_is_accurate(self, style_block: str):
        """The extracted selectors should contain the known base-tree entries
        (.paper-link and .contact-info a) — confirms the parser works."""
        selectors = _extract_focus_visible_selectors(style_block)
        combined = " ".join(selectors)
        # One of the two known base-tree :focus-visible rules must appear
        has_known = re.search(r"paper-link|contact-info", combined)
        assert has_known, (
            f":focus-visible selector extraction missed known base-tree rules. "
            f"Got: {selectors}"
        )

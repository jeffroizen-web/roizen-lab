"""T4 — B-1 print-stylesheet existence and key-rules guard (craft-uplift spec).

Guards (all of these ALREADY exist on the base tree — this test is GREEN
on the current tree and serves as a non-regression lock):

1. @media print block exists in the page <style>.
2. Non-essential elements are hidden: .navbar, .theme-toggle, .contact-form.
3. Body is forced to black text on white background.
4. Link URL-append rule is present: a[href^="http"]::after { content: " (" attr(href) ")" }.
5. page-break-inside: avoid on .question-row, .pub-arc, and .team-card.
6. At least one major section has page-break-before: always.

TDD GREEN on the current tree: the print block already satisfies all six guards.
This test prevents regression (the craft-uplift must not weaken the print block
while also not rewarding false additions — B-1 rubric line #10).

Run: python3 -m pytest tests/test_print_stylesheet.py -q
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "compare-purple-gold.html"

MAJOR_SECTIONS = ["#questions", "#publications", "#team", "#alumni"]
PAGE_BREAK_INSIDE_ELEMENTS = [".question-row", ".pub-arc", ".team-card"]
HIDDEN_ELEMENTS = [".navbar", ".theme-toggle", ".contact-form"]


def _get_style_block(html: str) -> str:
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    return m.group(1) if m else ""


def _extract_print_block(css: str) -> str:
    """Return the content of @media print { … } using brace matching."""
    start = css.find("@media print")
    if start == -1:
        return ""
    try:
        brace_i = css.index("{", start)
    except ValueError:
        return ""
    depth = 0
    j = brace_i
    while j < len(css):
        if css[j] == "{":
            depth += 1
        elif css[j] == "}":
            depth -= 1
            if depth == 0:
                return css[start : j + 1]
        j += 1
    return ""


@pytest.fixture(scope="module")
def style_block() -> str:
    return _get_style_block(HTML_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def print_block(style_block: str) -> str:
    return _extract_print_block(style_block)


# ---------------------------------------------------------------------------
# T4-a: @media print block exists
# ---------------------------------------------------------------------------

def ac4_print_block_exists(block: str) -> None:
    """The page must contain a non-empty @media print { … } block."""
    assert block.strip(), (
        "@media print block not found in compare-purple-gold.html. "
        "B-1 requires a print stylesheet for tenure-packet printing."
    )


def test_ac4_print_block_exists(print_block: str) -> None:
    ac4_print_block_exists(print_block)


# ---------------------------------------------------------------------------
# T4-b: non-essential elements are hidden
# ---------------------------------------------------------------------------

def ac4_non_essential_elements_hidden(block: str) -> None:
    """Navigation and chrome elements must be display:none in the print block."""
    for selector in HIDDEN_ELEMENTS:
        # The selector must appear in a rule that assigns display:none
        # (either directly or in a combined rule)
        pattern = re.compile(
            r"(?:[^{]*" + re.escape(selector) + r"[^{]*)\{[^}]*display\s*:\s*none",
            re.S,
        )
        assert pattern.search(block), (
            f"'{selector}' is not hidden (display:none) in @media print. "
            f"Non-essential chrome must be suppressed for printing."
        )


def test_ac4_non_essential_elements_hidden(print_block: str) -> None:
    ac4_non_essential_elements_hidden(print_block)


# ---------------------------------------------------------------------------
# T4-c: body forced to black text on white background
# ---------------------------------------------------------------------------

def ac4_body_forced_black_on_white(block: str) -> None:
    """body must be forced to black text (#000 / black) and white background
    (#fff / white) in the print stylesheet."""
    # Look for a body rule with background: #fff (or white) and color: #000 (or black)
    body_rules = re.findall(r"body[^{]*\{([^}]+)\}", block, re.S)
    found_bg_white = False
    found_color_black = False
    for rule in body_rules:
        if re.search(r"background\s*:\s*#fff\b|background\s*:\s*white\b", rule, re.I):
            found_bg_white = True
        if re.search(r"color\s*:\s*#000\b|color\s*:\s*black\b", rule, re.I):
            found_color_black = True
    assert found_bg_white, (
        "body background is not forced to #fff / white in @media print."
    )
    assert found_color_black, (
        "body color is not forced to #000 / black in @media print."
    )


def test_ac4_body_forced_black_on_white(print_block: str) -> None:
    ac4_body_forced_black_on_white(print_block)


# ---------------------------------------------------------------------------
# T4-d: link URL-append rule is present
# ---------------------------------------------------------------------------

def ac4_link_url_append_present(block: str) -> None:
    r"""a[href^="http"]::after must append the URL for paper readability."""
    assert re.search(
        r'a\[href\^="http"\]\s*::after\s*\{[^}]*content\s*:',
        block, re.S
    ), (
        r'a[href^="http"]::after { content: ... } rule not found in @media print. '
        "URLs must be appended after links for the printed tenure packet."
    )


def test_ac4_link_url_append_present(print_block: str) -> None:
    ac4_link_url_append_present(print_block)


# ---------------------------------------------------------------------------
# T4-e: page-break-inside: avoid on key elements
# ---------------------------------------------------------------------------

def ac4_page_break_inside_avoid(block: str) -> None:
    """page-break-inside: avoid must appear for .question-row, .pub-arc, .team-card."""
    for selector in PAGE_BREAK_INSIDE_ELEMENTS:
        pattern = re.compile(
            r"(?:[^{]*" + re.escape(selector) + r"[^{]*)\{[^}]*page-break-inside\s*:\s*avoid",
            re.S,
        )
        assert pattern.search(block), (
            f"'{selector}' does not have page-break-inside: avoid in @media print. "
            f"Academic content rows must not split across printed pages."
        )


def test_ac4_page_break_inside_avoid(print_block: str) -> None:
    ac4_page_break_inside_avoid(print_block)


# ---------------------------------------------------------------------------
# T4-f: at least one major section has page-break-before: always
# ---------------------------------------------------------------------------

def ac4_major_section_page_break_before(block: str) -> None:
    """At least one major section must have page-break-before: always so
    the tenure packet's major sections start on fresh pages."""
    found_any = False
    for section in MAJOR_SECTIONS:
        pattern = re.compile(
            re.escape(section) + r"[^{]*\{[^}]*page-break-before\s*:\s*always",
            re.S,
        )
        if pattern.search(block):
            found_any = True
            break
    assert found_any, (
        f"No major section ({MAJOR_SECTIONS}) has page-break-before: always in @media print. "
        "The tenure packet sections should start on a fresh page when printed."
    )


def test_ac4_major_section_page_break_before(print_block: str) -> None:
    ac4_major_section_page_break_before(print_block)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge: confirm the print block is substantial and not a stub."""

    def test_print_block_is_substantial(self, print_block: str):
        """The print block must have at least 8 CSS rules (not a one-liner stub)."""
        rule_count = len(re.findall(r"\{", print_block))
        assert rule_count >= 8, (
            f"@media print block has only {rule_count} rule(s); "
            "expected a substantial print stylesheet with ≥ 8 rules."
        )

    def test_print_block_hides_theme_toggle(self, print_block: str):
        """theme-toggle must be hidden — it's decoration, not tenure content."""
        assert re.search(r"theme-toggle", print_block, re.I), (
            ".theme-toggle is not referenced in @media print. "
            "The theme toggle must be hidden when printing."
        )

    def test_print_block_url_append_is_not_empty_content(self, print_block: str):
        """The URL-append content must use attr(href), not an empty string."""
        m = re.search(
            r'a\[href\^="http"\]\s*::after\s*\{[^}]*content\s*:\s*([^;]+)',
            print_block, re.S
        )
        if m:
            content_val = m.group(1).strip()
            assert "attr(href)" in content_val, (
                f"a[href^=\"http\"]::after content does not use attr(href): '{content_val}'. "
                "The URL must be appended for paper readability."
            )

"""T6 — CO-4 STYLE_BLOCK mirror consistency guard (craft-uplift spec).

Guards:
- The var(--TOKEN) names referenced in the .field-of-interest CSS rules inside
  compare-purple-gold.html EQUAL the var(--TOKEN) names in STYLE_BLOCK in
  scripts/wire_letter_writers.py.
- If the HTML uses a new token (e.g. var(--line-height-snug)) in the
  .field-of-interest block, STYLE_BLOCK must also use it — else the next
  daily cron run silently reverts that token reference (silent-revert guard).
- If the HTML drops a token from .field-of-interest and STYLE_BLOCK still
  uses it, STYLE_BLOCK is now inconsistent with the live HTML styles.
- If the HTML has NO .field-of-interest CSS override, STYLE_BLOCK is the
  sole source, and its tokens must all resolve in design-tokens.css
  (dangling-token guard).

TDD GREEN on the current tree:
  HTML .field-of-interest tokens = {accent-dark, font-size-sm, font-size-xs,
                                      primary, space-1, space-2, text-muted}
  STYLE_BLOCK tokens = same set → no diff → test PASSES.

Run: python3 -m pytest tests/test_style_block_mirror.py -q
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "compare-purple-gold.html"
WIRE_PATH = ROOT / "scripts" / "wire_letter_writers.py"
TOKENS_PATH = ROOT / "design-tokens.css"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_tokens_from_css_block(css_block: str) -> set[str]:
    """Return all --token-name strings referenced via var(--...) in a CSS block."""
    return set(re.findall(r"var\(--([a-z][a-z0-9-]*)\)", css_block))


def _get_style_block(html: str) -> str:
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    return m.group(1) if m else ""


def _extract_foi_css_rules(style: str) -> str:
    """Return the CSS text covering all .field-of-interest rules.

    Captures .field-of-interest { ... }, .field-of-interest.low-conf { ... },
    .field-of-interest .foi-label { ... } — any selector containing
    .field-of-interest and its corresponding { declarations } block.
    """
    pattern = re.compile(
        r"\.field-of-interest[^{]*\{[^}]+\}",
        re.S,
    )
    matches = pattern.findall(style)
    return "\n".join(matches)


def _extract_style_block_css(wire_source: str) -> str:
    """Return the content of the STYLE_BLOCK triple-quoted string."""
    m = re.search(r'STYLE_BLOCK\s*=\s*"""(.*?)"""', wire_source, re.S)
    return m.group(1) if m else ""


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def html_foi_tokens() -> set[str]:
    html = HTML_PATH.read_text(encoding="utf-8")
    style = _get_style_block(html)
    foi_css = _extract_foi_css_rules(style)
    return _extract_tokens_from_css_block(foi_css)


@pytest.fixture(scope="module")
def style_block_tokens() -> set[str]:
    wire = WIRE_PATH.read_text(encoding="utf-8")
    block_css = _extract_style_block_css(wire)
    return _extract_tokens_from_css_block(block_css)


@pytest.fixture(scope="module")
def defined_design_tokens() -> set[str]:
    tokens_css = TOKENS_PATH.read_text(encoding="utf-8")
    return set(re.findall(r"--([a-z][a-z0-9-]+)\s*:", tokens_css))


# ---------------------------------------------------------------------------
# T6-a: HTML .field-of-interest tokens == STYLE_BLOCK tokens
# ---------------------------------------------------------------------------

def ac6_foi_token_sets_match(html_tokens: set[str], sb_tokens: set[str]) -> None:
    """The var(--...) token names in the HTML .field-of-interest CSS rules and
    in STYLE_BLOCK must be identical.

    A discrepancy means the daily cron will silently revert any HTML-side
    change that wasn't mirrored into STYLE_BLOCK (silent-revert guard CO-4).
    """
    html_only = html_tokens - sb_tokens
    sb_only = sb_tokens - html_tokens

    assert not html_only and not sb_only, (
        f"STYLE_BLOCK mirror mismatch!\n"
        f"  Tokens in HTML .field-of-interest but NOT in STYLE_BLOCK: {sorted(html_only)}\n"
        f"  Tokens in STYLE_BLOCK but NOT in HTML .field-of-interest: {sorted(sb_only)}\n"
        f"CO-4: mirror any shared-token change into scripts/wire_letter_writers.py STYLE_BLOCK."
    )


def test_ac6_foi_token_sets_match(
    html_foi_tokens: set[str], style_block_tokens: set[str]
) -> None:
    ac6_foi_token_sets_match(html_foi_tokens, style_block_tokens)


# ---------------------------------------------------------------------------
# T6-b: STYLE_BLOCK tokens all resolve in design-tokens.css
# ---------------------------------------------------------------------------

def ac6_style_block_tokens_resolve(sb_tokens: set[str], defined: set[str]) -> None:
    """All tokens in STYLE_BLOCK must be defined in design-tokens.css.

    If a cron run emits a STYLE_BLOCK that references a non-existent token,
    the .field-of-interest styling will silently fall back to browser defaults.
    """
    # Only check tokens that start with scale prefixes; theme-color tokens
    # (--primary, --accent-dark etc.) live in the [data-theme] blocks, not
    # design-tokens.css, and that's expected.
    SCALE_PREFIXES = ("font-size-", "space-", "radius-", "shadow-",
                      "duration-", "line-height-", "tracking-", "letter-spacing-")
    dangling = {
        t for t in sb_tokens
        if any(t.startswith(p) for p in SCALE_PREFIXES) and t not in defined
    }
    assert not dangling, (
        f"STYLE_BLOCK references scale tokens not defined in design-tokens.css: "
        f"{sorted(dangling)}. Add them to design-tokens.css or update STYLE_BLOCK."
    )


def test_ac6_style_block_tokens_resolve(
    style_block_tokens: set[str], defined_design_tokens: set[str]
) -> None:
    ac6_style_block_tokens_resolve(style_block_tokens, defined_design_tokens)


# ---------------------------------------------------------------------------
# T6-c: HTML .field-of-interest tokens resolve in design-tokens.css (or theme vars)
# ---------------------------------------------------------------------------

def ac6_html_foi_tokens_resolve(html_tokens: set[str], defined: set[str]) -> None:
    """Scale tokens in the HTML .field-of-interest rules must resolve in design-tokens.css."""
    SCALE_PREFIXES = ("font-size-", "space-", "radius-", "shadow-",
                      "duration-", "line-height-", "tracking-", "letter-spacing-")
    dangling = {
        t for t in html_tokens
        if any(t.startswith(p) for p in SCALE_PREFIXES) and t not in defined
    }
    assert not dangling, (
        f"HTML .field-of-interest CSS references undefined design-tokens: "
        f"{sorted(dangling)}"
    )


def test_ac6_html_foi_tokens_resolve(
    html_foi_tokens: set[str], defined_design_tokens: set[str]
) -> None:
    ac6_html_foi_tokens_resolve(html_foi_tokens, defined_design_tokens)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge: validate the STYLE_BLOCK parsing itself."""

    def test_style_block_is_non_empty(self):
        """STYLE_BLOCK must exist and contain CSS rules (not an empty string)."""
        wire = WIRE_PATH.read_text(encoding="utf-8")
        block = _extract_style_block_css(wire)
        assert block.strip(), "STYLE_BLOCK is empty or not found in wire_letter_writers.py"

    def test_html_foi_rules_are_present(self):
        """The HTML must have .field-of-interest CSS rules (the STYLE_BLOCK
        injects them; they should already be wired in the base tree)."""
        html = HTML_PATH.read_text(encoding="utf-8")
        style = _get_style_block(html)
        foi_css = _extract_foi_css_rules(style)
        assert foi_css.strip(), (
            "No .field-of-interest CSS rules found in compare-purple-gold.html. "
            "The STYLE_BLOCK should have been wired in by wire_letter_writers.py."
        )

    def test_token_set_is_not_empty(self, html_foi_tokens: set[str]):
        """Both token sets should be non-empty (guards against a parse failure
        that returns empty sets and trivially passes the equality check)."""
        assert html_foi_tokens, (
            "HTML .field-of-interest token set is empty — possible parse failure."
        )

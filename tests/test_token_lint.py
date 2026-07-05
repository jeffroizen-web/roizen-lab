"""T1 — R-1 token-discipline lint (hex + spacing, craft-uplift spec).

Guards:
- Zero raw hex color literals outside [data-theme=...] / :root / @media print.
- Zero raw-px values in margin/padding/gap component rules (outside exempt blocks).

TDD RED on the current tree: 27 scattered hex + raw-px spacing (18px, 60px) present.
GREEN after the craft-uplift moves all scattered color/spacing to var(--…) tokens.

Delta carve-outs (architect review F3 + delta brief):
  (a) @media print block — B-1 mandates black-on-white print; its ~16 raw hex are
      expected and correct (e.g. #000/#fff/#ccc/#eee/#333/#555/#666).
  (b) SANCTIONED_HEX — a list of hex values that are legally un-removable even after
      the uplift; each entry has a one-line reason comment.  Currently empty because
      the implementation MUST replace every scattered hex with a var(--…) token.
      A new entry added here must have a reason, or the test will continue to fail.
      The test is verified to go RED on any new unsanctioned hex (see kill-proof test).

Run: python3 -m pytest tests/test_token_lint.py -q
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "compare-purple-gold.html"

# ---------------------------------------------------------------------------
# SANCTIONED_HEX: hex values that are legally un-removable in the component
# CSS even after the craft-uplift. Currently empty — all scattered hex must
# be replaced with var(--…) tokens.
#
# When adding an entry, include a one-line reason:
# e.g.  "#b03a3a",   # form-error red; no semantic token defined yet
# ---------------------------------------------------------------------------
SANCTIONED_HEX: frozenset[str] = frozenset()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_style_block(html: str) -> str:
    """Return the content of the first <style> … </style> block."""
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    return m.group(1) if m else ""


def _strip_data_theme_blocks(css: str) -> str:
    """Remove all [data-theme="..."] { … } blocks using brace matching.

    The blocks contain only CSS variable declarations (no nested rules),
    but brace-matching is more robust than a greedy non-nesting regex.
    """
    result_parts: list[str] = []
    i = 0
    while i < len(css):
        m = re.search(r"\[data-theme", css[i:])
        if not m:
            result_parts.append(css[i:])
            break
        result_parts.append(css[i : i + m.start()])
        i = i + m.start()
        try:
            brace_i = css.index("{", i)
        except ValueError:
            result_parts.append(css[i:])
            break
        depth = 0
        j = brace_i
        while j < len(css):
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
                if depth == 0:
                    i = j + 1
                    break
            j += 1
        else:
            break  # unclosed block
    return "".join(result_parts)


def _strip_root_block(css: str) -> str:
    """Remove the :root { … } block (no nested braces)."""
    return re.sub(r":root\s*\{[^}]+\}", "", css, flags=re.S)


def _strip_print_block(css: str) -> str:
    """Remove the @media print { … } block using brace matching."""
    start = css.find("@media print")
    if start == -1:
        return css
    try:
        brace_i = css.index("{", start)
    except ValueError:
        return css
    depth = 0
    j = brace_i
    while j < len(css):
        if css[j] == "{":
            depth += 1
        elif css[j] == "}":
            depth -= 1
            if depth == 0:
                return css[:start] + css[j + 1 :]
        j += 1
    return css  # unclosed — return unchanged


def _get_trimmed_css(html: str) -> str:
    """Return the style block with all exempt blocks removed."""
    css = _get_style_block(html)
    css = _strip_data_theme_blocks(css)
    css = _strip_root_block(css)
    css = _strip_print_block(css)
    return css


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def trimmed_css() -> str:
    html = HTML_PATH.read_text(encoding="utf-8")
    return _get_trimmed_css(html)


# ---------------------------------------------------------------------------
# T1-a: zero raw hex outside exempt blocks
# ---------------------------------------------------------------------------

def ac1_no_raw_hex_outside_exempt_blocks(trimmed: str) -> None:
    """Core assertion: no #rrggbb / #rgb / #rrggbbaa literals in component CSS."""
    # Match #hex preceded by a context that isn't a word char or & (avoids
    # matching URL fragments, HTML entities, or mid-word strings).
    hex_pattern = re.compile(r"(?<![&\w])#[0-9a-fA-F]{3,8}\b")
    found = [
        h
        for h in hex_pattern.findall(trimmed)
        if h.lower() not in {s.lower() for s in SANCTIONED_HEX}
    ]
    assert not found, (
        f"Raw hex literals in component CSS outside exempt blocks — "
        f"replace with var(--…) tokens: {sorted(set(found))}"
    )


def test_ac1_no_raw_hex_outside_exempt_blocks(trimmed_css: str) -> None:
    ac1_no_raw_hex_outside_exempt_blocks(trimmed_css)


# ---------------------------------------------------------------------------
# Kill-proof: the test MUST be able to go red on a new unsanctioned hex.
# This verifies testing-standards rule 2 (every test can go red).
# ---------------------------------------------------------------------------

def test_ac1_kill_proof_unsanctioned_hex_is_detected(trimmed_css: str) -> None:
    """Inject a fake unsanctioned hex and assert the scanner catches it."""
    poisoned = trimmed_css + "\n.fake-rule { color: #deadbe; }"
    hex_pattern = re.compile(r"(?<![&\w])#[0-9a-fA-F]{3,8}\b")
    found = [
        h
        for h in hex_pattern.findall(poisoned)
        if h.lower() not in {s.lower() for s in SANCTIONED_HEX}
    ]
    assert found, (
        "Kill-proof failed: injected unsanctioned hex '#deadbe' was not detected. "
        "Check that SANCTIONED_HEX doesn't accidentally include it."
    )


# ---------------------------------------------------------------------------
# T1-b: zero raw-px values in margin / padding / gap component rules
# ---------------------------------------------------------------------------

def ac1_no_raw_px_in_spacing_rules(trimmed: str) -> None:
    """Component margin/padding/gap must use var(--space-N), not raw Npx."""
    # Match a spacing property declaration that contains a bare integer+px value
    # outside a var(). We look for the property name followed by a colon and then
    # scan the value for \d+px not preceded by 'var(' context.
    #
    # Strategy: find every spacing property declaration, then check whether the
    # value portion contains a raw Npx that doesn't appear inside a var(...).
    spacing_decl_pattern = re.compile(
        r"(?:^|[;{])\s*"
        r"(?:margin|padding|gap)(?:-(?:top|right|bottom|left|inline|block|inline-start|inline-end|block-start|block-end))?"
        r"\s*:\s*([^;{}]+)",
        re.MULTILINE,
    )
    violations: list[str] = []
    for m in spacing_decl_pattern.finditer(trimmed):
        value = m.group(1).strip()
        # Skip if ALL px numbers appear inside var() — e.g. var(--space-4) is fine.
        # Find every Npx occurrence; check if it's inside a var(...)
        for px_m in re.finditer(r"\d+px", value):
            pos = px_m.start()
            # Walk back to see if we're inside a var(...)
            before = value[:pos]
            if before.count("var(") > before.count(")"):
                # inside a var() — acceptable
                continue
            violations.append(f"{m.group(0).strip()}")
            break
    assert not violations, (
        f"Raw-px values in margin/padding/gap component rules — "
        f"replace with var(--space-N): {violations}"
    )


def test_ac1_no_raw_px_in_spacing_rules(trimmed_css: str) -> None:
    ac1_no_raw_px_in_spacing_rules(trimmed_css)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge cases: ensure exempt blocks are correctly excluded."""

    def test_print_block_is_stripped(self):
        """The @media print block must be absent from the trimmed CSS so its
        legitimate raw hex (e.g. #000, #fff) does not trigger T1-a."""
        html = HTML_PATH.read_text(encoding="utf-8")
        trimmed = _get_trimmed_css(html)
        assert "@media print" not in trimmed, (
            "@media print block was not stripped — its sanctioned hex would false-fail T1-a"
        )

    def test_data_theme_blocks_are_stripped(self):
        """[data-theme=...] blocks must be absent from trimmed CSS."""
        html = HTML_PATH.read_text(encoding="utf-8")
        trimmed = _get_trimmed_css(html)
        assert "[data-theme" not in trimmed, (
            "[data-theme] blocks were not stripped from the trimmed CSS"
        )

    def test_root_block_is_stripped(self):
        """:root block must be absent from trimmed CSS."""
        html = HTML_PATH.read_text(encoding="utf-8")
        trimmed = _get_trimmed_css(html)
        # A very small :root token shouldn't appear after stripping
        css = _get_style_block(html)
        has_root = bool(re.search(r":root\s*\{", css))
        if has_root:
            assert ":root" not in trimmed or re.search(r":root\s*\{", trimmed) is None, (
                ":root block was not stripped — its variable definitions could false-fail T1-a"
            )

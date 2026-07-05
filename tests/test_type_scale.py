"""T2 — R-2 type-scale membership + single-h1 guard (craft-uplift spec).

Guards:
- design-tokens.css defines a line-height scale (≥ 1, ≤ 4 tokens named --line-height-*).
- design-tokens.css defines a tracking (letter-spacing) scale (≥ 1, ≤ 3 tokens named
  --tracking-* or --letter-spacing-*).
- Every raw `line-height: <number>` in component CSS uses var(--line-height-*).
- Every raw `letter-spacing: <number>` in component CSS uses var(--tracking-*).
- Exactly one <h1> in the document.
- No referenced --line-height-* / --tracking-* token is undefined (no dangling refs).

TDD RED on the current tree:
  - design-tokens.css has no --line-height-* or --tracking-* tokens → scale tests fail.
  - HTML has raw numbers for line-height (1.2, 1.3, 1.4, 1.5, 1.6, 1.65, 1.7, 1.8)
    and raw px for letter-spacing (0.2px, 0.3px, 0.4px, 0.5px, 1px, 1.2px, 1.5px,
    2px, 3px) → membership tests fail.
  - The single-h1 test is GREEN (1 h1 on the base tree).

Run: python3 -m pytest tests/test_type_scale.py -q
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "compare-purple-gold.html"
TOKENS_PATH = ROOT / "design-tokens.css"

# ---------------------------------------------------------------------------
# Exempt CSS block strips (mirror T1 helpers — inline to avoid shared-module)
# ---------------------------------------------------------------------------

def _get_style_block(html: str) -> str:
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    return m.group(1) if m else ""


def _strip_data_theme_blocks(css: str) -> str:
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
            break
    return "".join(result_parts)


def _strip_root_block(css: str) -> str:
    return re.sub(r":root\s*\{[^}]+\}", "", css, flags=re.S)


def _strip_print_block(css: str) -> str:
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
    return css


def _trimmed_css(html: str) -> str:
    css = _get_style_block(html)
    css = _strip_data_theme_blocks(css)
    css = _strip_root_block(css)
    css = _strip_print_block(css)
    return css


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def tokens_css() -> str:
    return TOKENS_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def html_text() -> str:
    return HTML_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def component_css(html_text: str) -> str:
    return _trimmed_css(html_text)


# ---------------------------------------------------------------------------
# Token-set helpers
# ---------------------------------------------------------------------------

def _line_height_tokens(tokens: str) -> set[str]:
    """Return the set of --line-height-* token names defined in design-tokens.css."""
    return set(re.findall(r"--(line-height-[a-z][a-z0-9-]*)\s*:", tokens))


def _tracking_tokens(tokens: str) -> set[str]:
    """Return the set of --tracking-* or --letter-spacing-* token names."""
    return set(re.findall(r"--((?:tracking|letter-spacing)-[a-z][a-z0-9-]*)\s*:", tokens))


# ---------------------------------------------------------------------------
# T2-a: line-height scale is defined in design-tokens.css
# ---------------------------------------------------------------------------

def ac2_line_height_scale_defined(tokens: str) -> None:
    """design-tokens.css must define 1–4 --line-height-* tokens (the scale)."""
    lh_tokens = _line_height_tokens(tokens)
    assert lh_tokens, (
        "design-tokens.css defines no --line-height-* tokens. "
        "Add a tokenized line-height scale (~4 steps) to satisfy R-2."
    )
    assert len(lh_tokens) <= 4, (
        f"design-tokens.css defines {len(lh_tokens)} --line-height-* tokens "
        f"({sorted(lh_tokens)}); the spec calls for ~4 steps (≤ 4)."
    )


def test_ac2_line_height_scale_defined(tokens_css: str) -> None:
    ac2_line_height_scale_defined(tokens_css)


# ---------------------------------------------------------------------------
# T2-b: tracking scale is defined in design-tokens.css
# ---------------------------------------------------------------------------

def ac2_tracking_scale_defined(tokens: str) -> None:
    """design-tokens.css must define 1–3 --tracking-* tokens (the tracking scale)."""
    tr_tokens = _tracking_tokens(tokens)
    assert tr_tokens, (
        "design-tokens.css defines no --tracking-* / --letter-spacing-* tokens. "
        "Add a tokenized tracking scale (~3 steps) to satisfy R-2."
    )
    assert len(tr_tokens) <= 3, (
        f"design-tokens.css defines {len(tr_tokens)} tracking tokens "
        f"({sorted(tr_tokens)}); the spec calls for ~3 steps (≤ 3)."
    )


def test_ac2_tracking_scale_defined(tokens_css: str) -> None:
    ac2_tracking_scale_defined(tokens_css)


# ---------------------------------------------------------------------------
# T2-c: every raw numeric line-height in component CSS uses a token var()
# ---------------------------------------------------------------------------

def ac2_all_line_heights_tokenized(css: str) -> None:
    """Every line-height: value in component rules must be var(--line-height-*).

    A raw numeric value (e.g. 1.6, 1.2) is a violation; it must be replaced
    with a reference to the new line-height scale token.
    """
    # Match line-height: <numeric> (not a var() reference)
    raw_lh = re.findall(
        r"line-height\s*:\s*(?!var\()[^;{}]+",
        css,
    )
    # Filter to actual numeric values (not 'inherit', 'normal', etc. or already var())
    numeric_raw = [
        v.strip() for v in raw_lh
        if re.search(r"[0-9]", v) and "var(" not in v
    ]
    assert not numeric_raw, (
        f"Raw numeric line-height values in component CSS — replace with var(--line-height-*): "
        f"{sorted(set(numeric_raw))}"
    )


def test_ac2_all_line_heights_tokenized(component_css: str) -> None:
    ac2_all_line_heights_tokenized(component_css)


# ---------------------------------------------------------------------------
# T2-d: every raw letter-spacing in component CSS uses a token var()
# ---------------------------------------------------------------------------

def ac2_all_letter_spacings_tokenized(css: str) -> None:
    """Every letter-spacing: value in component rules must be var(--tracking-*).

    Raw px/em/rem values must be replaced with tracking scale token references.
    """
    raw_ls = re.findall(
        r"letter-spacing\s*:\s*(?!var\()[^;{}]+",
        css,
    )
    # Filter out 'normal', 'inherit', 'initial' (non-numeric keywords)
    numeric_raw = [
        v.strip() for v in raw_ls
        if re.search(r"[0-9]", v) and "var(" not in v
    ]
    assert not numeric_raw, (
        f"Raw numeric letter-spacing values in component CSS — replace with var(--tracking-*): "
        f"{sorted(set(numeric_raw))}"
    )


def test_ac2_all_letter_spacings_tokenized(component_css: str) -> None:
    ac2_all_letter_spacings_tokenized(component_css)


# ---------------------------------------------------------------------------
# T2-e: referenced --line-height-* tokens resolve in design-tokens.css
# ---------------------------------------------------------------------------

def ac2_line_height_token_refs_resolve(css: str, tokens: str) -> None:
    """Every var(--line-height-*) used in HTML CSS must be defined in tokens."""
    defined = _line_height_tokens(tokens)
    referenced = set(re.findall(r"var\(--(line-height-[a-z][a-z0-9-]*)\)", css))
    dangling = referenced - defined
    assert not dangling, (
        f"HTML references undefined --line-height-* tokens: {sorted(dangling)}"
    )


def test_ac2_line_height_token_refs_resolve(component_css: str, tokens_css: str) -> None:
    ac2_line_height_token_refs_resolve(component_css, tokens_css)


# ---------------------------------------------------------------------------
# T2-f: referenced --tracking-* tokens resolve in design-tokens.css
# ---------------------------------------------------------------------------

def ac2_tracking_token_refs_resolve(css: str, tokens: str) -> None:
    """Every var(--tracking-*) used in HTML CSS must be defined in tokens."""
    defined = _tracking_tokens(tokens)
    referenced = set(re.findall(
        r"var\(--((?:tracking|letter-spacing)-[a-z][a-z0-9-]*)\)", css
    ))
    dangling = referenced - defined
    assert not dangling, (
        f"HTML references undefined --tracking-* tokens: {sorted(dangling)}"
    )


def test_ac2_tracking_token_refs_resolve(component_css: str, tokens_css: str) -> None:
    ac2_tracking_token_refs_resolve(component_css, tokens_css)


# ---------------------------------------------------------------------------
# T2-g: exactly one <h1> in the document (GREEN on base tree)
# ---------------------------------------------------------------------------

def ac2_single_h1(html: str) -> None:
    """The document must have exactly one <h1> element (WCAG + SEO requirement)."""
    h1_count = len(re.findall(r"<h1[\s>]", html, re.I))
    assert h1_count == 1, (
        f"Expected exactly 1 <h1> in compare-purple-gold.html, found {h1_count}."
    )


def test_ac2_single_h1(html_text: str) -> None:
    ac2_single_h1(html_text)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge: validate the scale constraints and token references."""

    def test_scale_token_count_max_4_line_height(self, tokens_css: str):
        """Regression: adding a 5th line-height token breaks the ~4-step scale constraint."""
        lh_tokens = _line_height_tokens(tokens_css)
        # Only fires RED if more than 4 tokens exist after implementation
        if lh_tokens:
            assert len(lh_tokens) <= 4, (
                f"Too many --line-height-* tokens ({len(lh_tokens)}); "
                f"collapse near-dupes to the 4-step scale"
            )

    def test_scale_token_count_max_3_tracking(self, tokens_css: str):
        """Regression: adding a 4th tracking token breaks the ~3-step scale constraint."""
        tr_tokens = _tracking_tokens(tokens_css)
        if tr_tokens:
            assert len(tr_tokens) <= 3, (
                f"Too many tracking tokens ({len(tr_tokens)}); "
                f"collapse to the 3-step scale"
            )

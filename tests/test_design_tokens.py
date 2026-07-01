"""Design-token discipline guard (web-quality PR-1, gap #1, 2026-07-01).

design-tokens.css is the single source of truth for the theme-independent
scales (type/spacing/radius/shadow/motion) — the seed of the canonical
claude-design-tokens. The site's 24 ad-hoc font sizes + hardcoded inline
px/rem were replaced with references to these tokens.

These guards lock that in:
- the token file exists and is linked from the page,
- NO ad-hoc font-size magic number survives in the HTML (the gap-fix lock),
- every design-token referenced in the HTML resolves to a definition in the
  token file (no dangling/typo'd token),
- the cron-generated .field-of-interest block (wire_letter_writers.py) also
  emits tokens, so a daily cron run can't revert the site to magic numbers.

Run: python3 -m pytest tests/test_design_tokens.py -q
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = (ROOT / "compare-purple-gold.html").read_text()
TOKENS = (ROOT / "design-tokens.css").read_text()
WIRE = (ROOT / "scripts" / "wire_letter_writers.py").read_text()

TOKEN_PREFIXES = ("font-size-", "space-", "radius-", "shadow-", "duration-")


def _defined_tokens():
    return set(re.findall(r"--([a-z0-9-]+)\s*:", TOKENS))


def test_token_file_exists_and_is_linked():
    assert (ROOT / "design-tokens.css").exists()
    assert 'href="design-tokens.css"' in HTML, "page does not link design-tokens.css"


def test_scales_are_defined():
    defined = _defined_tokens()
    # spot-check each scale has its endpoints (a real scale, not a stub)
    for name in ("font-size-xs", "font-size-5xl", "space-1", "space-16",
                 "radius-sm", "radius-pill", "shadow-sm", "shadow-xl",
                 "duration-fast", "duration-slow"):
        assert name in defined, f"design token --{name} missing from design-tokens.css"


def test_no_adhoc_font_size_in_html():
    """Every font-size must come from a token (the gap-#1 lock)."""
    adhoc = re.findall(r"font-size:\s*([0-9.]+(?:rem|px))", HTML)
    assert not adhoc, f"ad-hoc font-size magic numbers still in HTML: {sorted(set(adhoc))}"


def test_referenced_tokens_all_resolve():
    """Every var(--<scale>-*) used in the HTML is defined in the token file."""
    defined = _defined_tokens()
    referenced = re.findall(r"var\(--([a-z0-9-]+)\)", HTML)
    dangling = sorted({
        t for t in referenced
        if t.startswith(TOKEN_PREFIXES) and t not in defined
    })
    assert not dangling, f"HTML references undefined design tokens: {dangling}"


def test_cron_generator_emits_tokens_not_magic_numbers():
    """wire_letter_writers.py STYLE_BLOCK must use tokens, else a daily cron run
    reverts the .field-of-interest block to magic numbers and breaks the lock."""
    block = re.search(r'STYLE_BLOCK\s*=\s*"""(.*?)"""', WIRE, re.S)
    assert block, "STYLE_BLOCK not found in wire_letter_writers.py"
    adhoc = re.findall(r"font-size:\s*([0-9.]+(?:rem|px))", block.group(1))
    assert not adhoc, f"cron STYLE_BLOCK still has ad-hoc font-size: {adhoc}"

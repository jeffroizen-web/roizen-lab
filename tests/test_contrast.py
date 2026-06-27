"""WCAG AA contrast regression guard for the Roizen Lab theme palettes.

Parses the two theme blocks ([data-theme="purple-gold"] = active/light,
[data-theme="warm-slate"] = dark) out of compare-purple-gold.html, resolves
each var to a hex value, and asserts every text/background pair a visitor
actually sees clears WCAG AA (4.5:1 for normal text).

This locks in the 2026-06-27 a11y fix: the CTA buttons used white text on
gold (#C5A336) = 2.42:1 FAIL; they now use the theme-dark color on gold
(--btn-text / .btn-donate color:var(--primary)) = 5.39:1. If anyone reverts
the button text to white or lightens the gold, test_button_contrast catches it.

Computation is the WCAG 2.x relative-luminance formula (deterministic, no deps).

Run: python3 -m pytest tests/test_contrast.py -q
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HTML = (ROOT / "compare-purple-gold.html").read_text()

AA_NORMAL = 4.5


def _luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    R, G, B = lin(r), lin(g), lin(b)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def contrast(a: str, b: str) -> float:
    la, lb = _luminance(a), _luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _theme_vars(selector: str) -> dict:
    """Extract the --name: #hex; declarations inside one theme block."""
    m = re.search(re.escape(selector) + r"\s*\{(.*?)\}", HTML, re.S)
    assert m, f"theme block {selector!r} not found"
    body = m.group(1)
    return {name: val for name, val in re.findall(r"--([a-z0-9-]+):\s*(#[0-9A-Fa-f]{3,6})\s*;", body)}


LIGHT = _theme_vars('[data-theme="purple-gold"]')
DARK = _theme_vars('[data-theme="warm-slate"]')


@pytest.mark.parametrize("theme,name", [(LIGHT, "purple-gold"), (DARK, "warm-slate")])
def test_button_contrast(theme, name):
    """Both CTA buttons: .btn (text=--btn-text on bg=--btn-bg) and
    .btn-donate (text=--primary on bg=--accent) must clear AA."""
    btn = contrast(theme["btn-text"], theme["btn-bg"])
    donate = contrast(theme["primary"], theme["accent"])
    assert btn >= AA_NORMAL, f"[{name}] .btn {theme['btn-text']} on {theme['btn-bg']} = {btn:.2f}:1"
    assert donate >= AA_NORMAL, f"[{name}] .btn-donate {theme['primary']} on {theme['accent']} = {donate:.2f}:1"


@pytest.mark.parametrize("theme,name", [(LIGHT, "purple-gold"), (DARK, "warm-slate")])
def test_body_text_contrast(theme, name):
    """Body/heading/muted text on the white and off-white surfaces must clear AA."""
    checks = {
        "primary heading on white": ("primary", "white"),
        "body text on white": ("text", "white"),
        "muted text on white": ("text-muted", "white"),
        "muted text on off-white": ("text-muted", "off-white"),
        "gold body-text (accent-dark) on white": ("accent-dark", "white"),
        "gold body-text (accent-dark) on off-white": ("accent-dark", "off-white"),
    }
    failures = []
    for label, (fg, bg) in checks.items():
        ratio = contrast(theme[fg], theme[bg])
        if ratio < AA_NORMAL:
            failures.append(f"[{name}] {label}: {theme[fg]} on {theme[bg]} = {ratio:.2f}:1")
    assert not failures, "WCAG AA contrast failures:\n" + "\n".join(failures)


def test_no_white_on_gold_buttons():
    """Direct guard against the specific regression that was fixed: a button
    rule must not pair white text with a gold (accent/btn) background."""
    btn_donate = re.search(r"\.btn-donate\s*\{([^}]*)\}", HTML).group(1)
    assert "var(--primary)" in btn_donate and "#FFFFFF" not in btn_donate.upper().replace("#FFF;", "#FFFFFF;"), \
        f".btn-donate regressed to white-on-gold: {btn_donate.strip()}"
    assert LIGHT["btn-text"].upper() != "#FFFFFF", "light --btn-text regressed to white (white-on-gold = 2.42:1)"

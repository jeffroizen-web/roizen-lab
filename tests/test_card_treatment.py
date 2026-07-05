"""F2 design-decision guard (Rams MSG-903949, 2026-07-05).

The person / team sections are a DELIBERATE plain centered roster — faces + names
are the content; box chrome would read corporate on a front-door people list.
They are intentionally NOT the boxed `.card` base (which news / alumni / gear use).
This guard fails if a future edit folds them into `.card` (a front-door visual
regression). Zero-visual intent; see the `.card` base comment in
compare-purple-gold.html. Update this guard only with a design sign-off.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = (ROOT / "compare-purple-gold.html").read_text(encoding="utf-8")

PLAIN_ROSTER_CLASSES = {"person-card", "team-card"}


def test_plain_roster_cards_not_folded_into_card_base() -> None:
    """No element may carry BOTH a plain-roster class and the boxed `.card` base."""
    for m in re.finditer(r'class="([^"]*)"', HTML):
        classes = set(m.group(1).split())
        folded = classes & PLAIN_ROSTER_CLASSES
        if folded and "card" in classes:
            raise AssertionError(
                f'F2 guard: a plain-roster card was folded into .card: class="{m.group(1)}". '
                "Person/team sections are an intentional plain roster (Rams F2, MSG-903949); "
                "do not add the boxed .card base without a design sign-off."
            )


def test_plain_roster_classes_still_present() -> None:
    """Meta-guard: the classes this test protects must still exist in the markup."""
    assert 'class="person-card"' in HTML or 'class="team-card"' in HTML, (
        "Neither person-card nor team-card found — the F2 guard has nothing to "
        "protect; verify the markup."
    )

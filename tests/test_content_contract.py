"""Content-contract drift guard for the Roizen Lab site.

content/site-content.json is a config-for-one data contract: the stable,
Jeff-specific rendered-site content extracted from compare-purple-gold.html.
The canonical HTML is still authoritative for RENDER (no build step yet), so
this test guards the contract against silent drift from the HTML — every
content value in the contract must still appear in the live page.

Normalization makes the check robust to inline markup and HTML entities:
each value is searched against BOTH (a) the tag-stripped page text (for body
copy that contains <br>/<span>/<em>) and (b) the entity-unescaped raw HTML
(for attribute values, hrefs, and img src). A match in either passes.

Deliberately EXCLUDED from the contract (and therefore from this guard):
the cron-managed .field-of-interest spans (wire_letter_writers.py owns
docs/letter_writers.json) and per-person shared-publication lists. Those are
volatile and Producer-Owned; tracking them here would make this guard flap on
every cron run. test_no_cron_owned_fields keeps that boundary explicit.

Run: python3 -m pytest tests/test_content_contract.py -q
"""
import html
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "compare-purple-gold.html"
CONTRACT_PATH = ROOT / "content" / "site-content.json"

# Contract-internal keys whose values are NOT expected to appear in the HTML
# verbatim (file paths, booleans-as-config, documentation).
NON_RENDERED_KEYS = {"data_source"}
# Keys that would mean we'd started tracking cron-owned content — must stay absent.
FORBIDDEN_PERSON_KEYS = {"recent_focus", "field_of_interest", "foi", "shared_publications"}


def _collapse(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


@pytest.fixture(scope="module")
def contract():
    return json.loads(CONTRACT_PATH.read_text())


@pytest.fixture(scope="module")
def page_forms():
    raw = HTML_PATH.read_text()
    raw_norm = _collapse(html.unescape(raw))
    text_norm = _collapse(html.unescape(re.sub(r"<[^>]+>", " ", raw)))
    return raw_norm, text_norm


def _iter_values(node, key=None):
    """Yield every leaf string value worth guarding, skipping _meta + non-rendered keys."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "_meta" or k in NON_RENDERED_KEYS:
                continue
            yield from _iter_values(v, k)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_values(item, key)
    elif isinstance(node, str):
        v = node.strip()
        if v:
            yield key, v


def test_contract_parses_and_has_all_sections(contract):
    expected = {
        "meta", "hero", "big_questions", "team", "collaborators", "peers",
        "mentors", "publications", "news", "alumni", "donate", "contact", "links",
    }
    assert expected <= set(contract), f"missing sections: {expected - set(contract)}"


def test_structural_counts(contract):
    qs = contract["big_questions"]["questions"]
    assert [q["id"] for q in qs] == ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]
    assert len(contract["team"]["members"]) == 2
    assert len(contract["collaborators"]["people"]) == 2
    assert len(contract["peers"]["people"]) == 5
    assert len(contract["mentors"]["people"]) == 3
    assert len(contract["news"]["items"]) == 4
    assert len(contract["alumni"]["people"]) == 9


def test_every_contract_value_present_in_html(contract, page_forms):
    raw_norm, text_norm = page_forms
    missing = []
    for key, value in _iter_values(contract):
        v = _collapse(html.unescape(value))
        if v not in raw_norm and v not in text_norm:
            missing.append(f"[{key}] {value!r}")
    assert not missing, "contract values not found in compare-purple-gold.html (drift):\n" + "\n".join(missing)


def test_figure_srcs_resolve_to_files(contract):
    """Non-placeholder question figures must point at files that exist on disk."""
    broken = []
    for q in contract["big_questions"]["questions"]:
        fig = q["figure"]
        if not fig.get("placeholder") and fig.get("src"):
            if not (ROOT / fig["src"]).exists():
                broken.append(f'{q["id"]}: {fig["src"]}')
    assert not broken, "figure src(s) with no file on disk: " + ", ".join(broken)


def test_no_cron_owned_fields(contract):
    """Boundary guard: the contract must never start tracking cron-managed
    field-of-interest / shared-pub content (Producer-Owned by wire_letter_writers.py)."""
    offenders = []
    for section in ("collaborators", "peers", "mentors"):
        for person in contract[section]["people"]:
            bad = FORBIDDEN_PERSON_KEYS & set(person)
            if bad:
                offenders.append(f"{section}/{person.get('name')}: {bad}")
    assert not offenders, "contract leaked cron-owned fields: " + "; ".join(offenders)

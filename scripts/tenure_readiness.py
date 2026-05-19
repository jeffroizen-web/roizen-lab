#!/usr/bin/env python3
"""
Tenure-readiness watcher for the Roizen Lab site.

Scores the working HTML against the four audience rubrics defined in
docs/jeff-review-2026-04-15.md (committee, collaborator, journalist, reviewer).
Reports drift since the last run.

Run:
    python3 scripts/tenure_readiness.py            # human report
    python3 scripts/tenure_readiness.py --json     # machine-readable
    python3 scripts/tenure_readiness.py --baseline # write current state as new baseline

Exit codes:
    0 = pass (no NEW issues since baseline)
    1 = regression (new issues introduced)
    2 = no baseline yet (first run)
"""
import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "compare-purple-gold.html"
BASELINE = ROOT / "docs" / "tenure_readiness_baseline.json"

# Phrases the lab-website voice rule explicitly flags as Claude-rewrites.
# Each represents a one-line edit Jeff has already considered (jeff-review-2026-04-15 prose section).
BANNED_PHRASES = [
    "fortunate to work with",
    "stand on the shoulders",
    "leverage",
    "synergy",
    "ideate",
    "advances our understanding",
]

# href="#" is a dead-link smell. The donate button is the one accepted placeholder
# (waiting on CHOP Foundation URL — flagged in CLAUDE.md deferred decisions).
ACCEPTED_HASH_HREFS = {"donate"}


@dataclass
class Findings:
    dead_hash_hrefs: list = field(default_factory=list)
    figure_pending_count: int = 0
    figure_pending_ids: list = field(default_factory=list)
    img_missing_alt: list = field(default_factory=list)
    has_skip_link: bool = False
    has_main_landmark: bool = False
    has_pi_funding_signal: bool = False
    banned_phrases_found: list = field(default_factory=list)
    total_imgs: int = 0
    imgs_missing_dimensions: list = field(default_factory=list)

    def grade(self) -> str:
        critical = (
            len(self.dead_hash_hrefs)
            + len(self.img_missing_alt)
            + len(self.banned_phrases_found)
            + (0 if self.has_skip_link else 1)
            + (0 if self.has_main_landmark else 1)
            + (0 if self.has_pi_funding_signal else 1)
        )
        if critical == 0 and self.figure_pending_count == 0:
            return "A"
        if critical == 0 and self.figure_pending_count <= 2:
            return "A-"
        if critical <= 2:
            return "B"
        return "C"


def scan(html: str) -> Findings:
    f = Findings()

    # Dead links (href="#" excluding known placeholders)
    for match in re.finditer(r'<a\s+[^>]*href="#"[^>]*>(.*?)</a>', html, re.DOTALL):
        label = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", match.group(1))).strip()
        if not any(k in label.lower() for k in ACCEPTED_HASH_HREFS):
            f.dead_hash_hrefs.append(label[:60])

    # Figure-pending placeholders
    for match in re.finditer(
        r'<div\s+class="question-row"[^>]*\sid="(q\d+)"[^>]*>(.*?)</div>\s*</div>',
        html,
        re.DOTALL,
    ):
        qid, body = match.group(1), match.group(2)
        if "question-figure-placeholder" in body:
            f.figure_pending_count += 1
            f.figure_pending_ids.append(qid)

    # Imgs and alt/dimension audit
    for img_match in re.finditer(r"<img\b([^>]*)>", html):
        attrs = img_match.group(1)
        f.total_imgs += 1
        src_match = re.search(r'src="([^"]+)"', attrs)
        src = src_match.group(1)[:60] if src_match else "?"
        alt_match = re.search(r'alt="([^"]*)"', attrs)
        if alt_match is None or alt_match.group(1).strip() == "":
            # data:image inline SVG with explicit alt is OK; only flag if no alt attr at all
            if alt_match is None:
                f.img_missing_alt.append(src)
        is_svg = ".svg" in (src_match.group(1) if src_match else "") or "image/svg" in attrs
        if not is_svg and ("width=" not in attrs or "height=" not in attrs):
            f.imgs_missing_dimensions.append(src)

    # WCAG scaffolding
    f.has_skip_link = "skip-link" in html and 'href="#main-content"' in html
    f.has_main_landmark = '<main id="main-content"' in html

    # PI funding signal
    f.has_pi_funding_signal = "NIH-funded" in html and "publications" in html.lower()

    # Banned phrases (case-insensitive)
    low = html.lower()
    for phrase in BANNED_PHRASES:
        if phrase in low:
            f.banned_phrases_found.append(phrase)

    return f


def diff(old: dict, new: dict) -> list:
    """Return list of new-since-baseline issues. List/set fields only."""
    regressions = []
    for key, new_val in new.items():
        if not isinstance(new_val, list):
            continue
        old_val = set(old.get(key, []) or [])
        added = [v for v in new_val if v not in old_val]
        if added:
            regressions.append({"field": key, "new_issues": added})
    return regressions


def human_report(f: Findings, regressions: list) -> str:
    lines = []
    grade = f.grade()
    lines.append(f"Roizen Lab — Tenure Readiness Report ({datetime.now():%Y-%m-%d %H:%M})")
    lines.append("=" * 64)
    lines.append(f"Overall grade: {grade}")
    lines.append("")
    lines.append("Audience rubric:")
    lines.append(f"  [{'PASS' if not f.dead_hash_hrefs else 'FAIL'}] No dead links visible to a grant reviewer")
    lines.append(f"  [{'PASS' if f.has_pi_funding_signal else 'FAIL'}] PI funding/productivity signal present (committee)")
    lines.append(f"  [{'PASS' if not f.banned_phrases_found else 'FAIL'}] No Claude-voice prose drift (journalist/Jeff voice)")
    lines.append(f"  [{'PASS' if f.figure_pending_count <= 2 else 'WARN'}] Figure pending count: {f.figure_pending_count} ({', '.join(f.figure_pending_ids) or 'none'})")
    lines.append(f"  [{'PASS' if not f.img_missing_alt else 'FAIL'}] All imgs have alt (collaborator/a11y)")
    lines.append(f"  [{'PASS' if f.has_skip_link and f.has_main_landmark else 'FAIL'}] Skip-link + main landmark present (WCAG)")
    lines.append(f"  [{'PASS' if not f.imgs_missing_dimensions else 'WARN'}] All imgs have explicit width/height (CLS)")
    lines.append("")
    if f.dead_hash_hrefs:
        lines.append("Dead hash hrefs:")
        for d in f.dead_hash_hrefs:
            lines.append(f"  - {d}")
    if f.banned_phrases_found:
        lines.append("Banned phrases:")
        for p in f.banned_phrases_found:
            lines.append(f"  - {p}")
    if f.img_missing_alt:
        lines.append("Imgs missing alt:")
        for src in f.img_missing_alt:
            lines.append(f"  - {src}")
    if f.imgs_missing_dimensions:
        lines.append(f"Imgs missing width/height ({len(f.imgs_missing_dimensions)}):")
        for src in f.imgs_missing_dimensions[:5]:
            lines.append(f"  - {src}")
        if len(f.imgs_missing_dimensions) > 5:
            lines.append(f"  ... +{len(f.imgs_missing_dimensions) - 5} more")
    if regressions:
        lines.append("")
        lines.append("** REGRESSIONS SINCE BASELINE **")
        for r in regressions:
            lines.append(f"  {r['field']}: {r['new_issues']}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="machine-readable JSON output")
    ap.add_argument("--baseline", action="store_true", help="write current state as new baseline")
    ap.add_argument("--file", default=str(SITE), help="HTML file to scan")
    args = ap.parse_args()

    html = Path(args.file).read_text(encoding="utf-8")
    findings = scan(html)
    findings_dict = asdict(findings)
    findings_dict["grade"] = findings.grade()

    if args.baseline:
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps(findings_dict, indent=2, sort_keys=True))
        print(f"Baseline written: {BASELINE}")
        return 0

    regressions = []
    if BASELINE.exists():
        old = json.loads(BASELINE.read_text())
        regressions = diff(old, findings_dict)
    else:
        if args.json:
            print(json.dumps({"warning": "no baseline yet", "findings": findings_dict}, indent=2))
        else:
            print(human_report(findings, []))
            print("\n(no baseline — run with --baseline to set current state)")
        return 2

    if args.json:
        print(json.dumps({"findings": findings_dict, "regressions": regressions}, indent=2))
    else:
        print(human_report(findings, regressions))

    return 1 if regressions else 0


if __name__ == "__main__":
    sys.exit(main())

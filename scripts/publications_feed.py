#!/usr/bin/env python3
"""
Consumer-side parser for the Archivist → Ace Scout publications feed.

Contract: docs/contracts/archivist-publications.md

Run:
    python3 scripts/publications_feed.py [--feed PATH]
        renders an HTML <ul> string for the Publications section

    python3 scripts/publications_feed.py --validate
        validates feed envelope; exit 0 = OK, 1 = invalid

The parser is forgiving: missing required fields drop the publication
(logged), unknown research_arc falls back to "other", missing feed file
returns None so the site can fall back to docs/publications_data.md.
"""
import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DEFAULT_FEED_PATH = Path.home() / "orchestra-data" / "archivist" / "publications.json"
ALLOWED_ARCS = {"phenotype", "mechanism", "translation", "other"}
REQUIRED_FIELDS = {"pmid", "title", "authors", "venue", "year", "pubmed_url", "research_arc"}
STALENESS_BANNER_DAYS = 14


@dataclass
class Publication:
    pmid: str
    title: str
    authors: list
    venue: str
    year: int
    pubmed_url: str
    research_arc: str
    publication_date: Optional[str] = None
    doi: Optional[str] = None
    first_author: bool = False
    senior_author: bool = False
    open_access: bool = False


@dataclass
class FeedResult:
    publications: list = field(default_factory=list)
    data_as_of: Optional[datetime] = None
    fetched_at: Optional[datetime] = None
    fetched_from: Optional[str] = None
    dropped_count: int = 0
    dropped_reasons: list = field(default_factory=list)
    is_stale: bool = False
    error: Optional[str] = None


def parse_feed(payload: dict) -> FeedResult:
    result = FeedResult(fetched_at=datetime.now(timezone.utc))

    if not isinstance(payload, dict):
        result.error = "feed envelope is not a JSON object"
        return result

    data_as_of_raw = payload.get("data_as_of")
    if data_as_of_raw:
        try:
            result.data_as_of = datetime.fromisoformat(data_as_of_raw.replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - result.data_as_of).days
            result.is_stale = age_days > STALENESS_BANNER_DAYS
        except ValueError:
            result.dropped_reasons.append(f"invalid data_as_of: {data_as_of_raw!r}")

    result.fetched_from = payload.get("fetched_from")

    pubs = payload.get("publications")
    if not isinstance(pubs, list):
        result.error = "publications field missing or not a list"
        return result

    for i, raw in enumerate(pubs):
        if not isinstance(raw, dict):
            result.dropped_count += 1
            result.dropped_reasons.append(f"index {i}: not an object")
            continue
        missing = REQUIRED_FIELDS - set(raw.keys())
        if missing:
            result.dropped_count += 1
            result.dropped_reasons.append(f"pmid={raw.get('pmid', '?')}: missing {sorted(missing)}")
            continue
        arc = raw.get("research_arc")
        if arc not in ALLOWED_ARCS:
            result.dropped_reasons.append(f"pmid={raw['pmid']}: arc {arc!r} -> other")
            arc = "other"
        try:
            pub = Publication(
                pmid=str(raw["pmid"]),
                title=raw["title"],
                authors=list(raw["authors"]),
                venue=raw["venue"],
                year=int(raw["year"]),
                pubmed_url=raw["pubmed_url"],
                research_arc=arc,
                publication_date=raw.get("publication_date"),
                doi=raw.get("doi"),
                first_author=bool(raw.get("first_author", False)),
                senior_author=bool(raw.get("senior_author", False)),
                open_access=bool(raw.get("open_access", False)),
            )
        except (KeyError, TypeError, ValueError) as e:
            result.dropped_count += 1
            result.dropped_reasons.append(f"pmid={raw.get('pmid', '?')}: parse error {e}")
            continue
        result.publications.append(pub)

    return result


def load_feed(path: Path) -> Optional[FeedResult]:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        result = FeedResult(error=f"invalid JSON: {e}")
        return result
    return parse_feed(payload)


def render_html(result: FeedResult) -> str:
    """Render the Publications section <ul>. Includes a staleness banner if needed."""
    out = []
    if result.is_stale and result.data_as_of:
        out.append(
            f'<p class="freshness-banner">Publications list verified through '
            f'{result.data_as_of:%Y-%m-%d}.</p>'
        )
    pubs_by_arc = {"phenotype": [], "mechanism": [], "translation": [], "other": []}
    for pub in result.publications:
        pubs_by_arc[pub.research_arc].append(pub)
    for arc in ("phenotype", "mechanism", "translation", "other"):
        if not pubs_by_arc[arc]:
            continue
        out.append(f'<h3 class="arc-heading">{arc.title()}</h3>')
        out.append('<ul class="publication-list">')
        for pub in sorted(pubs_by_arc[arc], key=lambda p: p.year, reverse=True):
            authors = ", ".join(pub.authors[:3])
            if len(pub.authors) > 3:
                authors += " et al."
            badge = ""
            if pub.first_author:
                badge = ' <span class="pub-badge">first author</span>'
            elif pub.senior_author:
                badge = ' <span class="pub-badge">senior author</span>'
            out.append(
                f'<li><a href="{pub.pubmed_url}">{pub.title}</a>'
                f'{badge} &mdash; {authors}, <em>{pub.venue}</em> ({pub.year}).</li>'
            )
        out.append("</ul>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--feed", default=str(DEFAULT_FEED_PATH), help="path to publications.json")
    ap.add_argument("--validate", action="store_true", help="exit 0 if feed OK, 1 if invalid")
    args = ap.parse_args()

    result = load_feed(Path(args.feed))
    if result is None:
        print(f"FEED MISSING at {args.feed} — site should fall back to docs/publications_data.md")
        return 2
    if result.error:
        print(f"FEED INVALID: {result.error}")
        return 1
    if args.validate:
        print(f"OK — {len(result.publications)} publications, {result.dropped_count} dropped")
        if result.dropped_reasons:
            for r in result.dropped_reasons:
                print(f"  warn: {r}")
        return 0
    print(render_html(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Letter-writer field-of-interest scrape.

For each mentor / collaborator / peer named on the Roizen Lab site,
fetch their recent publication activity from PubMed e-utils (Layer 1),
extract their current field-of-interest, and emit a confidence-scored
JSON record per person.

The Roizen Lab "credibility engine" needs this for two reasons:
1. Tenure letter solicitation Sep 2026 — knowing each writer's current
   research focus shapes the ask language.
2. Site content tuning — collaborator/peer cards can surface "they
   currently work on X" instead of a static affiliation line.

Layers (per Redundant Solutions rule, orchestra.md):
- L1: PubMed e-utils esearch + esummary (auth-free, working)
- L2: ORCID public API (auth-free, stubbed — use when PubMed name
      disambiguation has >1 strong match)
- L3: WebFetch institutional bio page (brittle, often 403 from CLI;
      stubbed — Jeff can run in a real browser if L1+L2 fail)

Run:
    python3 scripts/letter_writer_scrape.py --probe "Muglia LJ"
        single-person probe, prints JSON record

    python3 scripts/letter_writer_scrape.py --from-site
        scrape every person extracted from compare-purple-gold.html,
        write docs/letter_writers.json
"""
import argparse
import json
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import quote
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "compare-purple-gold.html"
OUT = ROOT / "docs" / "letter_writers.json"

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
ORCID_SEARCH = "https://pub.orcid.org/v3.0/expanded-search/"
ORCID_WORKS = "https://pub.orcid.org/v3.0/{iid}/works"

# Affiliation hints used by ORCID disambiguation (institution-name match → trust the iD).
# Drawn from the site's people cards.
KNOWN_AFFILIATIONS = (
    "Children's Hospital of Philadelphia",
    "University of Pennsylvania",
    "Burroughs Wellcome",
    "Cincinnati Children's",
    "Washington University",
    "Dallas",
    "Texas",
)

L2_TRIGGER_CONFIDENCE = 0.6
L2_TRIGGER_PMID_COUNT = 5

# Common English/PubMed words to strip from title-word frequency.
# These are too generic to count as "field of interest" signal.
STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "for", "with", "and", "or", "but", "is",
    "are", "was", "were", "be", "been", "to", "from", "by", "as", "at", "this",
    "that", "these", "those", "study", "studies", "analysis", "based", "using",
    "via", "case", "report", "review", "trial", "results", "effect", "effects",
    "role", "novel", "between", "during", "after", "before", "among", "human",
    "humans", "patients", "patient", "clinical", "research", "data", "association",
    "associated", "evidence", "model", "models", "approach", "comparison", "system",
    "systems", "method", "methods", "new", "high", "low", "type", "use", "us",
}


@dataclass
class PersonProbe:
    name: str
    pubmed_query: str
    recent_pmids: list = field(default_factory=list)
    total_pubmed_count: int = 0
    recent_titles: list = field(default_factory=list)
    recent_venues: list = field(default_factory=list)
    recent_years: list = field(default_factory=list)
    field_terms: list = field(default_factory=list)
    confidence: float = 0.0
    confidence_notes: list = field(default_factory=list)
    layer_used: str = "L1_pubmed"
    fetched_at: str = ""
    error: Optional[str] = None


def _http_get(url: str, timeout: int = 10) -> Optional[bytes]:
    # Accept: application/json matters for ORCID (defaults to XML otherwise).
    # PubMed e-utils ignores it when retmode=json is in the query string.
    req = Request(url, headers={
        "User-Agent": "Roizen-Lab-Scrape/1.0 (ace-scout)",
        "Accept": "application/json",
    })
    try:
        with urlopen(req, timeout=timeout) as r:
            return r.read()
    except (URLError, HTTPError, TimeoutError):
        return None


def normalize_name_for_pubmed(name: str) -> str:
    """
    'Louis J. Muglia, MD, PhD' -> 'Muglia LJ'
    'Hakon Hakonarson, MD, PhD' -> 'Hakonarson H'
    """
    clean = re.sub(r",.*$", "", name).strip()
    parts = clean.replace(".", "").split()
    if len(parts) < 2:
        return clean
    last = parts[-1]
    initials = "".join(p[0] for p in parts[:-1] if p and p[0].isalpha())
    return f"{last} {initials}".strip()


def parse_pubdate_year(pubdate: str) -> Optional[int]:
    """'2026 Apr 28' -> 2026; '2025 Jan-Feb' -> 2025; None on parse fail."""
    if not pubdate:
        return None
    m = re.match(r"(\d{4})", pubdate.strip())
    return int(m.group(1)) if m else None


def extract_field_terms(titles: list, max_terms: int = 8) -> list:
    """Tokenize titles, drop stopwords + short tokens, return top-N by frequency."""
    counter = Counter()
    for t in titles:
        words = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", (t or "").lower())
        for w in words:
            if w in STOPWORDS or len(w) <= 3:
                continue
            counter[w] += 1
    return [w for w, _ in counter.most_common(max_terms)]


def compute_confidence(probe: PersonProbe) -> tuple:
    """Return (score 0-1, notes). Counts either PMIDs (L1) or titles (L2)."""
    score = 0.0
    notes = []
    n = max(len(probe.recent_pmids), len(probe.recent_titles))
    if n == 0:
        notes.append("no recent pubs found")
        return 0.0, notes
    score += min(n / 10.0, 0.4)
    notes.append(f"{n} recent pubs (+{min(n/10.0, 0.4):.2f})")
    current_year = datetime.now().year
    recent_recent = sum(1 for y in probe.recent_years if y is not None and y >= current_year - 3)
    if recent_recent:
        bump = min(recent_recent / n, 1.0) * 0.4
        score += bump
        notes.append(f"{recent_recent}/{n} in last 3yr (+{bump:.2f})")
    if probe.field_terms:
        score += 0.2
        notes.append(f"{len(probe.field_terms)} field terms extracted (+0.20)")
    return round(min(score, 1.0), 2), notes


def parse_display_name(display_name: str) -> tuple:
    """'Neil D. Romberg, MD' -> ('Neil', 'Romberg'). For ORCID search."""
    clean = re.sub(r",.*$", "", display_name).strip()
    parts = [p.replace(".", "") for p in clean.split() if p.replace(".", "")]
    if len(parts) < 2:
        return (clean, "")
    return (parts[0], parts[-1])


def orcid_disambiguate(display_name: str) -> Optional[str]:
    """
    Find an ORCID iD by family-name + given-names, preferring matches whose
    institution-name appears in KNOWN_AFFILIATIONS. Returns the iD or None.
    """
    given, family = parse_display_name(display_name)
    if not family or not given:
        return None
    q = f"family-name:{family}+AND+given-names:{given}"
    raw = _http_get(f"{ORCID_SEARCH}?q={q}&rows=10")
    if raw is None:
        return None
    try:
        results = json.loads(raw).get("expanded-result") or []
    except json.JSONDecodeError:
        return None
    if not results:
        return None
    if len(results) == 1:
        return results[0].get("orcid-id")
    # Disambiguate by institution-name hit.
    for r in results:
        institutions = " ".join(r.get("institution-name") or [])
        if any(hint in institutions for hint in KNOWN_AFFILIATIONS):
            return r.get("orcid-id")
    return None


def orcid_fetch_works(orcid_id: str, max_results: int = 10) -> list:
    """Return list of dicts: {title, year, venue}."""
    raw = _http_get(ORCID_WORKS.format(iid=orcid_id))
    if raw is None:
        return []
    try:
        groups = json.loads(raw).get("group") or []
    except json.JSONDecodeError:
        return []
    works = []
    for g in groups:
        summary = (g.get("work-summary") or [{}])[0]
        title = ((summary.get("title") or {}).get("title") or {}).get("value") or ""
        year_node = (summary.get("publication-date") or {}).get("year") or {}
        year_raw = year_node.get("value")
        try:
            year = int(year_raw) if year_raw else None
        except (TypeError, ValueError):
            year = None
        venue = (summary.get("journal-title") or {}).get("value") or ""
        works.append({"title": title, "year": year, "venue": venue})
    works.sort(key=lambda w: (w["year"] or 0), reverse=True)
    return works[:max_results]


def probe_orcid(display_name: str) -> Optional[PersonProbe]:
    """
    Layer 2: ORCID lookup. Returns a PersonProbe on success, None if no
    unambiguous iD found.
    """
    orcid_id = orcid_disambiguate(display_name)
    if not orcid_id:
        return None
    time.sleep(0.34)
    works = orcid_fetch_works(orcid_id)
    if not works:
        return None
    p = PersonProbe(
        name=display_name,
        pubmed_query=f"orcid:{orcid_id}",
        layer_used="L2_orcid",
        fetched_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    )
    p.recent_titles = [w["title"] for w in works]
    p.recent_venues = [w["venue"] for w in works]
    p.recent_years = [w["year"] for w in works]
    p.recent_pmids = []  # ORCID often doesn't have PMIDs linked
    p.field_terms = extract_field_terms(p.recent_titles)
    p.confidence_notes.append(f"orcid_id={orcid_id}")
    p.confidence, conf_notes = compute_confidence(p)
    p.confidence_notes.extend(conf_notes)
    # ORCID iD with institutional match is strong signal — bump baseline.
    p.confidence = round(min(p.confidence + 0.1, 1.0), 2)
    return p


def probe_pubmed(display_name: str, max_results: int = 10) -> PersonProbe:
    pubmed_q = normalize_name_for_pubmed(display_name)
    p = PersonProbe(
        name=display_name,
        pubmed_query=pubmed_q,
        fetched_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    )
    term = quote(f"{pubmed_q}[Author]")
    search_url = f"{ESEARCH}?db=pubmed&term={term}&retmax={max_results}&retmode=json"
    raw = _http_get(search_url)
    if raw is None:
        p.error = "esearch HTTP failure"
        return p
    try:
        search = json.loads(raw).get("esearchresult", {})
    except json.JSONDecodeError:
        p.error = "esearch JSON parse failure"
        return p
    p.recent_pmids = list(search.get("idlist", []))
    try:
        p.total_pubmed_count = int(search.get("count", 0))
    except (TypeError, ValueError):
        p.total_pubmed_count = 0

    if not p.recent_pmids:
        p.confidence, p.confidence_notes = compute_confidence(p)
        return p

    time.sleep(0.34)  # NCBI fair-use: <=3 req/sec without API key
    sum_url = f"{ESUMMARY}?db=pubmed&id={','.join(p.recent_pmids)}&retmode=json"
    raw = _http_get(sum_url)
    if raw is None:
        p.error = "esummary HTTP failure"
        p.confidence, p.confidence_notes = compute_confidence(p)
        return p
    try:
        sumdata = json.loads(raw).get("result", {})
    except json.JSONDecodeError:
        p.error = "esummary JSON parse failure"
        p.confidence, p.confidence_notes = compute_confidence(p)
        return p

    for pmid in p.recent_pmids:
        rec = sumdata.get(pmid)
        if not rec:
            continue
        p.recent_titles.append(rec.get("title", ""))
        p.recent_venues.append(rec.get("fulljournalname", "") or rec.get("source", ""))
        p.recent_years.append(parse_pubdate_year(rec.get("pubdate", "")))

    p.field_terms = extract_field_terms(p.recent_titles)
    p.confidence, p.confidence_notes = compute_confidence(p)
    return p


def probe_with_fallback(display_name: str) -> PersonProbe:
    """
    Layer 1 PubMed first; on low-confidence or too-few results, try L2 ORCID.
    Keep whichever yields higher confidence.
    """
    l1 = probe_pubmed(display_name)
    needs_l2 = (
        l1.confidence <= L2_TRIGGER_CONFIDENCE
        or len(l1.recent_pmids) < L2_TRIGGER_PMID_COUNT
    )
    if not needs_l2:
        return l1
    l2 = probe_orcid(display_name)
    if l2 is None:
        l1.confidence_notes.append("L2 ORCID attempted, no unambiguous iD")
        return l1
    if l2.confidence > l1.confidence:
        l2.confidence_notes.append(f"L1 superseded (L1 conf={l1.confidence})")
        return l2
    return l1


def extract_people_from_site(html: str) -> list:
    """Pull mentor/collaborator/peer names from each section."""
    people = []
    for section_id in ("collaborators", "peers", "mentors"):
        sec = re.search(rf'<section id="{section_id}".*?</section>', html, re.DOTALL)
        if not sec:
            continue
        for m in re.finditer(
            r'<h3[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>\s*</h3>', sec.group(0)
        ):
            url, name = m.group(1), m.group(2).strip()
            people.append({"name": name, "url": url, "section": section_id})
    return people


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", help="single-name PubMed probe (e.g. 'Muglia LJ')")
    ap.add_argument("--from-site", action="store_true", help="scrape every person from the site")
    ap.add_argument("--site", default=str(SITE))
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    if args.probe:
        probe = probe_with_fallback(args.probe)
        print(json.dumps(asdict(probe), indent=2))
        return 0

    if args.from_site:
        html = Path(args.site).read_text(encoding="utf-8")
        people = extract_people_from_site(html)
        print(f"Found {len(people)} people; probing PubMed (L1) + ORCID fallback (L2)...", file=sys.stderr)
        records = []
        for p in people:
            probe = probe_with_fallback(p["name"])
            probe_dict = asdict(probe)
            probe_dict["url"] = p["url"]
            probe_dict["section"] = p["section"]
            records.append(probe_dict)
            print(
                f"  {p['name']!r} -> {len(probe.recent_pmids)} pubs, "
                f"conf={probe.confidence}, terms={probe.field_terms[:3]}",
                file=sys.stderr,
            )
            time.sleep(0.5)
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps({
            "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "source": "pubmed_eutils_L1",
            "records": records,
        }, indent=2))
        print(f"Wrote {args.out}", file=sys.stderr)
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())

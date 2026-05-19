# Contract — Archivist → Ace Scout publication feed

**Producer**: Archivist (MR-VitaminD-Asthma project)
**Consumer**: Ace Scout (Roizen Lab — hypothesisdriven.org Publications section)
**Status**: DRAFT — awaiting Archivist counter-signature via Kleiber
**Drafted**: 2026-05-19 by Ace Scout per `/contract-test` skill

## Why this contract exists

Today the Roizen Lab site's Publications section is fed by a hand-curated `docs/publications_data.md` (compiled 2026-02-25). The completeness warning in that file says: "Most recent full CV is dated Feb 2017... Jeff should verify against NCBI My Bibliography." That is a Data Provenance violation (`docs/cm_operating_model.md` → Data Provenance): no `data_as_of` field, no freshness indicator, no automated re-fetch. Tenure-committee letters arrive Sep 2026; the publications section will look stale by then unless this contract is in place.

Archivist owns the upstream MR analysis and the paper-ready figures for Jeff's MR work. They are the closest CM to the publications source-of-truth (Jeff's NCBI My Bibliography + Manuscripts/ folder). Hence the producer-consumer relationship.

## Shape (per-publication object)

```json
{
  "pmid": "39123456",
  "title": "Mendelian randomization shows BMI causally lowers 25(OH)D",
  "authors": ["Roizen JD", "Manousaki D", "..."],
  "venue": "Journal of Clinical Endocrinology & Metabolism",
  "year": 2025,
  "publication_date": "2025-08-14",
  "doi": "10.1210/clinem/dgae123",
  "pubmed_url": "https://pubmed.ncbi.nlm.nih.gov/39123456/",
  "research_arc": "phenotype",
  "first_author": false,
  "senior_author": true,
  "open_access": true
}
```

### Field-level requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `pmid` | string | yes | PubMed ID; primary key |
| `title` | string | yes | Verbatim from PubMed |
| `authors` | string[] | yes | Last name + initials, in PubMed order |
| `venue` | string | yes | Full journal name; not abbreviation |
| `year` | int | yes | 4-digit publication year |
| `publication_date` | ISO-8601 date | preferred | YYYY-MM-DD; year-only fallback `YYYY-01-01` |
| `doi` | string | yes when assigned | omit if not yet assigned (in-press) |
| `pubmed_url` | string | yes | Resolves to live PubMed page |
| `research_arc` | enum | yes | `phenotype` \| `mechanism` \| `translation` \| `other` — keyed to the 3 arcs on the site |
| `first_author` | bool | yes | true if Jeff is first author |
| `senior_author` | bool | yes | true if Jeff is last/corresponding |
| `open_access` | bool | preferred | drives an "open access" badge on the site |

## Semantics

- **`research_arc`** maps to the three Q-arcs on the site (`#arc-phenotype`, `#arc-mechanism`, `#arc-translation`). The site renders publications grouped by arc; ambiguous → `other` and Ace Scout surfaces to Jeff for assignment, but Archivist must make the call (not leave null).
- **Manuscripts in preparation/revision** are NOT in this feed. They live in a separate `manuscripts_in_progress` feed (out of scope here — own contract later if Jeff wants them surfaced).
- **Co-author papers without Jeff as first/senior** are included but tagged `first_author=false senior_author=false`; the site filters by default to show first+senior, with a "Show all" toggle.

## Freshness

- **Max staleness**: 7 days. Archivist re-runs an NCBI My Bibliography fetch weekly; feed is published with `data_as_of` set to the fetch timestamp.
- **`fetched_at`** is when Ace Scout pulled the feed; **`data_as_of`** is when Archivist last verified against PubMed. These are distinct per the Data Provenance rule.
- If `data_as_of` is more than 14 days stale at site render time, Ace Scout surfaces a "Publications list verified through {date}" line in the section (no silent serving of stale data).

## Transport

Two options, decided jointly:

| Option | Pros | Cons |
|---|---|---|
| A: file in shared dir (`~/orchestra-data/archivist/publications.json`) | Simple, no service | Manual schedule; no push |
| B: HTTP endpoint on Pilot Railway (Archivist writes, Ace Scout reads) | Push semantics; cached | Needs Railway endpoint + auth |

**Default**: A for now (zero infra), B once Pilot Railway endpoint is live. Both write a top-level envelope:

```json
{
  "data_as_of": "2026-05-19T16:00:00Z",
  "fetched_from": "ncbi_mybibliography_50863673",
  "publications": [ ... ]
}
```

## Failure modes the contract must protect against

1. **NCBI rate-limit**: Archivist retries with exponential backoff; serves last-known-good feed with original `data_as_of` (NOT silently bumped).
2. **PubMed schema drift**: if a required field is missing from the upstream parse, that publication is dropped from the feed and logged to `archivist/publications_dropped.jsonl`; rest of the feed is still served.
3. **Ace Scout reads with no feed file**: site falls back to the static `docs/publications_data.md` AND renders a banner: "Live publications feed temporarily unavailable — list as of 2026-02-25."

## Tests (consumer side — Ace Scout owns)

`tests/test_publications_contract.py` should assert:

1. Given a sample envelope, parser extracts all fields and validates types.
2. Missing required field → publication dropped, warning logged, rest parsed.
3. Stale `data_as_of` (>14 days) → renders staleness banner.
4. Missing feed file → falls back to `docs/publications_data.md` without crashing.
5. `research_arc` enum strictly: `phenotype` | `mechanism` | `translation` | `other`; anything else → `other` + warning.

## Tests (producer side — Archivist owns)

To be written by Archivist:

1. NCBI My Bibliography 50863673 fetch returns N publications; spot-check one PMID's title against `pubmed.ncbi.nlm.nih.gov/{pmid}`.
2. `research_arc` classifier covers all current publications (no nulls in the canonical sample).
3. Manuscripts in preparation are NOT in the published feed.

## Action items (route via Kleiber)

1. **Send this contract to Archivist** for counter-signature.
2. **Archivist confirms** field list, transport choice (A or B), and weekly cadence.
3. **Archivist ships v0** to `~/orchestra-data/archivist/publications.json` (option A); Ace Scout wires the consumer-side parser + tests.
4. **First end-to-end run** validated against a live sample before swapping out `docs/publications_data.md` on the site.

## Open questions for Archivist (NOT for Jeff)

- Does Archivist already have an NCBI My Bibliography parser, or does this contract trigger building one?
- Is there an existing JSON publication record format in MR-VitaminD-Asthma we should align to instead of inventing this shape?
- Who owns `research_arc` classification rules? Archivist alone, or do they pass through to a separate classifier and Ace Scout consumes both?

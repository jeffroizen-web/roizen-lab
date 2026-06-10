#!/usr/bin/env python3
"""producer_readback_ccc_review.py — Layer-4 /ccc backstop for Producer-Read-Back.

Reads the session ledger of external writes (appended by producer_readback_check.py)
and surfaces them at /ccc so the agent can confirm each was read back before
closing the session — catching any write the per-turn nudge missed.

Advisory only: lists writes, exit 0 always, never blocks.

Usage:
  producer_readback_ccc_review.py [--session <id>] [--since-hours N]
  # /ccc passes the current session_id; falls back to a time window otherwise.
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta

LEDGER = os.environ.get("PRODUCER_READBACK_LEDGER") or os.path.expanduser(
    "~/.kleiber/logs/producer_readback_writes.jsonl"
)


def load(session=None, since_hours=12):
    if not os.path.exists(LEDGER):
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)
    out = []
    try:
        with open(LEDGER) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if session is not None:
                    if rec.get("session_id") == session:
                        out.append(rec)
                    continue
                ts = rec.get("ts", "")
                try:
                    when = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
                        tzinfo=timezone.utc
                    )
                except Exception:
                    continue
                if when >= cutoff:
                    out.append(rec)
    except Exception:
        return []
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", default=None)
    ap.add_argument("--since-hours", type=int, default=12)
    args = ap.parse_args()

    writes = load(args.session, args.since_hours)
    if not writes:
        print(
            "✓ Producer-Read-Back: no external writes logged this window — nothing to confirm."
        )
        return 0

    scope = f"session {args.session}" if args.session else f"last {args.since_hours}h"
    print(
        f"⊕ Producer-Read-Back /ccc backstop — {len(writes)} external write(s) logged ({scope})."
    )
    print("  Confirm each was read back (re-fetched + asserted landed == intent):")
    for r in writes:
        print(f"  - [{r.get('ts', '?')}] {r.get('command', '?')}")
    print("  If any was NOT read back, do it now before /ccc closes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

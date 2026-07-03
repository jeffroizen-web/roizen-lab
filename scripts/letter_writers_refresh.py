#!/usr/bin/env python3
"""
Weekly refresh of docs/letter_writers.json with confidence-regression detection.

Workflow:
  1. Read prior docs/letter_writers.json (if any) into a {name: confidence} map.
  2. Run the full from-site scrape, overwriting letter_writers.json.
  3. Diff per-person confidence; record drops >= REGRESSION_THRESHOLD as regressions.
  4. Re-run wire_letter_writers so the site reflects the new data.
  5. Emit research.commit event to the bus (gated by CROSS_CM_BUS_TRIAL_ENABLED):
     - outcome=routine-refresh on every run (low conf bucket)
     - outcome=confidence-regression with the dropped names (exact conf bucket)
       if any person's confidence fell by >= REGRESSION_THRESHOLD

Run:
    python3 scripts/letter_writers_refresh.py
        (typically via the launchd plist, weekly Sunday 03:00 EDT)
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from bus_emit import emit  # noqa: E402

DATA = ROOT / "docs" / "letter_writers.json"
PREV = ROOT / "docs" / "letter_writers_prev.json"
REGRESSION_THRESHOLD = 0.2


def confidence_map(payload: dict) -> dict:
    return {r["name"]: float(r.get("confidence", 0.0)) for r in payload.get("records", [])}


def find_regressions(prior: dict, current: dict, threshold: float = REGRESSION_THRESHOLD) -> list:
    out = []
    for name, prior_conf in prior.items():
        new_conf = current.get(name)
        if new_conf is None:
            out.append({"name": name, "prior": prior_conf, "new": None, "reason": "missing"})
            continue
        if prior_conf - new_conf >= threshold:
            out.append({"name": name, "prior": prior_conf, "new": new_conf,
                        "reason": f"drop {prior_conf - new_conf:.2f}"})
    return out


def main():
    prior_map = {}
    if DATA.exists():
        try:
            prior_payload = json.loads(DATA.read_text(encoding="utf-8"))
            prior_map = confidence_map(prior_payload)
            PREV.write_text(json.dumps(prior_payload, indent=2))
        except json.JSONDecodeError:
            prior_map = {}

    # Re-scrape.
    scrape = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "letter_writer_scrape.py"), "--from-site"],
        capture_output=True, text=True,
    )
    if scrape.returncode != 0:
        print(f"scrape failed: {scrape.stderr}", file=sys.stderr)
        return 1

    if not DATA.exists():
        print("letter_writers.json missing after scrape", file=sys.stderr)
        return 1

    new_payload = json.loads(DATA.read_text(encoding="utf-8"))
    new_map = confidence_map(new_payload)
    regressions = find_regressions(prior_map, new_map)

    # Re-wire into the site so the surface reflects the refresh.
    wire = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "wire_letter_writers.py")],
        capture_output=True, text=True,
    )
    if wire.returncode != 0:
        print(f"wire failed: {wire.stderr}", file=sys.stderr)
        # Continue to emit anyway — scrape succeeded, just surface is stale.

    # Routine heartbeat.
    routine_emit = emit("research.commit", {
        "outcome": "routine-refresh",
        "project": "roizen-lab-site",
        "people_count": len(new_map),
        "data_as_of": new_payload.get("generated_at"),
    }, confidence=0.4)

    # Regression alert if any.
    regression_emit = None
    if regressions:
        regression_emit = emit("research.commit", {
            "outcome": "confidence-regression",
            "project": "roizen-lab-site",
            "regressions": regressions,
        }, confidence=0.9)

    summary = {
        "refreshed_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        # Drift is a FINDING carried here + in the emitted regression event, NOT in
        # the exit code (R2 / exit-code-outcome-mismatch, 2026-07-03). A successful
        # regression-detect is a successful run — launchd reads nonzero as a crash.
        "outcome": "drift-detected" if regressions else "clean",
        "people_count": len(new_map),
        "regressions": regressions,
        "routine_emit": routine_emit.get("status"),
        "regression_emit": regression_emit.get("status") if regression_emit else None,
    }
    print(json.dumps(summary, indent=2))
    # Exit 0 on a successful run whether or not drift was found. nonzero is reserved
    # for genuine execution failure (scrape/IO/parse), handled by the early returns above.
    return 0


if __name__ == "__main__":
    sys.exit(main())

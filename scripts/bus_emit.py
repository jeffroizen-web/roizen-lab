#!/usr/bin/env python3
"""
Minimal cross-CM event bus emitter for Ace Scout.

POSTs to Pilot's trial bus endpoint with Bearer auth.

ENV:
    CROSS_CM_BUS_TRIAL_ENABLED   "1" to actually POST; anything else = dry-run log only
    CROSS_CM_BUS_ENDPOINT        full URL of the bus events endpoint
    TRIAL_BUS_TOKEN              Bearer token (or fetched via scripts/get-fitness-cred.sh)

Public API:
    emit(kind: str, payload: dict, *, source: str = "ace-scout",
         subject_date: str | None = None, confidence: float = 1.0,
         dry_run: bool | None = None, endpoint: str | None = None,
         token: str | None = None) -> dict

Returns a dict with: status (delivered|dry-run|skipped|error), bus_response (or None),
audit_path (where the line was logged).
"""
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union
from urllib.error import URLError, HTTPError
from urllib.request import urlopen, Request

ROOT = Path(__file__).resolve().parent.parent
AUDIT_LOG = ROOT / "decisions" / "bus_emit_log.jsonl"

DEFAULT_ENDPOINT = "https://ulysses-production.up.railway.app/api/role-balance-trial/events"

# Pilot's bus accepts STRING confidence values, not numeric (per Kleiber MSG-b14dd7,
# cross-pollinated from AquaErg MSG-af3b42). Internal callers still pass a float in
# [0, 1]; we bucket-map to the canonical strings on the wire.
CONFIDENCE_BUCKETS = (
    (0.90, "exact"),
    (0.70, "high"),
    (0.50, "medium"),
    (0.30, "low"),
    (0.00, "very-low"),
)


def confidence_to_string(value: Union[float, int, str]) -> str:
    """Map a numeric confidence to Pilot's accepted string bucket. Strings pass through."""
    if isinstance(value, str):
        return value
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "very-low"
    for threshold, label in CONFIDENCE_BUCKETS:
        if v >= threshold:
            return label
    return "very-low"


def _is_enabled() -> bool:
    return os.environ.get("CROSS_CM_BUS_TRIAL_ENABLED", "0") == "1"


def _fetch_token() -> Optional[str]:
    """Token resolution: env var first, then the fitness-cred helper."""
    tok = os.environ.get("TRIAL_BUS_TOKEN")
    if tok:
        return tok
    helper = ROOT / "scripts" / "get-fitness-cred.sh"
    if not helper.exists():
        return None
    try:
        result = subprocess.run(
            ["bash", str(helper), "TRIAL_BUS_TOKEN", "ace-scout"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, OSError):
        pass
    return None


def _audit_write(entry: dict) -> Path:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return AUDIT_LOG


def emit(
    kind: str,
    payload: dict,
    *,
    source: str = "ace-scout",
    subject_date: Optional[str] = None,
    confidence: float = 1.0,
    dry_run: Optional[bool] = None,
    endpoint: Optional[str] = None,
    token: Optional[str] = None,
    timeout: int = 5,
) -> dict:
    """Emit an event to the cross-CM bus. Idempotent at the audit-log level."""
    if not kind or not isinstance(payload, dict):
        raise ValueError("kind required (str), payload required (dict)")

    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    subject = subject_date or now[:10]
    # Pilot's API schema (per MSG-b14dd7): camelCase keys, string confidence, required eventId/emittedAt.
    event = {
        "eventId": f"ace-scout-{kind}-{uuid.uuid4().hex[:12]}",
        "emittedBy": source,
        "emittedAt": now,
        "subjectDate": subject,
        "kind": kind,
        "payload": payload,
        "confidence": confidence_to_string(confidence),
    }

    effective_endpoint = endpoint or os.environ.get("CROSS_CM_BUS_ENDPOINT") or DEFAULT_ENDPOINT
    effective_token = token or _fetch_token()
    if dry_run is None:
        dry_run = not _is_enabled()

    audit_entry = {
        "event": event,
        "endpoint": effective_endpoint,
        "dry_run": dry_run,
        "token_present": bool(effective_token),
    }

    if dry_run:
        audit_entry["status"] = "dry-run"
        path = _audit_write(audit_entry)
        return {"status": "dry-run", "bus_response": None, "audit_path": str(path)}

    if not effective_token:
        audit_entry["status"] = "skipped"
        audit_entry["reason"] = "no token"
        path = _audit_write(audit_entry)
        return {"status": "skipped", "bus_response": None, "audit_path": str(path)}

    body = json.dumps(event).encode("utf-8")
    req = Request(
        effective_endpoint,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {effective_token}",
            "User-Agent": "ace-scout-bus-emit/1.0",
        },
    )
    started = time.monotonic()
    try:
        with urlopen(req, timeout=timeout) as r:
            response_text = r.read().decode("utf-8", errors="replace")
            try:
                response_json = json.loads(response_text)
            except json.JSONDecodeError:
                response_json = {"raw": response_text}
            audit_entry["status"] = "delivered"
            audit_entry["http_status"] = r.status
            audit_entry["latency_ms"] = int((time.monotonic() - started) * 1000)
            audit_entry["bus_response"] = response_json
            path = _audit_write(audit_entry)
            return {"status": "delivered", "bus_response": response_json, "audit_path": str(path)}
    except HTTPError as e:
        # Per Kleiber MSG-b14dd7, Pilot returns a JSON body with errors:[] on 400.
        # Capture it so the audit log shows exactly which fields failed validation.
        body = None
        try:
            body_raw = e.read().decode("utf-8", errors="replace")
            try:
                body = json.loads(body_raw)
            except json.JSONDecodeError:
                body = {"raw": body_raw}
        except Exception:
            pass
        audit_entry["status"] = "error"
        audit_entry["http_status"] = e.code
        audit_entry["error"] = f"HTTPError {e.code}"
        audit_entry["bus_response"] = body
        path = _audit_write(audit_entry)
        return {"status": "error", "bus_response": body, "audit_path": str(path)}
    except (URLError, TimeoutError, OSError) as e:
        audit_entry["status"] = "error"
        audit_entry["error"] = str(e)
        path = _audit_write(audit_entry)
        return {"status": "error", "bus_response": None, "audit_path": str(path)}


def main():
    """CLI: emit a manually-built event. Use sparingly — most emits are from scripts."""
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True)
    ap.add_argument("--payload-json", required=True, help="JSON-encoded payload object")
    ap.add_argument("--confidence", type=float, default=1.0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    payload = json.loads(args.payload_json)
    result = emit(args.kind, payload, confidence=args.confidence, dry_run=args.dry_run or None)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in ("delivered", "dry-run") else 1


if __name__ == "__main__":
    sys.exit(main())

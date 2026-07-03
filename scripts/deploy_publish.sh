#!/usr/bin/env bash
# Gated auto-redeploy of the lean GitHub Pages artifact (Kleiber MSG-006188).
#
# WHY: the `gh-pages` serving branch is a SNAPSHOT of the canonical page. When a
# cron re-wires the canonical (weekly letter-writers refresh, weekly publications
# refresh), the snapshot goes stale. This script re-syncs + redeploys so canonical
# changes auto-serve — WITHOUT a human in the loop, so every guard is mechanical.
#
# SOURCE-OF-TRUTH DECISION (the design finding, resolved): we deploy the
# WORKING-TREE canonical (compare-purple-gold.html as-is, INCLUDING the live cron
# field-of-interest diff), NOT committed main. Rationale: gh-pages is a DERIVED
# serving artifact, not source — it legitimately reflects current live content.
# sync_publish.py already byte-copies the working tree (the hash-match test
# enforces publish/index.html == working-tree canonical). Consequence: the cron
# does NOT auto-commit the foi, so the clean-attribution model is UNCHANGED
# (my commits still HEAD-reconstruct to exclude the foi; gh-pages carries the
# live working-tree state). See [[reference-html-edit-cron-foi-clean-attribution]].
#
# SAFETY (auto-force-push to a PUBLIC branch = a standing automated external
# action → every Tier-2 guard is mechanical here):
#   1. KILL-SWITCH: ROIZEN_AUTO_DEPLOY must == 1, else DISARMED (default). A
#      disarmed run logs outcome=disarmed and exits 0 — a PASS, not a no-op
#      (Daily-Fire Route-Side-Gate: every path writes an observable outcome).
#   2. GATE: sync_publish --check (no missing assets) + the publish-sync hash
#      test (publish/index.html == canonical). Gate-fail → NO deploy, exit 1.
#   3. CHANGE-DETECT: canonical sha256 vs last-deployed hash; unchanged → skip
#      (no no-op force-push), outcome=no-change, exit 0.
#   4. READ-BACK: fetch the live URL cache-busted, sha256, assert == the bytes
#      just deployed (retries for CDN propagation lag). Finding rides the log +
#      stderr, NOT the exit code (R2 / exit-code-outcome-mismatch: the exit code
#      encodes "did the job RUN", never "what did it find").
#   5. FAILURE-LEDGER: a push transport flake → git-push-transport-flaky row.
#
# ARMING (Jeff/Kleiber-gated — NOT done by building this file):
#   - set ROIZEN_AUTO_DEPLOY=1 in the cron's environment, AND
#   - point the letter_writers plist at scripts/letter_writers_refresh_cron.sh
#     (which runs the refresh, then calls this).
# Until armed, this file is inert (kill-switch defaults OFF).
#
# On-demand (safe): ROIZEN_DEPLOY_DRY_RUN=1 bash scripts/deploy_publish.sh
#   does everything EXCEPT the real force-push + real network read-back.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

CANONICAL="$REPO_ROOT/compare-purple-gold.html"
PUBLISH_DIR="$REPO_ROOT/publish"
REMOTE_URL="${ROIZEN_DEPLOY_REMOTE:-https://github.com/jeffroizen-web/roizen-lab.git}"
LIVE_URL="${ROIZEN_DEPLOY_LIVE_URL:-https://jeffroizen-web.github.io/roizen-lab/}"
STATE_FILE="${ROIZEN_DEPLOY_STATE:-$REPO_ROOT/docs/reports/.deploy_last_hash}"
LOG_FILE="${ROIZEN_DEPLOY_LOG:-$REPO_ROOT/docs/reports/deploy-publish.jsonl}"
DRY_RUN="${ROIZEN_DEPLOY_DRY_RUN:-0}"
LOG_FAILURE="/Users/roizenj/Code/Claude Apps/Claude coding Asst/scripts/log_failure.py"

mkdir -p "$(dirname "$STATE_FILE")" "$(dirname "$LOG_FILE")"

now_utc() { date -u +%Y-%m-%dT%H:%M:%SZ; }

# Append one observable outcome row (Daily-Fire Route-Side-Gate).
log_outcome() {
    # $1 = outcome, $2 = detail
    python3 - "$1" "$2" "$LOG_FILE" <<'PY'
import json, sys, datetime
outcome, detail, path = sys.argv[1], sys.argv[2], sys.argv[3]
row = {"ts": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
       "outcome": outcome, "detail": detail}
with open(path, "a") as f:
    f.write(json.dumps(row) + "\n")
print(f"[deploy_publish] outcome={outcome} detail={detail}", file=sys.stderr)
PY
}

canonical_hash() { shasum -a 256 "$CANONICAL" | awk '{print $1}'; }

# ---- 1. KILL-SWITCH -------------------------------------------------------
if [ "${ROIZEN_AUTO_DEPLOY:-0}" != "1" ]; then
    log_outcome disarmed "ROIZEN_AUTO_DEPLOY!=1 (default OFF); no deploy attempted"
    exit 0
fi

CANON_HASH="$(canonical_hash)"

# ---- 3. CHANGE-DETECT (before the expensive gate) -------------------------
LAST_HASH="$(cat "$STATE_FILE" 2>/dev/null || echo '')"
if [ "$CANON_HASH" = "$LAST_HASH" ]; then
    log_outcome no-change "canonical unchanged since last deploy (${CANON_HASH:0:16})"
    exit 0
fi

# ---- 2. GATE (only when there IS a change to ship) ------------------------
if ! python3 scripts/sync_publish.py --check >/dev/null 2>&1; then
    log_outcome gate-failed "sync_publish --check reported missing referenced assets"
    exit 1
fi
if ! python3 -m pytest tests/test_publish_sync.py -q >/dev/null 2>&1; then
    log_outcome gate-failed "tests/test_publish_sync.py failed (publish != canonical / heavy-tree leak)"
    exit 1
fi

# sync_publish --check already rebuilt publish/; the hash-match test re-ran build().
DEPLOY_HASH="$(shasum -a 256 "$PUBLISH_DIR/index.html" | awk '{print $1}')"
if [ "$DEPLOY_HASH" != "$CANON_HASH" ]; then
    log_outcome gate-failed "publish/index.html hash != canonical (${DEPLOY_HASH:0:16} != ${CANON_HASH:0:16})"
    exit 1
fi

# ---- 4a. DEPLOY (force-push the lean artifact to gh-pages) -----------------
if [ "$DRY_RUN" = "1" ]; then
    log_outcome deployed-dry-run "would force-push publish/ (${CANON_HASH:0:16}) to gh-pages; no network side effect"
    echo "$CANON_HASH" > "$STATE_FILE"
    exit 0
fi

TMP_GHP="$(mktemp -d)"
trap 'rm -rf "$TMP_GHP"' EXIT
cp -R "$PUBLISH_DIR"/. "$TMP_GHP"/
(
    cd "$TMP_GHP"
    git init -q -b gh-pages
    git add -A
    git -c user.email=deploy@hypothesisdriven.org -c user.name="Ace Scout Deploy" \
        commit -qm "deploy: ${CANON_HASH:0:16} ($(now_utc))"
)
PUSH_OK=0
for attempt in 1 2; do
    if git -C "$TMP_GHP" push -f "$REMOTE_URL" gh-pages >/dev/null 2>&1; then
        PUSH_OK=1
        [ "$attempt" -gt 1 ] && python3 "$LOG_FAILURE" --cm ace-scout \
            --failure-class git-push-transport-flaky --severity default \
            --surface gh-pages-deploy --resolution workaround \
            --what-dropped "gh-pages force-push retried; attempt $attempt recovered" >/dev/null 2>&1
        break
    fi
    sleep 5
done
if [ "$PUSH_OK" != "1" ]; then
    log_outcome push-failed "git push -f gh-pages failed after retries (${CANON_HASH:0:16})"
    python3 "$LOG_FAILURE" --cm ace-scout --failure-class git-push-transport-flaky \
        --severity default --surface gh-pages-deploy --resolution workaround \
        --what-dropped "gh-pages force-push failed after 2 attempts; live site not updated to ${CANON_HASH:0:16}" >/dev/null 2>&1
    exit 1
fi

# Push succeeded → the job RAN. Persist the deployed hash now (R2: exit code
# encodes execution, not the read-back finding below).
echo "$CANON_HASH" > "$STATE_FILE"

# ---- 4b. READ-BACK (byte-exact; findings ride the log, not the exit code) -
READBACK="pending"
for attempt in 1 2 3 4 5; do
    SERVED_HASH="$(curl -fsSL "${LIVE_URL}?cb=$(date +%s)-$attempt" 2>/dev/null | shasum -a 256 | awk '{print $1}')"
    if [ "$SERVED_HASH" = "$CANON_HASH" ]; then
        READBACK="verified"
        break
    fi
    sleep 6
done
if [ "$READBACK" = "verified" ]; then
    log_outcome deployed "live bytes == deployed canonical (${CANON_HASH:0:16}), read-back verified"
else
    # Propagation lag is the common cause (push succeeded); LOUD but exit 0 (R2).
    log_outcome deployed-readback-pending "pushed ${CANON_HASH:0:16}; live read-back did not converge in window (likely CDN lag)"
fi
exit 0

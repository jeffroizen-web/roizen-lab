#!/usr/bin/env bash
# Cron/launchd wrapper for the tenure-readiness watcher.
#
# Runs the watcher; writes a dated report; on regression, optionally emits
# a `site.audit.regression` event to the cross-CM trial bus (gated by
# CROSS_CM_BUS_TRIAL_ENABLED=1).
#
# Install (one-time, run by Jeff or with Jeff's approval — touches launchd):
#   cp scripts/com.hypothesisdriven.tenure_readiness.plist ~/Library/LaunchAgents/
#   launchctl bootstrap gui/$UID ~/Library/LaunchAgents/com.hypothesisdriven.tenure_readiness.plist
#
# Uninstall:
#   launchctl bootout gui/$UID ~/Library/LaunchAgents/com.hypothesisdriven.tenure_readiness.plist
#   rm ~/Library/LaunchAgents/com.hypothesisdriven.tenure_readiness.plist
#
# This script is also runnable on demand: `bash scripts/tenure_readiness_cron.sh`

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

REPORT_DIR="$REPO_ROOT/docs/reports"
mkdir -p "$REPORT_DIR"
DATE_STAMP="$(date +%Y-%m-%d)"
REPORT_FILE="$REPORT_DIR/tenure-readiness-$DATE_STAMP.md"
JSON_FILE="$REPORT_DIR/tenure-readiness-$DATE_STAMP.json"

# Capture JSON for downstream emit; human report to the dated md file.
python3 scripts/tenure_readiness.py --json > "$JSON_FILE.tmp" 2>&1
EXIT_CODE=$?
mv "$JSON_FILE.tmp" "$JSON_FILE"

# Drift is carried in the JSON `outcome` field, NOT the exit code (R2 fix,
# 2026-07-03): EXIT_CODE is now 0 on a clean run OR a drift-detect, nonzero
# only on genuine execution failure. Read the finding from `outcome`.
OUTCOME="$(python3 -c "import json; print(json.load(open('$JSON_FILE')).get('outcome','?'))" 2>/dev/null || echo '?')"

{
    echo "# Tenure Readiness — $(date '+%Y-%m-%d %H:%M %Z')"
    echo ""
    echo '```'
    python3 scripts/tenure_readiness.py 2>&1 || true
    echo '```'
    echo ""
    echo "Exit code: $EXIT_CODE (0=ran ok, nonzero=execution failure) · outcome: $OUTCOME"
} > "$REPORT_FILE"

# Drift detected (a SUCCESSFUL finding, exit 0) — emit to cross-CM bus if enabled.
if [ "$OUTCOME" = "drift-detected" ]; then
    python3 -c "
import json, sys
sys.path.insert(0, 'scripts')
from bus_emit import emit
data = json.load(open('$JSON_FILE'))
result = emit(
    'research.commit',
    {
        'outcome': 'regression',
        'project': 'roizen-lab-site',
        'grade': data.get('findings', {}).get('grade', '?'),
        'regressions': data.get('regressions', []),
        'report_path': '$REPORT_FILE',
    },
    confidence=0.9,
)
print('bus emit:', result['status'], file=sys.stderr)
" 2>&1
fi

# Always emit a routine heartbeat (low-confidence advisory).
python3 -c "
import json, sys
sys.path.insert(0, 'scripts')
from bus_emit import emit
data = json.load(open('$JSON_FILE'))
findings = data.get('findings', {}) if isinstance(data, dict) and 'findings' in data else data
result = emit(
    'research.commit',
    {
        'outcome': 'heartbeat',
        'project': 'roizen-lab-site',
        'grade': findings.get('grade', '?'),
        'dead_link_count': len(findings.get('dead_hash_hrefs', [])),
        'figure_pending_count': findings.get('figure_pending_count', 0),
        'banned_phrase_count': len(findings.get('banned_phrases_found', [])),
    },
    confidence=0.4,
)
print('heartbeat emit:', result['status'], file=sys.stderr)
" 2>&1

# R4 (2026-07-03): bound the report footprint. The dated pairs are gitignored
# ephemeral cron output; keep a rolling `-latest` (always current) + the newest
# KEEP dated pairs on disk. Portable to BSD/macOS head (positive -n only).
cp "$JSON_FILE"   "$REPORT_DIR/tenure-readiness-latest.json"
cp "$REPORT_FILE" "$REPORT_DIR/tenure-readiness-latest.md"
KEEP=14
for ext in md json; do
    files="$(ls -1 "$REPORT_DIR"/tenure-readiness-20*."$ext" 2>/dev/null | sort)"
    count="$(printf '%s\n' "$files" | grep -c .)"
    if [ "$count" -gt "$KEEP" ]; then
        ndel=$((count - KEEP))
        printf '%s\n' "$files" | head -n "$ndel" | while read -r old; do
            [ -n "$old" ] && rm -f "$old"
        done
    fi
done

exit "$EXIT_CODE"

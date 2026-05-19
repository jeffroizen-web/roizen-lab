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

{
    echo "# Tenure Readiness — $(date '+%Y-%m-%d %H:%M %Z')"
    echo ""
    echo '```'
    python3 scripts/tenure_readiness.py 2>&1 || true
    echo '```'
    echo ""
    echo "Exit code: $EXIT_CODE (0=clean, 1=regression, 2=no baseline)"
} > "$REPORT_FILE"

# Regression — exit 1 — emit to cross-CM bus if enabled.
if [ "$EXIT_CODE" = "1" ]; then
    python3 -c "
import json, sys
sys.path.insert(0, 'scripts')
from bus_emit import emit
data = json.load(open('$JSON_FILE'))
result = emit(
    'site.audit.regression',
    {
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
    'site.audit.heartbeat',
    {
        'grade': findings.get('grade', '?'),
        'dead_link_count': len(findings.get('dead_hash_hrefs', [])),
        'figure_pending_count': findings.get('figure_pending_count', 0),
        'banned_phrase_count': len(findings.get('banned_phrases_found', [])),
    },
    confidence=0.4,
)
print('heartbeat emit:', result['status'], file=sys.stderr)
" 2>&1

exit "$EXIT_CODE"

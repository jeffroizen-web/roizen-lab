#!/usr/bin/env bash
# T8 — R-5 / R-7 instrument: reproducible Lighthouse + axe runner (craft-uplift spec).
#
# Produces LCP_ms, CLS, TBT_ms, Lighthouse perf/a11y scores, and axe violation
# counts appended as a fenced INSTRUMENT RESULTS block to the judged artifact.
# The loop asserts BLOCK-class budgets before the judge scores.
#
# Delta-amended perf assertion (architect review F4 + delta brief):
#   - Runs Lighthouse with DESKTOP preset + NO throttling (--throttling-method=provided)
#     so localhost LCP is comparable to the ~468ms production CDN baseline.
#   - BLOCK gate: desktop-preset LCP ≥ 2500ms OR LCP regression > 20% vs iter-1 baseline.
#   - Uses --headless=new (not deprecated --headless).
#
# axe is optional: if `npx @axe-core/cli` fails (network unavailable), the scan
# is recorded as "unavailable" — this is NOT a silent pass; R-7 BLOCK-class reduces
# to contrast-only (test_contrast.py) in that case.
#
# Usage:
#   ARTIFACT=compare-purple-gold.html  # path to the build artifact to judge
#   ITER=1                             # iteration number (1 on first run)
#   BASELINE_LCP=468                   # iter-1 LCP in ms (0 = not yet measured)
#   bash tests/instrument_cwv.sh
#
# Outputs:
#   /tmp/ace_pipe4_lh.json   — raw Lighthouse JSON
#   /tmp/ace_pipe4_axe.json  — raw axe JSON (if available)
#   Appended to $ARTIFACT:   INSTRUMENT RESULTS fenced block
#   Exit code 0 = PASS (all BLOCK-class budgets met)
#   Exit code 1 = BLOCK (at least one BLOCK-class budget missed)
#
# Run: bash tests/instrument_cwv.sh

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration (override via env)
# ---------------------------------------------------------------------------
ARTIFACT="${ARTIFACT:-compare-purple-gold.html}"
ITER="${ITER:-1}"
BASELINE_LCP="${BASELINE_LCP:-0}"   # 0 = not yet set; iter-1 sets it
HTTP_PORT="${HTTP_PORT:-8137}"
LH_JSON="/tmp/ace_pipe4_lh.json"
AXE_JSON="/tmp/ace_pipe4_axe.json"

# BLOCK-class budget thresholds (desktop-preset, no-throttle)
LCP_BLOCK_MS=2500          # absolute gate: LCP ≥ this → BLOCK
CLS_BLOCK=0.10             # CLS ≥ this → BLOCK
TBT_BLOCK_MS=200           # TBT ≥ this → BLOCK
LCP_REGRESSION_PCT=20      # LCP regression vs iter-1 baseline > this % → BLOCK

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# ---------------------------------------------------------------------------
# 1. Serve the worktree
# ---------------------------------------------------------------------------
echo "[T8] Starting HTTP server on port $HTTP_PORT ..."
python3 -m http.server "$HTTP_PORT" >/tmp/ace_pipe4_http.log 2>&1 &
HTTP_PID=$!
sleep 1   # allow server to start
URL="http://localhost:${HTTP_PORT}/${ARTIFACT}"

cleanup() {
  kill "$HTTP_PID" 2>/dev/null || true
}
trap cleanup EXIT

# ---------------------------------------------------------------------------
# 2. Run Lighthouse (desktop + no throttling for localhost comparability)
# ---------------------------------------------------------------------------
echo "[T8] Running Lighthouse (desktop, no throttle) against $URL ..."
npx --yes lighthouse "$URL" \
  --preset=desktop \
  --throttling-method=provided \
  --only-categories=performance,accessibility \
  --output=json \
  --output-path="$LH_JSON" \
  --quiet \
  --chrome-flags="--headless=new --no-sandbox" \
  || { echo "[T8] Lighthouse failed — check Chrome/npx availability"; exit 1; }

# ---------------------------------------------------------------------------
# 3. Extract metrics from Lighthouse JSON
# ---------------------------------------------------------------------------
extract_metric() {
  python3 -c "
import json, sys
data = json.load(open('$LH_JSON'))
key = sys.argv[1]
print(round(data['audits'][key]['numericValue'], 2))
" "$1" 2>/dev/null || echo "N/A"
}

LCP_MS=$(extract_metric "largest-contentful-paint")
CLS=$(extract_metric "cumulative-layout-shift")
TBT_MS=$(extract_metric "total-blocking-time")
LH_PERF=$(python3 -c "import json; d=json.load(open('$LH_JSON')); print(round(d['categories']['performance']['score']*100,1))" 2>/dev/null || echo "N/A")
LH_A11Y=$(python3 -c "import json; d=json.load(open('$LH_JSON')); print(round(d['categories']['accessibility']['score']*100,1))" 2>/dev/null || echo "N/A")

echo "[T8] LCP=${LCP_MS}ms  CLS=${CLS}  TBT=${TBT_MS}ms  Perf=${LH_PERF}  A11y=${LH_A11Y}"

# ---------------------------------------------------------------------------
# 4. Optional axe scan
# ---------------------------------------------------------------------------
AXE_CRITICAL="N/A"
AXE_SERIOUS="N/A"
AXE_MODERATE="N/A"
AXE_STATUS="unavailable"

if npx --yes @axe-core/cli "$URL" --exit 0 --save "$AXE_JSON" 2>/dev/null; then
  AXE_CRITICAL=$(python3 -c "
import json
d=json.load(open('$AXE_JSON'))
violations = d.get('violations', d) if isinstance(d, dict) else d
# axe-core/cli saves {violations:[...]} or an array
if isinstance(violations, list):
    vivs = violations
elif isinstance(violations, dict):
    vivs = violations.get('violations', [])
else:
    vivs = []
print(sum(1 for v in vivs if v.get('impact') == 'critical'))
" 2>/dev/null || echo "N/A")
  AXE_SERIOUS=$(python3 -c "
import json
d=json.load(open('$AXE_JSON'))
if isinstance(d, list): vivs=d
elif isinstance(d, dict): vivs=d.get('violations', [])
else: vivs=[]
print(sum(1 for v in vivs if v.get('impact') == 'serious'))
" 2>/dev/null || echo "N/A")
  AXE_MODERATE=$(python3 -c "
import json
d=json.load(open('$AXE_JSON'))
if isinstance(d, list): vivs=d
elif isinstance(d, dict): vivs=d.get('violations', [])
else: vivs=[]
print(sum(1 for v in vivs if v.get('impact') == 'moderate'))
" 2>/dev/null || echo "N/A")
  AXE_STATUS="measured"
fi

# ---------------------------------------------------------------------------
# 5. BLOCK-class budget assertions
# ---------------------------------------------------------------------------
BLOCK_REASONS=()

# LCP absolute gate
if [[ "$LCP_MS" != "N/A" ]]; then
  python3 -c "
import sys
lcp=float('$LCP_MS')
if lcp >= $LCP_BLOCK_MS:
    print(f'BLOCK: LCP {lcp}ms >= ${LCP_BLOCK_MS}ms')
    sys.exit(1)
" || BLOCK_REASONS+=("LCP ${LCP_MS}ms >= ${LCP_BLOCK_MS}ms")
fi

# LCP regression vs iter-1 baseline (only applies when BASELINE_LCP > 0)
if [[ "$BASELINE_LCP" -gt 0 && "$LCP_MS" != "N/A" ]]; then
  python3 -c "
import sys
lcp=float('$LCP_MS')
baseline=float('$BASELINE_LCP')
regression_pct = ((lcp - baseline) / baseline) * 100
if regression_pct > $LCP_REGRESSION_PCT:
    print(f'BLOCK: LCP regression {regression_pct:.1f}% > ${LCP_REGRESSION_PCT}% (${LCP_MS}ms vs baseline ${BASELINE_LCP}ms)')
    sys.exit(1)
" || BLOCK_REASONS+=("LCP regression ${LCP_MS}ms vs baseline ${BASELINE_LCP}ms > ${LCP_REGRESSION_PCT}%")
fi

# CLS gate
if [[ "$CLS" != "N/A" ]]; then
  python3 -c "
import sys
cls=float('$CLS')
if cls >= $CLS_BLOCK:
    print(f'BLOCK: CLS {cls} >= ${CLS_BLOCK}')
    sys.exit(1)
" || BLOCK_REASONS+=("CLS ${CLS} >= ${CLS_BLOCK}")
fi

# TBT gate
if [[ "$TBT_MS" != "N/A" ]]; then
  python3 -c "
import sys
tbt=float('$TBT_MS')
if tbt >= $TBT_BLOCK_MS:
    print(f'BLOCK: TBT {tbt}ms >= ${TBT_BLOCK_MS}ms')
    sys.exit(1)
" || BLOCK_REASONS+=("TBT ${TBT_MS}ms >= ${TBT_BLOCK_MS}ms")
fi

# axe critical/serious gate (only when measured)
if [[ "$AXE_STATUS" == "measured" && "$AXE_CRITICAL" != "N/A" ]]; then
  if [[ "$AXE_CRITICAL" -gt 0 ]]; then
    BLOCK_REASONS+=("axe: ${AXE_CRITICAL} critical violation(s)")
  fi
  if [[ "$AXE_SERIOUS" -gt 0 ]]; then
    BLOCK_REASONS+=("axe: ${AXE_SERIOUS} serious violation(s)")
  fi
fi

# ---------------------------------------------------------------------------
# 6. Append INSTRUMENT RESULTS block to the artifact
# ---------------------------------------------------------------------------
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BLOCK_STATUS="PASS"
if [[ ${#BLOCK_REASONS[@]} -gt 0 ]]; then
  BLOCK_STATUS="BLOCK"
fi

INSTRUMENT_BLOCK="
\`\`\`
INSTRUMENT RESULTS — iteration ${ITER} — ${TIMESTAMP}
Method: Lighthouse desktop, no-throttle, localhost:${HTTP_PORT}

LCP_ms:         ${LCP_MS}
CLS:            ${CLS}
TBT_ms:         ${TBT_MS}
LH_perf_score:  ${LH_PERF}
LH_a11y_score:  ${LH_A11Y}

axe_status:     ${AXE_STATUS}
axe_critical:   ${AXE_CRITICAL}
axe_serious:    ${AXE_SERIOUS}
axe_moderate:   ${AXE_MODERATE}

baseline_LCP_ms: ${BASELINE_LCP}

BLOCK_class_verdict: ${BLOCK_STATUS}
$(if [[ ${#BLOCK_REASONS[@]} -gt 0 ]]; then printf 'BLOCK_reasons:\n'; for r in "${BLOCK_REASONS[@]}"; do printf '  - %s\n' "$r"; done; fi)
\`\`\`
"

echo "$INSTRUMENT_BLOCK" >> "$ARTIFACT"
echo "[T8] Appended INSTRUMENT RESULTS to $ARTIFACT"

# ---------------------------------------------------------------------------
# 7. Exit with BLOCK status
# ---------------------------------------------------------------------------
if [[ ${#BLOCK_REASONS[@]} -gt 0 ]]; then
  echo "[T8] BLOCK: ${BLOCK_REASONS[*]}"
  exit 1
else
  echo "[T8] PASS: all BLOCK-class budgets met"
  exit 0
fi

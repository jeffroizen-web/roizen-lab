#!/usr/bin/env bash
# Cron/launchd wrapper for the weekly letter-writers refresh + auto-redeploy.
#
# Runs the refresh (scrape → re-wire the canonical), then calls the GATED
# auto-redeploy so the re-wired canonical auto-serves on the live site. The
# deploy self-gates: it is DISARMED unless ROIZEN_AUTO_DEPLOY=1, and it
# change-detects (a refresh that alters no canonical bytes ships nothing).
#
# ARMING (Jeff/Kleiber-gated — reported at gate before this goes live in cron):
#   1. Point the plist ProgramArguments at THIS script instead of the bare
#      letter_writers_refresh.py:
#        <string>/bin/bash</string>
#        <string>/Users/roizenj/Code/Claude Apps/Roizen Lab/scripts/letter_writers_refresh_cron.sh</string>
#   2. Add ROIZEN_AUTO_DEPLOY=1 to the plist EnvironmentVariables.
# Until BOTH are done, the live cron still runs the bare refresh (no deploy) and
# this wrapper is a no-op deploy even if invoked (kill-switch OFF).
#
# On demand: bash scripts/letter_writers_refresh_cron.sh

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# 1. Refresh (scrape + re-wire the canonical field-of-interest spans).
python3 scripts/letter_writers_refresh.py
REFRESH_EXIT=$?

# 2. Gated auto-redeploy (self-gates on kill-switch + change-detect + test gate).
#    A refresh failure still lets deploy run its OWN change-detect: if the
#    canonical bytes are unchanged, deploy is a logged no-op; if a partial
#    re-wire changed bytes, the deploy GATE (hash-match test) is the backstop.
bash scripts/deploy_publish.sh
DEPLOY_EXIT=$?

# The wrapper's exit reflects whether the JOB RAN (R2). A nonzero refresh is a
# genuine execution failure; a nonzero deploy is a gate/push failure worth
# surfacing. Prefer the refresh code, fall back to deploy.
if [ "$REFRESH_EXIT" -ne 0 ]; then
    exit "$REFRESH_EXIT"
fi
exit "$DEPLOY_EXIT"

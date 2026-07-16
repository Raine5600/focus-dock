#!/bin/bash
# Run outreach in background — survives terminal close.
# Usage: ./run-outreach.sh [--all] [--future] [--limit N]

set -euo pipefail
cd "$(dirname "$0")"

PIDFILE="outreach-send.pid"
LOG="outreach-send.log"

if [[ -f "$PIDFILE" ]]; then
  OLD_PID=$(cat "$PIDFILE")
  if kill -0 "$OLD_PID" 2>/dev/null; then
    echo "Campaign already running (PID $OLD_PID). Check $LOG"
    exit 0
  fi
fi

ARGS=(--send --force)
if [[ "${1:-}" == "--all" ]]; then
  ARGS=(--all "${ARGS[@]}")
elif [[ "${1:-}" == "--future" ]]; then
  ARGS=(--source future "${ARGS[@]}")
fi
if [[ "${1:-}" == "--limit" && -n "${2:-}" ]]; then
  ARGS=(--limit "$2" "${ARGS[@]}")
elif [[ "${2:-}" == "--limit" && -n "${3:-}" ]]; then
  ARGS=(--limit "$3" "${ARGS[@]}")
fi

nohup python3 -u email-campaign.py "${ARGS[@]}" >> "$LOG" 2>&1 &
echo $! > "$PIDFILE"
echo "Started outreach PID $(cat "$PIDFILE"). Tail: tail -f $LOG"
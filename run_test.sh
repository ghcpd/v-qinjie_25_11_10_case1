#!/usr/bin/env bash
set -euo pipefail
MODE=${1:-repaired}

rm -f exploit_marker.txt

if [ "$MODE" = "original" ]; then
  echo "Running original vulnerable program (expected to fail security checks)..."
  python input_original.py || true
  if [ -f exploit_marker.txt ]; then
    echo "EXPLOIT DETECTED: original program executed arbitrary user script."
    exit 1
  else
    echo "Original program did NOT execute the exploit (unexpected)."
    exit 0
  fi
elif [ "$MODE" = "repaired" ]; then
  echo "Running repaired secure program (expected to succeed)..."
  export DB_PASSWORD="REPAIRED_PASSWORD"
  python input.py
  if [ -f exploit_marker.txt ]; then
    echo "EXPLOIT DETECTED: repaired program still allowed arbitrary user script."
    exit 1
  else
    echo "Repaired program did not run the exploit. Success."
    exit 0
  fi
else
  echo "Unknown mode: $MODE"; exit 2
fi

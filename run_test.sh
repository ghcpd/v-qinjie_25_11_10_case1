#!/usr/bin/env bash
set -euo pipefail
mkdir -p logs
LOGFILE=logs/test_run.log
echo "Security scan started" > "$LOGFILE"

scan_file() {
	local file="$1"
	# Look for exec( usage or hardcoded DB_PASSWORD assignment
	grep -nE "exec\(|DB_PASSWORD\s*=" "$file" || true
}

echo "Scanning original_input.py for insecure patterns (should be vulnerable)" >> "$LOGFILE"
ORIG_FINDINGS=$(scan_file original_input.py)
if [ -n "$ORIG_FINDINGS" ]; then
	echo "Original findings:" >> "$LOGFILE"
	echo "$ORIG_FINDINGS" >> "$LOGFILE"
	ORIG_STATUS=VULNERABLE
else
	echo "No insecure patterns found in original_input.py (unexpected)" >> "$LOGFILE"
	ORIG_STATUS=CLEAN
fi

echo "Scanning input.py for insecure patterns (should be clean)" >> "$LOGFILE"
PATCH_FINDINGS=$(scan_file input.py)
if [ -n "$PATCH_FINDINGS" ]; then
	echo "Patched findings:" >> "$LOGFILE"
	echo "$PATCH_FINDINGS" >> "$LOGFILE"
	PATCH_STATUS=VULNERABLE
else
	echo "No insecure patterns found in input.py" >> "$LOGFILE"
	PATCH_STATUS=CLEAN
fi

echo "Original status: $ORIG_STATUS" >> "$LOGFILE"
echo "Patched status: $PATCH_STATUS" >> "$LOGFILE"

if [ "$ORIG_STATUS" = "VULNERABLE" ] && [ "$PATCH_STATUS" = "CLEAN" ]; then
	echo "Test result: PASS (original vulnerable, patched clean)" >> "$LOGFILE"
	exit 0
else
	echo "Test result: FAIL" >> "$LOGFILE"
	exit 1
fi


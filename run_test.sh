#!/usr/bin/env bash
set -euo pipefail

mkdir -p logs

echo "Running security check on vulnerable version (should fail)"
python -u security_check.py input_vulnerable.py -o report_vulnerable.json
ret=$?
if [ $ret -eq 0 ]; then
  echo "ERROR: Vulnerable file did not fail the security check"
  exit 1
else
  echo "Detected vulnerabilities as expected for vulnerable file. (exit $ret)"
fi

echo "Running security check on fixed version (should succeed)"
python -u security_check.py input.py -o report_fixed.json
if [ $? -ne 0 ]; then
  echo "ERROR: Fixed file was detected as vulnerable"
  exit 1
fi

echo "All checks passed"

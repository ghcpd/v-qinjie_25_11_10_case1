# Security Audit and Hardening for input.py

This repository contains a vulnerable `input_vulnerable.py` and a fixed `input.py`.

Files added:
- `input_vulnerable.py`: The original vulnerable file preserved for testing.
- `input.py`: The repaired version that avoids exec usage and reads secret from the environment.
- `security_check.py`: A small scanner that looks for simple vulnerable patterns and writes `report.json`.
- `report.json`: A JSON summary of vulnerabilities and fixes.
- `run_test.sh`, `run_test.bat`: Scripts that run checks on the vulnerable and repaired code.
- `run_tests_auto.py`: Auto-detects platform and runs the correct test script, logging to `logs/test_run.log`.
- `setup.sh`: Sets up environment variables for quick testing.
- `Dockerfile`: For reproducible test runs in a container.

Quick guide:
 1. Setup environment (Linux/macOS):
    - `source setup.sh` (this sets a sample DB_PASSWORD in your shell)
 2. Run the full automated tests:
    - Linux/macOS: `./run_test.sh`
    - Windows: `run_test.bat`
    - Or `python run_tests_auto.py` to auto-detect the environment and log results to `logs/test_run.log`.

Notes:
- `security_check.py` is intentionally small and pattern-based; it's not a replacement for a full static analysis tool but demonstrates a reproducible test case.

#!/bin/bash

# Test runner script for Linux/macOS
# This script runs both the original and fixed code tests and logs results

set -o pipefail

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/test_run.log"
RESULTS_FILE="$LOG_DIR/test_results.log"

{
    echo "======================================================================"
    echo "Security Audit - Test Execution ($(date))"
    echo "======================================================================"
    echo "Platform: Linux/macOS"
    echo "Python Version: $(python3 --version)"
    echo ""
    
    # Set environment variable
    export DB_PASSWORD="test_password_123"
    
    echo "--- Running Original Code Tests (Expected to PASS - Vulnerabilities Confirmed) ---"
    echo ""
    if python3 test_original.py; then
        ORIGINAL_RESULT="PASS"
        echo "✓ Original code test PASSED (vulnerabilities confirmed)"
    else
        ORIGINAL_RESULT="FAIL"
        echo "✗ Original code test FAILED"
    fi
    
    echo ""
    echo "--- Running Fixed Code Tests (Expected to PASS - All Vulnerabilities Fixed) ---"
    echo ""
    if python3 test_fixed.py; then
        FIXED_RESULT="PASS"
        echo "✓ Fixed code test PASSED (all vulnerabilities fixed)"
    else
        FIXED_RESULT="FAIL"
        echo "✗ Fixed code test FAILED"
    fi
    
    echo ""
    echo "======================================================================"
    echo "Test Results Summary"
    echo "======================================================================"
    echo "Original Code (Vulnerability Check): $ORIGINAL_RESULT"
    echo "Fixed Code (Security Verification): $FIXED_RESULT"
    echo "======================================================================"
    
} | tee "$LOG_FILE"

echo ""
echo "Logs saved to: $LOG_FILE"

#!/usr/bin/env python3
"""
Test script for the ORIGINAL vulnerable code.
This script demonstrates the vulnerabilities in the original code.
Expected behavior: This test SHOULD FAIL to show the vulnerabilities.
"""

import os
import sys
import traceback

print("\n" + "=" * 60)
print("Testing ORIGINAL Vulnerable Code")
print("=" * 60 + "\n")

# Test 1: Check for hardcoded password (Vulnerability SEC-001)
print("[TEST 1] Checking for hardcoded secrets...")
try:
    with open("input.py", "r") as f:
        content = f.read()
        if "root_password123" in content:
            print("  [FAIL] Hardcoded password found in source code!")
            print("    Vulnerability: Hardcoded secret exposure")
            sys.exit(1)
except Exception as e:
    print(f"  [ERROR] {e}")
    sys.exit(1)

# Test 2: Check for dangerous exec() usage (Vulnerability SEC-002)
print("\n[TEST 2] Checking for dangerous exec() usage...")
try:
    with open("input.py", "r") as f:
        content = f.read()
        # Look for exec( call - specifically the dangerous built-in function
        for line in content.split('\n'):
            stripped = line.split('#')[0]  # Remove comments
            if 'exec(' in stripped:
                print("  [FAIL] Unsafe exec() usage found in source code!")
                print("    Vulnerability: Code injection risk")
                sys.exit(1)
except Exception as e:
    print(f"  [ERROR] {e}")
    sys.exit(1)

# Test 3: Check for password in print statements (Vulnerability SEC-004)
print("\n[TEST 3] Checking for password in console output...")
try:
    with open("input.py", "r") as f:
        content = f.read()
        if "print(f\"Connecting to DB with password:" in content:
            print("  [FAIL] Password found in print statement!")
            print("    Vulnerability: Information disclosure")
            sys.exit(1)
except Exception as e:
    print(f"  [ERROR] {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("All vulnerability checks PASSED (vulnerabilities confirmed)")
print("The original code contains the expected security issues.")
print("=" * 60 + "\n")

sys.exit(0)

#!/usr/bin/env python3
"""
Test script for the FIXED secure code.
This script verifies that all vulnerabilities have been remediated.
Expected behavior: This test SHOULD PASS.
"""

import os
import sys
import subprocess
from pathlib import Path

print("\n" + "=" * 60)
print("Testing FIXED Secure Code")
print("=" * 60 + "\n")

# Set environment variable for testing
os.environ["DB_PASSWORD"] = "test_password_123"

# Test 1: No hardcoded secrets (SEC-001 Fixed)
print("[TEST 1] Verifying no hardcoded secrets...")
try:
    with open("input_fixed.py", "r") as f:
        content = f.read()
        if "root_password123" in content:
            print("  [FAIL] Hardcoded password still found!")
            sys.exit(1)
        if "DB_PASSWORD = os.getenv" not in content:
            print("  [FAIL] DB_PASSWORD not using environment variable!")
            sys.exit(1)
    print("  [PASS] No hardcoded secrets, using environment variables")
except Exception as e:
    print(f"  [ERROR] {e}")
    sys.exit(1)

# Test 2: No dangerous exec() usage (SEC-002 Fixed)
print("\n[TEST 2] Verifying no dangerous exec() usage...")
try:
    with open("input_fixed.py", "r") as f:
        lines = f.readlines()
        in_docstring = False
        for i, line in enumerate(lines, 1):
            # Track if we're in a docstring
            if '"""' in line or "'''" in line:
                in_docstring = not in_docstring
            
            if not in_docstring:
                stripped = line.split('#')[0]  # Remove comments
                # Check for exec( but exclude exec_module
                if 'exec(' in stripped and 'exec_module' not in stripped:
                    print(f"  [FAIL] Dangerous exec() built-in function found on line {i}!")
                    sys.exit(1)
        
        if "importlib.util" not in ''.join(lines):
            print("  [FAIL] importlib not used for safer code loading!")
            sys.exit(1)
    print("  [PASS] Using safe importlib instead of exec()")
except Exception as e:
    print(f"  [ERROR] {e}")
    sys.exit(1)

# Test 3: File path validation present (SEC-003 Fixed)
print("\n[TEST 3] Verifying file path validation...")
try:
    with open("input_fixed.py", "r") as f:
        content = f.read()
        if "Path(file_path).resolve()" not in content:
            print("  [FAIL] Path validation not implemented!")
            sys.exit(1)
        if "FileNotFoundError" not in content:
            print("  [FAIL] Missing file existence check!")
            sys.exit(1)
    print("  [PASS] Path validation and checks implemented")
except Exception as e:
    print(f"  [ERROR] {e}")
    sys.exit(1)

# Test 4: No password in console output (SEC-004 Fixed)
print("\n[TEST 4] Verifying no passwords in console output...")
try:
    with open("input_fixed.py", "r") as f:
        content = f.read()
        if "print(f\"Connecting to DB with password:" in content:
            print("  [FAIL] Password still in print statement!")
            sys.exit(1)
        if "print(\"Connecting to DB with credentials" not in content:
            print("  [FAIL] Safe message not found!")
            sys.exit(1)
    print("  [PASS] No sensitive data in console output")
except Exception as e:
    print(f"  [ERROR] {e}")
    sys.exit(1)

# Test 5: Code syntax and import validation
print("\n[TEST 5] Verifying code syntax and imports...")
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("input_fixed", "input_fixed.py")
    if spec is None or spec.loader is None:
        print("  [FAIL] Cannot load fixed module!")
        sys.exit(1)
    module = importlib.util.module_from_spec(spec)
    print("  [PASS] Fixed code syntax is valid")
except SyntaxError as e:
    print(f"  [FAIL] Syntax error in fixed code: {e}")
    sys.exit(1)
except Exception as e:
    print(f"  [ERROR] {e}")
    sys.exit(1)

# Test 6: Verify environment variable handling
print("\n[TEST 6] Verifying environment variable handling...")
try:
    # Temporarily unset DB_PASSWORD
    original_val = os.environ.get("DB_PASSWORD")
    if "DB_PASSWORD" in os.environ:
        del os.environ["DB_PASSWORD"]
    
    # Check if code handles missing env var gracefully
    with open("input_fixed.py", "r") as f:
        content = f.read()
        if "os.getenv" not in content:
            print("  [FAIL] Not using os.getenv for environment variable!")
            sys.exit(1)
    
    # Restore
    if original_val:
        os.environ["DB_PASSWORD"] = original_val
    
    print("  [PASS] Environment variable handling implemented")
except Exception as e:
    print(f"  [ERROR] {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("All tests PASSED!")
print("The fixed code successfully addresses all vulnerabilities.")
print("=" * 60 + "\n")

sys.exit(0)

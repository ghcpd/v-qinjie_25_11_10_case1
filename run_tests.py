#!/usr/bin/env python3
"""
Automatic test execution script that detects environment and runs appropriate tests.
Supports Windows, Linux, macOS, and Docker environments.
"""

import os
import sys
import platform
import subprocess
import json
from pathlib import Path
from datetime import datetime

class EnvironmentDetector:
    """Detect the current runtime environment."""
    
    @staticmethod
    def is_docker():
        """Check if running inside Docker container."""
        return os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv")
    
    @staticmethod
    def get_platform():
        """Get the current platform."""
        return platform.system()
    
    @classmethod
    def detect(cls):
        """Detect and return the current environment."""
        if cls.is_docker():
            return "docker"
        
        system = cls.get_platform()
        if system == "Windows":
            return "windows"
        elif system == "Darwin":
            return "macos"
        elif system == "Linux":
            return "linux"
        else:
            return "unknown"

class TestRunner:
    """Execute tests for the security audit."""
    
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "test_run.log"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment": EnvironmentDetector.detect(),
            "platform": EnvironmentDetector.get_platform(),
            "tests": []
        }
    
    def log(self, message, level="INFO"):
        """Log a message to both console and file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)
        with open(self.log_file, "a") as f:
            f.write(log_message + "\n")
    
    def run_command(self, cmd, name, shell=False):
        """Run a command and log results."""
        self.log(f"Running: {name}")
        self.log(f"Command: {cmd}")
        
        try:
            result = subprocess.run(
                cmd,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            stdout = result.stdout
            stderr = result.stderr
            return_code = result.returncode
            
            self.log(f"Return code: {return_code}")
            if stdout:
                self.log(f"STDOUT:\n{stdout}")
            if stderr:
                self.log(f"STDERR:\n{stderr}")
            
            test_result = {
                "name": name,
                "success": return_code == 0,
                "return_code": return_code,
                "stdout": stdout,
                "stderr": stderr
            }
            self.results["tests"].append(test_result)
            
            return return_code == 0
            
        except subprocess.TimeoutExpired:
            self.log(f"Test '{name}' timed out", "ERROR")
            test_result = {
                "name": name,
                "success": False,
                "error": "Timeout"
            }
            self.results["tests"].append(test_result)
            return False
        except Exception as e:
            self.log(f"Error running test '{name}': {str(e)}", "ERROR")
            test_result = {
                "name": name,
                "success": False,
                "error": str(e)
            }
            self.results["tests"].append(test_result)
            return False
    
    def run_tests(self, environment):
        """Run tests based on the detected environment."""
        self.log(f"Detected Environment: {environment}")
        self.log("=" * 60)
        
        # Set environment variable for tests
        os.environ["DB_PASSWORD"] = "test_password_123"
        
        if environment == "windows":
            self.run_windows_tests()
        elif environment in ["linux", "macos"]:
            self.run_unix_tests()
        elif environment == "docker":
            self.run_docker_tests()
        else:
            self.log("Unknown environment, attempting Unix-style tests", "WARNING")
            self.run_unix_tests()
        
        self.save_results()
    
    def run_windows_tests(self):
        """Run tests on Windows."""
        self.log("Running Windows tests...")
        
        # Test original code (should fail with error)
        self.log("\n--- Testing Original Code (Expected to Fail) ---")
        self.run_command(
            ["python", "test_original.py"],
            "Test Original Code",
            shell=False
        )
        
        # Test fixed code (should pass)
        self.log("\n--- Testing Fixed Code (Expected to Pass) ---")
        self.run_command(
            ["python", "test_fixed.py"],
            "Test Fixed Code",
            shell=False
        )
    
    def run_unix_tests(self):
        """Run tests on Linux/macOS."""
        self.log("Running Unix-style tests...")
        
        # Test original code (should fail with error)
        self.log("\n--- Testing Original Code (Expected to Fail) ---")
        self.run_command(
            "python3 test_original.py",
            "Test Original Code",
            shell=True
        )
        
        # Test fixed code (should pass)
        self.log("\n--- Testing Fixed Code (Expected to Pass) ---")
        self.run_command(
            "python3 test_fixed.py",
            "Test Fixed Code",
            shell=True
        )
    
    def run_docker_tests(self):
        """Run tests inside Docker container."""
        self.log("Running Docker container tests...")
        
        # Test original code (should fail with error)
        self.log("\n--- Testing Original Code (Expected to Fail) ---")
        self.run_command(
            ["python", "test_original.py"],
            "Test Original Code in Docker",
            shell=False
        )
        
        # Test fixed code (should pass)
        self.log("\n--- Testing Fixed Code (Expected to Pass) ---")
        self.run_command(
            ["python", "test_fixed.py"],
            "Test Fixed Code in Docker",
            shell=False
        )
    
    def save_results(self):
        """Save test results to JSON file."""
        results_file = self.log_dir / "test_results.json"
        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2)
        self.log(f"\nTest results saved to: {results_file}")
        self.log("=" * 60)
        
        # Print summary
        total_tests = len(self.results["tests"])
        passed_tests = sum(1 for t in self.results["tests"] if t["success"])
        self.log(f"\nTest Summary:")
        self.log(f"  Total Tests: {total_tests}")
        self.log(f"  Passed: {passed_tests}")
        self.log(f"  Failed: {total_tests - passed_tests}")

def main():
    """Main entry point."""
    print("\n" + "=" * 60)
    print("Security Audit - Automatic Test Execution")
    print("=" * 60 + "\n")
    
    runner = TestRunner()
    environment = EnvironmentDetector.detect()
    runner.run_tests(environment)
    
    print("\n" + "=" * 60)
    print(f"Full logs saved to: {runner.log_file}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

import os
import subprocess
import sys


def run_cmd(cmd, env=None):
    proc = subprocess.run(cmd, shell=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.decode("utf-8", errors="replace")


def setup_module():
    # clean marker files
    try:
        os.remove("exploit_marker.txt")
    except FileNotFoundError:
        pass


def test_original_executes_malicious_script():
    # The original vulnerable program is located at input_original.py and will execute the user script
    rc, out = run_cmd("python input_original.py")
    assert os.path.exists("exploit_marker.txt"), "Original did not execute malicious script as expected"


def test_repaired_does_not_execute_malicious_script():
    # The repaired program should not execute the top-level user_script.py
    env = os.environ.copy()
    env["DB_PASSWORD"] = "test_pass"
    # Ensure previous markers are removed
    try:
        os.remove("exploit_marker.txt")
    except FileNotFoundError:
        pass
    rc, out = run_cmd("python input.py", env=env)
    assert not os.path.exists("exploit_marker.txt"), "Repaired program allowed arbitrary code execution"


def test_repaired_hides_db_password():
    # Verify that the repaired script doesn't echo DB_PASSWORD
    env = os.environ.copy()
    env["DB_PASSWORD"] = "secret_pw_123"
    rc, out = run_cmd("python input.py", env=env)
    assert "secret_pw_123" not in out

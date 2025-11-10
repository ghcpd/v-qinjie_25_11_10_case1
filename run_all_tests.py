import os
import platform
import subprocess
import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "test_run.log")

def run(cmd, env=None):
    start = datetime.datetime.utcnow().isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as fh:
        fh.write(f"=== START {cmd} at {start}\n")
        proc = subprocess.run(cmd, shell=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        fh.write(proc.stdout.decode("utf-8", errors="replace"))
        fh.write(f"=== END {cmd} exit={proc.returncode}\n\n")
    return proc.returncode

def detect_and_run():
    system = platform.system().lower()
    if os.path.exists("/.dockerenv"):
        system = "docker"

    if system == "windows":
        # Run Windows batch file via cmd to avoid PowerShell semantics
        return_code = run("cmd /c run_test.bat repaired")
    else:
        # Default to POSIX shell
        run("chmod +x run_test.sh || true")
        return_code = run("./run_test.sh repaired")

    if return_code == 0:
        print("Repaired test passed. See logs/test_run.log for details.")
    else:
        print("Repaired test failed. See logs/test_run.log for details.")
    return return_code

if __name__ == "__main__":
    rc = detect_and_run()
    raise SystemExit(rc)

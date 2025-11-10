import os
import platform
import subprocess
from pathlib import Path

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logfile = log_dir / "test_run.log"


def run(cmd, shell=False):
    with open(logfile, "a") as f:
        f.write(f"Running: {cmd}\n")
        try:
            subprocess.check_call(cmd, shell=shell)
            f.write("Success\n")
        except subprocess.CalledProcessError as e:
            f.write(f"Failed: {e}\n")


def in_docker():
    # Detect common Docker indicators
    if Path("/.dockerenv").exists():
        return True
    try:
        with open("/proc/1/cgroup", "r") as f:
            txt = f.read()
            if "docker" in txt or "kubepods" in txt:
                return True
    except Exception:
        pass
    return False


def main():
    # Clear logfile
    open(logfile, "w").close()
    run(["python", "-V"]) 
    p = platform.system()
    if in_docker():
        run(["bash", "run_test.sh"]) 
    elif p == "Windows":
        run(["cmd", "/c", "run_test.bat"]) 
    else:
        run(["bash", "run_test.sh"]) 


if __name__ == "__main__":
    main()

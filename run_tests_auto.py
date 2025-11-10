import os
import platform
import subprocess
from pathlib import Path


def is_docker():
    if Path("/.dockerenv").exists():
        return True
    try:
        with open('/proc/1/cgroup', 'rt') as fh:
            return 'docker' in fh.read() or 'kubepods' in fh.read()
    except Exception:
        return False


def main():
    logs = Path('logs')
    logs.mkdir(exist_ok=True)
    log_file = logs / 'test_run.log'
    system = platform.system()
    cmd = None
    if is_docker() or system in ('Linux', 'Darwin'):
        cmd = ['bash', 'run_test.sh']
    elif system == 'Windows':
        cmd = ['cmd', '/c', 'run_test.bat']
    else:
        print(f'Unknown platform: {system}. Defaulting to run_test.sh')
        cmd = ['bash', 'run_test.sh']

    print(f'Executing: {cmd} (logging to {log_file})')
    with open(log_file, 'w', encoding='utf-8') as fh:
        proc = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.STDOUT)
        proc.communicate()
        return proc.returncode


if __name__ == '__main__':
    raise SystemExit(main())

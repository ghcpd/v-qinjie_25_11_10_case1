"""Simple security scanner for Python source files.

It looks for risky patterns (exec, hardcoded DB_PASSWORD) and reports findings as JSON.
Exit code 0 -> no findings, exit code 1 -> findings detected.
"""
import argparse
import json
import re
from pathlib import Path


VULN_PATTERNS = [
    {
        "id": "V001",
        "name": "Hardcoded DB password",
        "pattern": re.compile(r'^\s*DB_PASSWORD\s*=\s*["\'].*["\']', re.MULTILINE),
        "severity": "HIGH",
        "description": "Detects hardcoded database password variables in source code",
    },
    {
        "id": "V002",
        "name": "exec usage",
        "pattern": re.compile(r'\bexec\s*\('),
        "severity": "CRITICAL",
        "description": "Detects exec() calls which can execute arbitrary code",
    },
    {
        "id": "V003",
        "name": "Cleartext password logging",
        "pattern": re.compile(r"Connecting to DB with password"),
        "severity": "MEDIUM",
        "description": "Logs DB password to console",
    },
]


def scan_file(path: Path):
    findings = []
    text = path.read_text(encoding='utf-8')
    for patt in VULN_PATTERNS:
        for m in patt["pattern"].finditer(text):
            # Determine line number
            lineno = text.count('\n', 0, m.start()) + 1
            findings.append({
                "vuln_id": patt["id"],
                "name": patt["name"],
                "severity": patt["severity"],
                "description": patt["description"],
                "file": str(path),
                "line": lineno,
                "snippet": text.splitlines()[lineno-1].strip(),
            })
    return findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Python file to scan")
    parser.add_argument("-o", "--output", type=str, default="report.json", help="Output file for JSON report")
    args = parser.parse_args()

    p = Path(args.path)
    if not p.exists():
        print(f"File not found: {p}")
        return 2

    findings = scan_file(p)
    report = {"file": str(p), "findings": findings}
    Path(args.output).write_text(json.dumps(report, indent=2), encoding='utf-8')

    if findings:
        print(f"Found {len(findings)} issues. See {args.output}")
        return 1
    else:
        print("No issues found.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

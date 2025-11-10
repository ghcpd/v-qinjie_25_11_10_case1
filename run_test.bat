@echo off
if not exist logs mkdir logs

echo Running security check on vulnerable version (should fail)
python -u security_check.py input_vulnerable.py -o report_vulnerable.json
if %ERRORLEVEL% EQU 0 (
    echo ERROR: Vulnerable file did not fail the security check
    exit /b 1
) else (
    echo Detected vulnerabilities as expected for vulnerable file. (exit %ERRORLEVEL%)
)

echo Running security check on fixed version (should succeed)
python -u security_check.py input.py -o report_fixed.json
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Fixed file was detected as vulnerable
    exit /b 2
)

echo All checks passed

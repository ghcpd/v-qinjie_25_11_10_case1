@echo off
if not exist logs mkdir logs
set LOGFILE=logs\test_run.log
echo Security scan started > %LOGFILE%

rem Search for exec( or DB_PASSWORD assignment in files
findstr /n /R "exec( DB_PASSWORD\s*=\"" original_input.py input.py > nul 2>&1 || rem ignore

echo Scanning original_input.py for insecure patterns (should be vulnerable) >> %LOGFILE%
findstr /n /R "exec(\|DB_PASSWORD\s*=" original_input.py >> %LOGFILE% || echo No findings >> %LOGFILE%

echo Scanning input.py for insecure patterns (should be clean) >> %LOGFILE%
findstr /n /R "exec(\|DB_PASSWORD\s*=" input.py >> %LOGFILE% || echo No findings >> %LOGFILE%

echo Logs written to %LOGFILE%

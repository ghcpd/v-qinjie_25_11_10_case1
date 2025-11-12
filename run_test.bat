@echo off
setlocal
set MODE=%1
if "%MODE%"=="" set MODE=repaired

del /f /q exploit_marker.txt >NUL 2>NUL

if /i "%MODE%"=="original" (
  echo Running original vulnerable program (expected to fail security checks)...
  python input_original.py || REM ignore
  if exist exploit_marker.txt (
    echo EXPLOIT DETECTED: original program executed arbitrary user script.
    exit /b 1
  ) else (
    echo Original program did NOT execute the exploit (unexpected).
    exit /b 0
  )
) else (
  if /i "%MODE%"=="repaired" (
    echo Running repaired secure program (expected to succeed)...
    set "DB_PASSWORD=REPAIRED_PASSWORD"
    python input.py
    if exist exploit_marker.txt (
      echo EXPLOIT DETECTED: repaired program still allowed arbitrary user script.
      exit /b 1
    ) else (
      echo Repaired program did not run the exploit. Success.
      exit /b 0
    )
  ) else (
    echo Unknown mode: %MODE%
    exit /b 2
  )
)

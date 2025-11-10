@echo off
REM Test runner script for Windows
REM This script runs both the original and fixed code tests and logs results

setlocal enabledelayedexpansion

set LOG_DIR=logs
set LOG_FILE=%LOG_DIR%\test_run.log
set RESULTS_FILE=%LOG_DIR%\test_results.log

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Redirect output to both console and log file
(
    echo ======================================================================
    echo Security Audit - Test Execution - %date% %time%
    echo ======================================================================
    echo Platform: Windows
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
    echo Python Version: %PYVER%
    echo.
    
    REM Set environment variable
    set DB_PASSWORD=test_password_123
    
    echo --- Running Original Code Tests ^(Expected to PASS - Vulnerabilities Confirmed^) ---
    echo.
    python test_original.py
    if %ERRORLEVEL% equ 0 (
        set ORIGINAL_RESULT=PASS
        echo.
        echo [OK] Original code test PASSED - Vulnerabilities confirmed
    ) else (
        set ORIGINAL_RESULT=FAIL
        echo.
        echo [FAILED] Original code test FAILED
    )
    
    echo.
    echo --- Running Fixed Code Tests ^(Expected to PASS - All Vulnerabilities Fixed^) ---
    echo.
    python test_fixed.py
    if %ERRORLEVEL% equ 0 (
        set FIXED_RESULT=PASS
        echo.
        echo [OK] Fixed code test PASSED - All vulnerabilities fixed
    ) else (
        set FIXED_RESULT=FAIL
        echo.
        echo [FAILED] Fixed code test FAILED
    )
    
    echo.
    echo ======================================================================
    echo Test Results Summary
    echo ======================================================================
    echo Original Code ^(Vulnerability Check^): !ORIGINAL_RESULT!
    echo Fixed Code ^(Security Verification^): !FIXED_RESULT!
    echo ======================================================================
    
) > "%LOG_FILE%" 2>&1

type "%LOG_FILE%"
echo.
echo Logs saved to: %LOG_FILE%

endlocal

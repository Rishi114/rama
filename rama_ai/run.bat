@echo off
REM RAMA AI - Launch with auto Python detection

set PYTHON_CMD=

REM Try different Python commands
where python >nul 2>&1
if %errorlevel% equ 0 set PYTHON_CMD=python

if not defined PYTHON_CMD (
    where python3 >nul 2>&1
    if %errorlevel% equ 0 set PYTHON_CMD=python3
)

if not defined PYTHON_CMD (
    where py >nul 2>&1
    if %errorlevel% equ 0 set PYTHON_CMD=py
)

if not defined PYTHON_CMD (
    echo.
    echo ❌ Python not found!
    echo.
    echo Please install Python:
    echo   https://www.python.org/downloads/
    echo.
    echo Or run setup.bat for help
    echo.
    pause
    exit /b
)

echo ✅ Using: %PYTHON_CMD%
echo.

REM Run RAMA
%PYTHON_CMD% main.py
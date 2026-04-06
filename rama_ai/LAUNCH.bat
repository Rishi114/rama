@echo off
REM RAMA AI - Simple Launcher
REM Just double-click this to run!

echo.
echo 🤖 Starting RAMA AI...
echo.

REM Try py launcher first (Windows built-in)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Found Python via py launcher
    py main.py
    goto :end
)

REM Try python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Found Python
    python main.py
    goto :end
)

REM Try python3
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Found Python3
    python3 main.py
    goto :end
)

echo.
echo ❌ Python not found!
echo.
echo Please install Python from:
echo https://www.python.org/downloads/
echo.
echo Make sure to check "Add Python to PATH"
echo.
pause

:end
pause
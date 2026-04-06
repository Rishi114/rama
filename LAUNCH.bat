@echo off
REM RAMA AI - Launcher
cd /d "%~dp0"

echo.
echo 🤖 Starting RAMA AI v2.0...
echo.

REM Try py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Starting...
    py main.py
    goto :end
)

REM Try python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Starting...
    python main.py
    goto :end
)

echo.
echo ❌ Python not installed!
echo Download: https://www.python.org/downloads/
echo.
pause

:end
pause
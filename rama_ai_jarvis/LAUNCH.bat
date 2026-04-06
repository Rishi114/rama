@echo off
REM RAMA AI - Jarvis-Style Voice Assistant Launcher
cd /d "%~dp0"

echo.
echo 🤖 Starting RAMA - Jarvis Style...
echo.

REM Try py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Starting with voice...
    py main.py
    goto :end
)

REM Try python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Starting with voice...
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
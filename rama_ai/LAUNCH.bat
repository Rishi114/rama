@echo off
REM RAMA AI - Voice Launcher (Double-click for voice mode!)
cd /d "%~dp0"

echo.
echo 🤖 Starting RAMA AI with Voice...
echo.

REM Try py launcher first (Windows built-in)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Using py launcher with voice
    py main.py --voice
    goto :end
)

REM Try python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Using python with voice
    python main.py --voice
    goto :end
)

REM Try python3
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Using python3 with voice
    python3 main.py --voice
    goto :end
)

echo.
echo ❌ Python not installed!
echo.
echo Download from: https://www.python.org/downloads/
echo IMPORTANT: Check "Add Python to PATH"
echo.
pause

:end
pause
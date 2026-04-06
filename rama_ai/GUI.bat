@echo off
REM RAMA AI - GUI Launcher (Desktop App!)
cd /d "%~dp0"

echo.
echo 🤖 Starting RAMA AI Desktop UI...
echo.

REM Try py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Starting GUI...
    py gui.py
    goto :end
)

REM Try python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Starting GUI...
    python gui.py
    goto :end
)

echo.
echo ❌ Python not installed!
echo.
pause

:end
@echo off
REM RAMA AI - Animated GUI Launcher
cd /d "%~dp0"

echo.
echo 🤖 Starting RAMA AI - Animated 3D GUI!
echo.

REM Try py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Starting GUI...
    py frontend\animated_gui.py
    goto :end
)

REM Try python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Starting GUI...
    python frontend\animated_gui.py
    goto :end
)

echo.
echo ❌ Python not installed!
echo Download: https://www.python.org/downloads/
echo.
pause

:end
pause
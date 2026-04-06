@echo off
REM RAMA AI - Image GUI Launcher
cd /d "%~dp0"

echo.
echo 🤖 Starting RAMA AI - Image Based GUI!
echo.

py --version >nul 2>&1
if %errorlevel% equ 0 (
    py frontend\image_gui.py
    goto :end
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    python frontend\image_gui.py
    goto :end
)

echo ❌ Python not found!
pause

:end
pause
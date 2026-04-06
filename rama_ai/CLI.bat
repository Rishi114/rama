@echo off
REM RAMA AI - CLI Launcher (No voice, text only)
cd /d "%~dp0"

echo.
echo 🤖 Starting RAMA AI (Text Mode)...
echo.

REM Try py launcher first
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Using py launcher
    py main.py --cli
    goto :end
)

REM Try python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Using python
    python main.py --cli
    goto :end
)

REM Try python3
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Using python3
    python3 main.py --cli
    goto :end
)

echo.
echo ❌ Python not installed!
echo.
pause

:end
pause
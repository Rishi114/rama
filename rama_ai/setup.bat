@echo off
REM RAMA AI - Python Setup Helper
REM Run this to install/setup Python for RAMA

echo.
echo ========================================
echo   🤖 RAMA AI - Python Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python is already installed!
    python --version
    echo.
    goto :install_deps
)

REM Check for python3
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python3 is installed!
    python3 --version
    echo.
    goto :install_deps
)

REM Python not found - offer to install
echo ❌ Python not found!
echo.
echo Please install Python from: https://www.python.org/downloads/
echo.
echo Or search in Microsoft Store: "Python"
echo.
echo After installing, run this script again!
echo.
pause
exit /b

:install_deps
echo ========================================
echo 📦 Installing RAMA dependencies...
echo ========================================
echo.

REM Install core dependencies
pip install customtkinter requests aiohttp psutil pydantic pyyaml

echo.
echo ========================================
echo ✅ Setup Complete!
echo ========================================
echo.
echo Now run: python main.py
echo.
pause
@echo off
REM Setup script for Phishing URL Detector - Backend (Windows)

echo ================================
echo Setting up Phishing URL Detector Backend
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
echo ✓ %PYTHON_VER% found
echo.

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create dummy model
echo Creating dummy ML model...
python create_dummy_model.py

echo.
echo ================================
echo ✓ Setup complete!
echo ================================
echo.
echo To start the backend server, run:
echo   venv\Scripts\activate.bat
echo   python app.py
echo.
pause

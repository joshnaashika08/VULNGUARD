@echo off
setlocal
echo ============================================
echo   VULNGUARD ^| AI Security Engine
echo ============================================

:: Check for Python
echo [STEP] Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python from python.org
    pause
    exit /b
)

echo.
echo [STEP] Installing/Verifying Backend Dependencies...
python -m pip install -r server\requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Problem installing dependencies. 
    echo Trying alternative method...
    python -m pip install --user -r server\requirements.txt
)

echo.
echo [STEP] Starting Backend Server...
echo Site will be at: http://127.0.0.1:5000
echo.
echo [KEEP THIS WINDOW OPEN TO USE THE SCANNER]
echo ============================================

:: Run server
python server\app.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The server stopped unexpectedly.
    pause
)
pause

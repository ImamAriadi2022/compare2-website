@echo off
echo ============================================
echo Website Comparator - Setup Script
echo ============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo Silakan install Python dari https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Membuat virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Gagal membuat virtual environment
    pause
    exit /b 1
)

echo [2/4] Aktivasi virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Upgrade pip...
python -m pip install --upgrade pip

echo [4/4] Install dependencies...
pip install -r requirements.txt

echo.
echo ============================================
echo [SUCCESS] Setup selesai!
echo ============================================
echo.
echo Langkah selanjutnya:
echo 1. Aktivasi environment: venv\Scripts\activate.bat
echo 2. Install Playwright browsers: playwright install chromium
echo 3. Jalankan example: python example.py
echo.
pause

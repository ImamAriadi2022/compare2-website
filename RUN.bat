@echo off
echo ========================================
echo WEBSITE COMPARATOR - QUICK RUN
echo ========================================
echo.

:: Check if venv exists
if not exist "venv" (
    echo [ERROR] Virtual environment tidak ditemukan!
    echo Jalankan setup.bat terlebih dahulu.
    echo.
    pause
    exit /b 1
)

:: Activate venv
call venv\Scripts\activate.bat

:: Check if dependencies installed
python -c "import requests" 2>nul
if errorlevel 1 (
    echo [ERROR] Dependencies belum terinstall!
    echo Jalankan setup.bat terlebih dahulu.
    echo.
    pause
    exit /b 1
)

:: Run quick_start.py
echo [INFO] Menjalankan quick_start.py...
echo.
python quick_start.py

echo.
echo ========================================
echo Selesai! Cek folder output/ untuk hasil PDF
echo ========================================
pause

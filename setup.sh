#!/bin/bash

echo "============================================"
echo "Website Comparator - Setup Script"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 tidak ditemukan!"
    echo "Silakan install Python dari https://www.python.org/downloads/"
    exit 1
fi

echo "[1/4] Membuat virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Gagal membuat virtual environment"
    exit 1
fi

echo "[2/4] Aktivasi virtual environment..."
source venv/bin/activate

echo "[3/4] Upgrade pip..."
python -m pip install --upgrade pip

echo "[4/4] Install dependencies..."
pip install -r requirements.txt

echo ""
echo "============================================"
echo "[SUCCESS] Setup selesai!"
echo "============================================"
echo ""
echo "Langkah selanjutnya:"
echo "1. Aktivasi environment: source venv/bin/activate"
echo "2. Install Playwright browsers: playwright install chromium"
echo "3. Jalankan example: python example.py"
echo ""

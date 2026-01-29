# Website Output Capability Comparison Tool

Tool untuk membandingkan output capability antara dua website secara teknis dan menghasilkan laporan PDF.

## 📋 Daftar Isi
- [Fitur](#-fitur)
- [Instalasi](#-instalasi)
- [Cara Menjalankan](#-cara-menjalankan)
- [Penggunaan](#-penggunaan)
- [Memahami Hasil](#-memahami-hasil)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Fitur

Membandingkan **6 jenis output capability**:
1. **Output Grafik / Chart** - Deteksi canvas, SVG, library chart (Chart.js, D3.js, dll)
2. **Output Data Tabel** - Deteksi tabel dinamis, DataTables, grid JS
3. **Output File** - Deteksi tombol download CSV, Excel, PDF, Gambar
4. **Output Dinamis / Real-time** - Deteksi WebSocket, SSE, polling
5. **Output Interaktif** - Input form yang memicu perubahan output
6. **Output Berbasis API** - Fetch/XHR yang merender data ke UI

---

## 💻 Instalasi

### Prerequisite
- Python 3.8 atau lebih tinggi
- Koneksi internet
- Google Chrome (akan otomatis terinstall ChromeDriver)

### Langkah Instalasi

**Windows:**
```bash
# 1. Masuk ke folder project
cd c:\programming\compare2-website

# 2. Jalankan setup otomatis
setup.bat

# 3. Aktivasi virtual environment
venv\Scripts\activate.bat

# SELESAI! Tidak perlu install Playwright lagi
```

**Linux/Mac:**
```bash
# 1. Masuk ke folder project
cd /path/to/compare2-website

# 2. Jalankan setup otomatis
chmod +x setup.sh
./setup.sh

# 3. Aktivasi virtual environment
source venv/bin/activate

# SELESAI! Tidak perlu install Playwright lagi
```

### Instalasi Manual (Opsional)

```bash
# 1. Buat virtual environment
python -m venv venv

# 2. Aktivasi environment
# Windows:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### ✅ Verifikasi Instalasi

```bash
python test_suite.py
```

Jika semua test **PASSED**, instalasi berhasil!

---

## 🚀 Cara Menjalankan

### Metode 1: Quick Start (PALING MUDAH)

1. **Edit file `quick_start.py`**

   Buka file `quick_start.py` dan ganti URL di bagian ini:
   ```python
   # Website A - Masukkan URL yang ingin Anda analisis
   WEBSITE_A_URLS = [
       "https://contoh-a.com/dashboard",
       "https://contoh-a.com/analytics",
   ]

   # Website B - Masukkan URL yang ingin Anda analisis
   WEBSITE_B_URLS = [
       "https://contoh-b.com/dashboard",
       "https://contoh-b.com/reports",
   ]
   
   # Nama website (opsional)
   WEBSITE_A_NAME = "Website A"
   WEBSITE_B_NAME = "Website B"
   ```

2. **Jalankan script**
   ```bash
   python quick_start.py
   ```

3. **Buka hasil PDF**
   
   File PDF akan tersimpan di folder `output/`

### Metode 2: Menggunakan Example

Jalankan contoh yang sudah disiapkan:
```bash
python example.py
```

### Metode 3: Import di Script Python Anda

```python
from website_comparator import compare_websites

# Definisikan URLs
website_a_urls = [
    "https://site-a.com/page1",
    "https://site-a.com/page2",
]

website_b_urls = [
    "https://site-b.com/page1",
    "https://site-b.com/page2",
]

# Jalankan analisis
result = compare_websites(
    website_a_urls=website_a_urls,
    website_b_urls=website_b_urls,
    website_a_name="Website A",
    website_b_name="Website B",
    output_pdf="hasil_perbandingan.pdf"
)

print(f"PDF tersimpan di: {result['pdf_path']}")
```

---

## 📖 Penggunaan

### Format URL

**✅ BENAR:**
```python
urls = [
    "https://example.com/dashboard",
    "https://example.com/analytics",
    "https://example.com/reports"
]
```

**❌ SALAH:**
```python
urls = ["example.com"]  # Harus pakai https://
urls = []  # Minimal 1 URL
```

### Customisasi Lanjutan

```python
from website_comparator import WebsiteComparator

# Initialize dengan custom settings
comparator = WebsiteComparator(
    screenshot_dir="my_screenshots",  # Folder screenshot
    output_dir="my_reports"           # Folder output PDF
)

# Jalankan analisis
result = comparator.compare(
    website_a_urls=["https://a.com"],
    website_b_urls=["https://b.com"],
    website_a_name="Website A",
    website_b_name="Website B"
)

# Akses hasil detail
print(f"Website A capabilities:")
for cap_key, cap_data in result['website_a_capabilities'].items():
    if cap_data['supported']:
        print(f"  ✓ {cap_key}")
        print(f"    Confidence: {cap_data['confidence']}")
        print(f"    Found in: {cap_data['url_count']} URLs")
```

---

## 📊 Memahami Hasil

### Struktur Output PDF

1. **Halaman Sampul**
   - Judul analisis
   - Nama kedua website
   - Tanggal dan waktu analisis

2. **Metodologi**
   - Pendekatan verifikasi
   - Kriteria bukti teknis

3. **Tabel Ringkasan Perbandingan**
   - 6 capability dengan status ✓ atau ✗
   - Level confidence (High/Medium/Low)

4. **Detail Per Capability**
   - Screenshot sebagai bukti
   - Penjelasan teknis
   - URL yang ditemukan

5. **Kesimpulan**
   - Ringkasan perbandingan
   - Rekomendasi

### Interpretasi Confidence Level

- **High (90-100%)**: Bukti sangat kuat (multiple indicators)
- **Medium (60-89%)**: Bukti cukup (beberapa indicators)
- **Low (30-59%)**: Bukti lemah (1-2 indicators)
- **Very Low (<30%)**: Tidak yakin

### Contoh Output

```
Website A: ✓ Chart Output (Confidence: High)
  - Detected: canvas, Chart.js library
  - Found in: 2 out of 3 URLs
  
Website B: ✗ Chart Output (Confidence: Low)
  - No chart elements detected
```

---

## 🛠 Troubleshooting

### Masalah: "Python tidak ditemukan"

**Solusi:**
1. Install Python dari [python.org](https://www.python.org/downloads/)
2. Pastikan centang "Add Python to PATH" saat instalasi
3. Restart terminal/command prompt

### Masalah: "pip tidak dikenali"

**Solusi:**
```bash
python -m pip install --upgrade pip
```

### Masalah: "ModuleNotFoundError"

**Solusi:**
```bash
# Pastikan virtual environment aktif
# Windows:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install ulang dependencies
pip install -r requirements.txt
```

### Masalah: "Website tidak bisa diakses"

**Solusi:**
1. Periksa koneksi internet
2. Cek apakah URL benar (harus pakai `https://`)
3. Coba buka URL di browser manual
4. Beberapa website mungkin memblokir automated access

### Masalah: "Error saat generate PDF"

**Solusi:**
```bash
# Install ulang reportlab
pip uninstall reportlab
pip install reportlab==4.0.9
```

### Masalah: Setup.bat error

**Solusi:**
```bash
# Instalasi manual
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

## 📝 Metodologi Teknis

Tool ini menggunakan:
- **Selenium ChromeDriver** untuk membuka browser real dan render JavaScript
- **BeautifulSoup4** untuk parsing HTML
- **DOM Analysis** untuk deteksi elemen HTML (canvas, SVG, table, dll)
- **Pattern Matching** untuk deteksi JavaScript library
- **Screenshot Capture** untuk bukti visual
- **PDF Generation** (ReportLab) untuk laporan komprehensif

---

## ⚙️ Command Reference

### Testing
```bash
# Test semua module
python test_suite.py

# Test specific module
python -c "from web_scraper import WebScraper; print('OK')"
python -c "from capability_analyzer import CapabilityAnalyzer; print('OK')"
python -c "from pdf_generator import PDFGenerator; print('OK')"
```

### Dependencies
```bash
# List semua package
pip list

# Check specific package
pip show beautifulsoup4
pip show reportlab
```

### Clean Up
```bash
# Hapus cache
rm -rf __pycache__
rm -rf output/
rm -rf screenshots/
```

---

## 🔒 Batasan

- ✗ Tidak bisa mengakses halaman yang memerlukan login/authentication
- ✓ Bisa menangani website dengan JavaScript dinamis (menggunakan ChromeDriver)
- ✓ Cocok untuk analisis website modern (dashboard, chart, dll)
- ✓ Screenshot otomatis tersedia
- ✓ Memerlukan koneksi internet
- ✓ Waktu analisis: ~1-2 menit per website (tergantung jumlah URL)

---

## 📄 Lisensi

Lihat file [LICENSE](LICENSE) untuk detail.

---

## 💡 Tips

1. **Gunakan URL spesifik** yang memiliki fitur yang ingin Anda analisis
2. **Jangan terlalu banyak URL** (3-5 URL per website sudah cukup)
3. **Pilih halaman yang berbeda** (dashboard, reports, analytics, dll)
4. **Periksa PDF hasil** untuk insight detail dengan screenshot

---

**Butuh bantuan?** Baca file dokumentasi tambahan:
- `GUIDE.md` - Panduan lengkap
- `COMMANDS.md` - Command reference
- `TECHNICAL_DOCS.md` - Dokumentasi teknis
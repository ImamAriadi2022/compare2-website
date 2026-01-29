# Panduan Lengkap - Website Output Capability Comparison Tool

## 📋 Daftar Isi
1. [Instalasi](#instalasi)
2. [Quick Start](#quick-start)
3. [Penggunaan Lanjutan](#penggunaan-lanjutan)
4. [Memahami Hasil](#memahami-hasil)
5. [Tips & Best Practices](#tips--best-practices)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## 🚀 Instalasi

### Prerequisite
- Python 3.8 atau lebih tinggi
- Koneksi internet
- ~500MB disk space untuk browser

### Windows

```bash
# 1. Clone/download repository
cd c:\programming\compare2-website

# 2. Jalankan setup script
setup.bat

# 3. Aktivasi virtual environment
venv\Scripts\activate.bat

# 4. Install Playwright browser
playwright install chromium
```

### Linux/Mac

```bash
# 1. Clone/download repository
cd /path/to/compare2-website

# 2. Jalankan setup script
chmod +x setup.sh
./setup.sh

# 3. Aktivasi virtual environment
source venv/bin/activate

# 4. Install Playwright browser
playwright install chromium
```

### Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate.bat

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

### Verifikasi Instalasi

```bash
python test_suite.py
```

Jika semua test PASSED, instalasi berhasil!

---

## ⚡ Quick Start

### Cara Tercepat (5 Menit)

1. **Edit `quick_start.py`**

```python
# Ganti URL dengan website yang ingin Anda analisis
WEBSITE_A_URLS = [
    "https://your-website-a.com/dashboard",
    "https://your-website-a.com/analytics"
]

WEBSITE_B_URLS = [
    "https://your-website-b.com/dashboard",
    "https://your-website-b.com/reports"
]

WEBSITE_A_NAME = "Nama Website A"
WEBSITE_B_NAME = "Nama Website B"
```

2. **Jalankan**

```bash
python quick_start.py
```

3. **Buka PDF hasil**

File PDF akan tersimpan di folder `output/`

---

## 📚 Penggunaan Lanjutan

### Method 1: Import di Script Python

```python
from website_comparator import compare_websites

# Definisikan URLs
website_a_urls = [
    "https://site-a.com/page1",
    "https://site-a.com/page2",
    "https://site-a.com/page3"
]

website_b_urls = [
    "https://site-b.com/page1",
    "https://site-b.com/page2",
    "https://site-b.com/page3"
]

# Jalankan analisis
result = compare_websites(
    website_a_urls=website_a_urls,
    website_b_urls=website_b_urls,
    website_a_name="Company A Dashboard",
    website_b_name="Company B Analytics",
    output_pdf="comparison_A_vs_B.pdf"  # Optional
)

# Akses hasil
print(f"PDF saved to: {result['pdf_path']}")
print(f"Screenshots in: {result['screenshot_dir']}")
```

### Method 2: Customized Class

```python
from website_comparator import WebsiteComparator

# Initialize dengan custom directories
comparator = WebsiteComparator(
    screenshot_dir="my_screenshots",
    output_dir="my_reports"
)

# Run comparison
result = comparator.compare(
    website_a_urls=["https://a.com"],
    website_b_urls=["https://b.com"],
    website_a_name="Website A",
    website_b_name="Website B"
)

# Access detailed capabilities
for cap_key, cap_data in result['website_a_capabilities'].items():
    if cap_data['supported']:
        print(f"✓ {cap_key}")
        print(f"  Confidence: {cap_data['confidence']}")
        print(f"  Found in: {cap_data['url_count']} URLs")
```

### Method 3: Interactive Example

```bash
python example.py
```

Pilih dari beberapa contoh yang sudah disiapkan.

---

## 📊 Memahami Hasil

### Struktur PDF

#### 1. Halaman Sampul
- Judul analisis
- Nama kedua website
- Tanggal analisis

#### 2. Metodologi
- Pendekatan verifikasi
- Kriteria bukti teknis
- Batasan analisis

#### 3. Tabel Ringkasan
```
┌─────────────────────┬────────────┬────────────┬────────────┐
│ Capability          │ Website A  │ Website B  │ Keunggulan │
├─────────────────────┼────────────┼────────────┼────────────┤
│ Output Grafik/Chart │ ✓ (tinggi) │ ✗          │ Website A  │
│ Output Data Tabel   │ ✓ (sedang) │ ✓ (tinggi) │ Website B* │
│ ...                 │ ...        │ ...        │ ...        │
└─────────────────────┴────────────┴────────────┴────────────┘

* = Tingkat kepercayaan lebih tinggi
```

#### 4. Detail Per Capability

Untuk setiap capability:

**Website A:**
- Status: DIDUKUNG/TIDAK DIDUKUNG
- Tingkat kepercayaan: Tinggi/Sedang/Rendah
- URL sumber
- Indikator teknis (bullets)
- Screenshot (visual proof)

**Website B:**
- Struktur sama

**Catatan Analisis:**
Interpretasi hasil perbandingan

#### 5. Kesimpulan
- Capability unik Website A
- Capability unik Website B
- Capability yang sama
- Ringkasan keunggulan berbasis bukti

### Tingkat Kepercayaan

| Level | Arti | Contoh |
|-------|------|--------|
| **Tinggi** | Bukti teknis sangat kuat, library terdeteksi | Chart.js library + canvas element |
| **Sedang** | Bukti teknis cukup, elemen ada tapi library tidak jelas | Canvas element tanpa library |
| **Rendah** | Bukti teknis lemah, hanya indikasi CSS | Class="chart" tanpa elemen actual |

### Membaca Indikator Teknis

Contoh output:
```
Indikator Teknis:
• Ditemukan 3 elemen <canvas>
• Terdeteksi library chart: Chart.js, D3.js
• Ditemukan 2 chart dengan dimensi signifikan
• Ditemukan 5 elemen dengan class chart/graph
```

**Interpretasi:**
- Website ini PASTI memiliki capability chart
- Menggunakan 2 library chart (Chart.js dan D3.js)
- Ada 3 canvas dan 2 yang berukuran signifikan
- Tingkat kepercayaan: TINGGI

---

## 💡 Tips & Best Practices

### Pemilihan URL

✅ **LAKUKAN:**
- Pilih halaman dengan fitur yang jelas (dashboard, analytics, reports)
- Gunakan 3-5 URL per website (tidak terlalu banyak)
- Pilih halaman yang dapat diakses tanpa login
- Include halaman dengan variasi fitur

❌ **JANGAN:**
- Halaman login/auth
- Halaman yang butuh interaksi kompleks
- Halaman dengan infinite scroll
- Terlalu banyak URL (> 10 per website)

### Contoh URL Bagus vs Buruk

| ✅ BAGUS | ❌ BURUK |
|----------|----------|
| `/dashboard` | `/login` |
| `/analytics` | `/profile/settings` |
| `/reports` | `/admin` (butuh auth) |
| `/charts` | `/infinite-feed` |
| `/data-export` | `/` (homepage terlalu umum) |

### Optimasi Performa

1. **Batasi jumlah URL**: 3-5 URL optimal
2. **Pilih URL spesifik**: Hindari halaman terlalu besar
3. **Gunakan koneksi cepat**: Proses lebih cepat
4. **Jalankan di waktu off-peak**: Hindari jam sibuk

### Meningkatkan Akurasi

1. **Pilih halaman representatif**: Halaman yang menunjukkan fitur utama
2. **Multiple pages**: Analisis beberapa halaman untuk coverage lebih baik
3. **Review manual**: Selalu verify hasil dengan pengecekan manual
4. **Update screenshot**: Jika halaman berubah, run ulang analisis

---

## 🔧 Troubleshooting

### Error: "playwright not found"

**Solusi:**
```bash
pip install playwright
playwright install chromium
```

### Error: "Navigation timeout"

**Penyebab:** URL tidak dapat diakses atau loading terlalu lama

**Solusi:**
1. Cek koneksi internet
2. Cek apakah URL valid dan accessible
3. Increase timeout di `web_scraper.py` line 77:
   ```python
   await page.goto(url, wait_until='networkidle', timeout=60000)  # 60 detik
   ```

### Error: "Screenshot not found"

**Penyebab:** Gagal capture screenshot

**Solusi:**
1. Cek disk space
2. Cek permissions folder `screenshots/`
3. Verify halaman ter-render dengan baik

### Error: "Cannot load image in PDF"

**Penyebab:** Screenshot path tidak valid

**Solusi:**
1. Pastikan screenshot ada di folder
2. Cek path absolute vs relative
3. Re-run scraping jika screenshot missing

### Hasil PDF Kosong/Error

**Solusi:**
1. Cek apakah scraping berhasil (lihat folder screenshots)
2. Run test suite: `python test_suite.py`
3. Cek error log di console

### Performance Lambat

**Optimasi:**
1. Kurangi jumlah URL
2. Pilih halaman lebih ringan
3. Gunakan koneksi internet lebih cepat
4. Close aplikasi lain yang berat

---

## ❓ FAQ

### Q: Berapa lama waktu analisis?

**A:** Tergantung jumlah URL:
- 1 URL: ~10-15 detik
- 3 URLs per website (6 total): ~2 menit
- 5 URLs per website (10 total): ~3-4 menit

### Q: Apakah bisa analisis website yang butuh login?

**A:** Tidak secara otomatis. Tool ini hanya untuk halaman publik. Untuk website dengan login, Anda perlu:
1. Manual login dulu
2. Copy cookies/session
3. Modify `web_scraper.py` untuk inject cookies

### Q: Apakah hasil 100% akurat?

**A:** Tidak ada analisis otomatis yang 100% akurat. Tool ini memberikan:
- Tingkat kepercayaan untuk setiap finding
- Bukti teknis yang dapat diverifikasi
- Screenshot sebagai visual proof

Selalu review hasil secara manual.

### Q: Bisa compare lebih dari 2 website?

**A:** Tidak built-in, tapi bisa:
1. Compare A vs B, simpan hasil
2. Compare A vs C, simpan hasil
3. Compare B vs C, simpan hasil
4. Manual comparison dari 3 PDF

### Q: Bagaimana update tool ini?

**A:** 
1. Backup folder screenshots dan output
2. Download versi baru
3. Run setup ulang
4. Copy back data penting

### Q: Bisa export ke format lain (Excel, JSON)?

**A:** Saat ini hanya PDF. Untuk format lain, modifikasi `pdf_generator.py` atau extract data dari result dict:

```python
import json

result = compare_websites(...)

# Save to JSON
with open('result.json', 'w') as f:
    json.dump({
        'website_a': result['website_a_capabilities'],
        'website_b': result['website_b_capabilities']
    }, f, indent=2)
```

### Q: Tool ini aman? Apakah data dikirim ke server?

**A:** 
- 100% lokal, tidak ada data dikirim ke server eksternal
- Hanya connect ke URL yang Anda specify
- Semua data disimpan lokal di komputer Anda
- Open source, bisa review kode

### Q: Minimum system requirements?

**A:**
- OS: Windows 10+, macOS 10.13+, atau Linux modern
- RAM: 4GB minimum, 8GB recommended
- Disk: 500MB untuk browser + space untuk screenshots
- Internet: Stabil connection untuk scraping

### Q: Bisa dijalankan di server/cloud?

**A:** Ya, bisa di:
- Linux server dengan X virtual display
- Docker container dengan headless browser
- Cloud services (AWS, GCP, Azure)

Perlu konfigurasi tambahan untuk headless environment.

---

## 📞 Support & Contact

Jika ada pertanyaan atau issue:

1. **Check dokumentasi**:
   - [README.md](README.md) - Overview
   - [TECHNICAL_DOCS.md](TECHNICAL_DOCS.md) - Technical details

2. **Run test suite**:
   ```bash
   python test_suite.py
   ```

3. **Enable debug mode**:
   Edit `web_scraper.py` dan tambahkan print statements

4. **Check logs**:
   Review error messages di console

---

## 📝 Changelog

### Version 1.0.0
- Initial release
- Support 6 capability types
- PDF report generation
- Screenshot capture
- Network monitoring
- JavaScript library detection

---

## 🎯 Roadmap

Future improvements (optional):
- [ ] Support untuk multiple websites (> 2)
- [ ] Export ke Excel/JSON
- [ ] Interactive HTML report
- [ ] Login/authentication support
- [ ] Custom capability definitions
- [ ] Performance metrics
- [ ] Automated scheduling
- [ ] REST API interface

---

**Happy Analyzing! 🚀**

# Website Output Capability Comparison Tool

Tool untuk membandingkan output capability antara dua website secara teknis dan menghasilkan laporan PDF.

## Fitur

Membandingkan 6 jenis output capability:
1. **Output Grafik / Chart** - Deteksi canvas, SVG, library chart
2. **Output Data Tabel** - Deteksi tabel dinamis, grid JS
3. **Output File** - Deteksi download CSV, Excel, PDF, Gambar
4. **Output Dinamis / Real-time** - WebSocket, SSE, polling
5. **Output Interaktif** - Input yang memicu perubahan output
6. **Output Berbasis API** - Fetch/XHR yang render ke UI

## Instalasi

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Penggunaan

```python
from website_comparator import WebsiteComparator

# Definisikan URL untuk masing-masing website
website_a_urls = [
    "https://example-a.com/dashboard",
    "https://example-a.com/reports",
    "https://example-a.com/analytics"
]

website_b_urls = [
    "https://example-b.com/dashboard",
    "https://example-b.com/charts",
    "https://example-b.com/data"
]

# Jalankan analisis
comparator = WebsiteComparator()
comparator.compare(
    website_a_urls=website_a_urls,
    website_b_urls=website_b_urls,
    output_pdf="hasil_perbandingan.pdf"
)
```

## Metodologi

Tool ini menggunakan:
- **Browser Headless** (Playwright) untuk render halaman
- **DOM Analysis** untuk deteksi elemen HTML
- **JavaScript Runtime Inspection** untuk deteksi library
- **Network Monitoring** untuk deteksi API calls
- **Screenshot Capture** sebagai bukti visual
- **PDF Generation** untuk laporan komprehensif

## Output

File PDF berisi:
1. Halaman Sampul
2. Metodologi Singkat
3. Tabel Ringkasan Perbandingan
4. Detail Per Capability (dengan screenshot)
5. Kesimpulan

## Batasan

- Hanya menganalisis halaman publik (tanpa login)
- Memerlukan koneksi internet
- Waktu analisis tergantung jumlah URL dan kompleksitas halaman
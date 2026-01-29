# 🚀 PETUNJUK SINGKAT - CARA MENJALANKAN

## Langkah 1: Setup (Hanya Sekali)

```bash
# Jalankan setup
setup.bat

# Aktifkan environment
venv\Scripts\activate.bat
```

## Langkah 2: Edit URL

Buka file **`quick_start.py`** dan ganti bagian ini:

```python
WEBSITE_A_URLS = [
    "https://contoh-a.com/dashboard",  # <-- GANTI INI
    "https://contoh-a.com/analytics",
]

WEBSITE_B_URLS = [
    "https://contoh-b.com/dashboard",  # <-- GANTI INI
    "https://contoh-b.com/reports",
]
```

## Langkah 3: Jalankan

```bash
python quick_start.py
```

## Langkah 4: Lihat Hasil

Buka folder **`output/`** dan buka file PDF yang dihasilkan.

---

## 📝 Contoh Lengkap

```python
# File: quick_start.py (sudah tersedia)

WEBSITE_A_URLS = [
    "https://example.com/page1",
    "https://example.com/page2",
]

WEBSITE_B_URLS = [
    "https://competitor.com/page1",
    "https://competitor.com/page2",
]

WEBSITE_A_NAME = "My Website"
WEBSITE_B_NAME = "Competitor"
```

Lalu jalankan:
```bash
python quick_start.py
```

---

## ❓ Troubleshooting Cepat

**Masalah:** "Python tidak ditemukan"
- **Solusi:** Install Python dari python.org

**Masalah:** "pip tidak dikenali"
- **Solusi:** `python -m pip install --upgrade pip`

**Masalah:** "ModuleNotFoundError"
- **Solusi:** 
  ```bash
  venv\Scripts\activate.bat
  pip install -r requirements.txt
  ```

---

**Untuk dokumentasi lengkap, lihat README.md**

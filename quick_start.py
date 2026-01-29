"""
Quick Start Script
Contoh sederhana untuk mulai menggunakan tool
"""

from website_comparator import compare_websites


# ============================================================
# EDIT BAGIAN INI DENGAN URL ANDA
# ============================================================

# Website A - Masukkan URL yang ingin Anda analisis
WEBSITE_A_URLS = [
    "https://example-a.com/page1",
    "https://example-a.com/page2",
    # Tambahkan URL lainnya di sini
]

# Website B - Masukkan URL yang ingin Anda analisis
WEBSITE_B_URLS = [
    "https://example-b.com/page1",
    "https://example-b.com/page2",
    # Tambahkan URL lainnya di sini
]

# Nama website (opsional)
WEBSITE_A_NAME = "Website A"
WEBSITE_B_NAME = "Website B"

# Output PDF path (opsional, akan auto-generate jika kosong)
OUTPUT_PDF = None  # atau "output/my_comparison.pdf"

# ============================================================
# JANGAN EDIT DI BAWAH INI
# ============================================================

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║               WEBSITE OUTPUT CAPABILITY COMPARISON                ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    print("Configuration:")
    print(f"  Website A: {WEBSITE_A_NAME} ({len(WEBSITE_A_URLS)} URLs)")
    print(f"  Website B: {WEBSITE_B_NAME} ({len(WEBSITE_B_URLS)} URLs)")
    print()
    
    # Validasi URLs
    if not WEBSITE_A_URLS or not WEBSITE_B_URLS:
        print("⚠ ERROR: Silakan edit quick_start.py dan masukkan URL yang valid!")
        print("\nContoh:")
        print('  WEBSITE_A_URLS = ["https://example-a.com/page1"]')
        print('  WEBSITE_B_URLS = ["https://example-b.com/page1"]')
        return
    
    # Confirm sebelum run
    confirm = input("Lanjutkan analisis? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Dibatalkan.")
        return
    
    print("\nMemulai analisis...\n")
    
    # Jalankan comparison
    try:
        result = compare_websites(
            website_a_urls=WEBSITE_A_URLS,
            website_b_urls=WEBSITE_B_URLS,
            website_a_name=WEBSITE_A_NAME,
            website_b_name=WEBSITE_B_NAME,
            output_pdf=OUTPUT_PDF
        )
        
        print("\n" + "="*70)
        print("✓ ANALISIS SELESAI!")
        print("="*70)
        print(f"\nLaporan PDF: {result['pdf_path']}")
        print(f"Screenshots: {result['screenshot_dir']}/")
        print("\nBuka file PDF untuk melihat hasil lengkap!")
        print("="*70)
        
    except Exception as e:
        print(f"\n⚠ ERROR: {str(e)}")
        print("\nTips:")
        print("  - Pastikan URL dapat diakses")
        print("  - Pastikan koneksi internet aktif")
        print("  - Pastikan Playwright sudah terinstall: playwright install chromium")


if __name__ == "__main__":
    main()

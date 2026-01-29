"""
Example Usage - Website Comparator

Contoh penggunaan tool untuk membandingkan dua website
"""

from website_comparator import compare_websites


def example_basic():
    """Example dasar dengan URLs sederhana"""
    
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Comparison")
    print("="*70 + "\n")
    
    # Define URLs to compare
    website_a_urls = [
        "https://www.chartjs.org/",  # Has charts
        "https://www.chartjs.org/docs/latest/samples/information.html"
    ]
    
    website_b_urls = [
        "https://plotly.com/python/",  # Also has charts
        "https://plotly.com/python/basic-charts/"
    ]
    
    # Run comparison
    result = compare_websites(
        website_a_urls=website_a_urls,
        website_b_urls=website_b_urls,
        website_a_name="Chart.js Documentation",
        website_b_name="Plotly Documentation",
        output_pdf="output/example_basic_comparison.pdf"
    )
    
    print(f"\n✓ Comparison complete!")
    print(f"  PDF: {result['pdf_path']}")


def example_dashboard_comparison():
    """Example perbandingan dashboard"""
    
    print("\n" + "="*70)
    print("EXAMPLE 2: Dashboard Comparison")
    print("="*70 + "\n")
    
    # Contoh dengan dashboard (gunakan URL real yang ingin dibandingkan)
    website_a_urls = [
        "https://example-dashboard-a.com/overview",
        "https://example-dashboard-a.com/analytics",
        "https://example-dashboard-a.com/reports"
    ]
    
    website_b_urls = [
        "https://example-dashboard-b.com/dashboard",
        "https://example-dashboard-b.com/data",
        "https://example-dashboard-b.com/exports"
    ]
    
    result = compare_websites(
        website_a_urls=website_a_urls,
        website_b_urls=website_b_urls,
        website_a_name="Dashboard A",
        website_b_name="Dashboard B"
        # output_pdf akan auto-generate dengan timestamp
    )
    
    print(f"\n✓ Comparison complete!")
    print(f"  PDF: {result['pdf_path']}")


def example_custom_analysis():
    """Example dengan customization lebih lanjut"""
    
    from website_comparator import WebsiteComparator
    
    print("\n" + "="*70)
    print("EXAMPLE 3: Custom Analysis")
    print("="*70 + "\n")
    
    # Initialize with custom directories
    comparator = WebsiteComparator(
        screenshot_dir="custom_screenshots",
        output_dir="custom_output"
    )
    
    # URLs to compare
    website_a_urls = [
        "https://example-a.com/page1",
        "https://example-a.com/page2"
    ]
    
    website_b_urls = [
        "https://example-b.com/page1",
        "https://example-b.com/page2"
    ]
    
    # Run comparison
    result = comparator.compare(
        website_a_urls=website_a_urls,
        website_b_urls=website_b_urls,
        website_a_name="Custom Website A",
        website_b_name="Custom Website B",
        output_pdf="custom_output/my_comparison.pdf"
    )
    
    print(f"\n✓ Custom comparison complete!")
    print(f"  PDF: {result['pdf_path']}")
    print(f"  Screenshots: {result['screenshot_dir']}/")
    
    # Access detailed results
    print("\n--- Website A Capabilities ---")
    for cap_key, cap_data in result['website_a_capabilities'].items():
        if cap_data['supported']:
            print(f"  ✓ {cap_key}: {cap_data['confidence']} confidence")
    
    print("\n--- Website B Capabilities ---")
    for cap_key, cap_data in result['website_b_capabilities'].items():
        if cap_data['supported']:
            print(f"  ✓ {cap_key}: {cap_data['confidence']} confidence")


def main():
    """Main function untuk menjalankan examples"""
    
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║          WEBSITE OUTPUT CAPABILITY COMPARISON - EXAMPLES           ║
    ╚════════════════════════════════════════════════════════════════════╝
    
    Pilih example yang ingin dijalankan:
    
    1. Basic Comparison (Chart.js vs Plotly)
    2. Dashboard Comparison (Custom URLs)
    3. Custom Analysis with detailed results
    
    Atau edit file ini untuk menggunakan URL Anda sendiri!
    """)
    
    choice = input("\nPilih example (1-3, atau Enter untuk skip): ").strip()
    
    if choice == "1":
        example_basic()
    elif choice == "2":
        print("\n⚠ Note: Gunakan URL real untuk dashboard yang ingin dibandingkan")
        confirm = input("Lanjutkan dengan URL example? (y/n): ").strip().lower()
        if confirm == 'y':
            example_dashboard_comparison()
    elif choice == "3":
        print("\n⚠ Note: Gunakan URL real untuk analysis yang sebenarnya")
        confirm = input("Lanjutkan dengan URL example? (y/n): ").strip().lower()
        if confirm == 'y':
            example_custom_analysis()
    else:
        print("\n✓ Silakan edit file example.py dengan URL Anda sendiri!")
        print("\nQuick start:")
        print("-" * 70)
        print("""
from website_comparator import compare_websites

result = compare_websites(
    website_a_urls=["https://your-site-a.com/page1", "https://your-site-a.com/page2"],
    website_b_urls=["https://your-site-b.com/page1", "https://your-site-b.com/page2"],
    website_a_name="My Site A",
    website_b_name="My Site B"
)

print(f"PDF Report: {result['pdf_path']}")
        """)


if __name__ == "__main__":
    main()

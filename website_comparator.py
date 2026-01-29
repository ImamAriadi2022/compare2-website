"""
Website Comparator - Main Module
Script utama untuk menjalankan perbandingan website
"""

import asyncio
from typing import List
import os
from datetime import datetime

from web_scraper import WebScraper
from capability_analyzer import CapabilityAnalyzer
from pdf_generator import PDFGenerator


class WebsiteComparator:
    """Main class untuk menjalankan perbandingan website"""
    
    def __init__(self, screenshot_dir: str = "screenshots", output_dir: str = "output"):
        """
        Initialize WebsiteComparator
        
        Args:
            screenshot_dir: Directory untuk menyimpan screenshots
            output_dir: Directory untuk menyimpan output PDF
        """
        self.screenshot_dir = screenshot_dir
        self.output_dir = output_dir
        
        # Create directories
        os.makedirs(screenshot_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize modules
        self.scraper = WebScraper(screenshot_dir=screenshot_dir)
        self.analyzer = CapabilityAnalyzer()
        self.pdf_generator = PDFGenerator()
    
    def compare(
        self,
        website_a_urls: List[str],
        website_b_urls: List[str],
        website_a_name: str = "Website A",
        website_b_name: str = "Website B",
        output_pdf: str = None
    ):
        """
        Jalankan perbandingan lengkap antara dua website
        
        Args:
            website_a_urls: List URL untuk Website A
            website_b_urls: List URL untuk Website B
            website_a_name: Nama Website A (optional)
            website_b_name: Nama Website B (optional)
            output_pdf: Path output PDF (optional, akan auto-generate jika tidak diisi)
        """
        
        print("=" * 70)
        print("WEBSITE OUTPUT CAPABILITY COMPARISON")
        print("=" * 70)
        print(f"\n{website_a_name}: {len(website_a_urls)} URLs")
        print(f"{website_b_name}: {len(website_b_urls)} URLs")
        print("\n" + "=" * 70)
        
        # Step 1: Scrape Website A
        print(f"\n[STEP 1/5] Scraping {website_a_name}...")
        print("-" * 70)
        website_a_data = asyncio.run(
            self.scraper.scrape_multiple_urls(website_a_urls, website_a_name)
        )
        print(f"[DONE] Scraped {len(website_a_data)} pages from {website_a_name}")
        
        # Step 2: Scrape Website B
        print(f"\n[STEP 2/5] Scraping {website_b_name}...")
        print("-" * 70)
        website_b_data = asyncio.run(
            self.scraper.scrape_multiple_urls(website_b_urls, website_b_name)
        )
        print(f"[DONE] Scraped {len(website_b_data)} pages from {website_b_name}")
        
        # Step 3: Analyze capabilities for Website A
        print(f"\n[STEP 3/5] Analyzing capabilities for {website_a_name}...")
        print("-" * 70)
        website_a_capabilities = self.analyzer.aggregate_website_capabilities(website_a_data)
        self._print_capability_summary(website_a_name, website_a_capabilities)
        
        # Step 4: Analyze capabilities for Website B
        print(f"\n[STEP 4/5] Analyzing capabilities for {website_b_name}...")
        print("-" * 70)
        website_b_capabilities = self.analyzer.aggregate_website_capabilities(website_b_data)
        self._print_capability_summary(website_b_name, website_b_capabilities)
        
        # Step 5: Generate PDF report
        print(f"\n[STEP 5/5] Generating PDF report...")
        print("-" * 70)
        
        if output_pdf is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_pdf = os.path.join(
                self.output_dir,
                f"comparison_{website_a_name}_{website_b_name}_{timestamp}.pdf"
            )
        
        self.pdf_generator.generate_report(
            website_a_name=website_a_name,
            website_b_name=website_b_name,
            website_a_capabilities=website_a_capabilities,
            website_b_capabilities=website_b_capabilities,
            output_path=output_pdf
        )
        
        # Final summary
        print("\n" + "=" * 70)
        print("COMPARISON COMPLETE!")
        print("=" * 70)
        print(f"\nPDF Report: {output_pdf}")
        print(f"Screenshots: {self.screenshot_dir}/")
        print("\n" + "=" * 70)
        
        return {
            'website_a_name': website_a_name,
            'website_b_name': website_b_name,
            'website_a_capabilities': website_a_capabilities,
            'website_b_capabilities': website_b_capabilities,
            'pdf_path': output_pdf,
            'screenshot_dir': self.screenshot_dir
        }
    
    def _print_capability_summary(self, website_name: str, capabilities: dict):
        """Print capability summary to console"""
        
        capability_names = {
            'output_grafik_chart': 'Output Grafik/Chart',
            'output_data_tabel': 'Output Data Tabel',
            'output_file': 'Output File',
            'output_dinamis_realtime': 'Output Dinamis/Real-time',
            'output_interaktif': 'Output Interaktif',
            'output_berbasis_api': 'Output Berbasis API'
        }
        
        print(f"\nCapabilities for {website_name}:")
        print("-" * 70)
        
        for key, name in capability_names.items():
            data = capabilities.get(key, {})
            supported = data.get('supported', False)
            confidence = data.get('confidence', 'rendah')
            url_count = data.get('url_count', 0)
            
            status_icon = "✓" if supported else "✗"
            status_text = f"{status_icon} {name}"
            
            if supported:
                status_text += f" (Confidence: {confidence}, Found in {url_count} URL(s))"
            
            print(status_text)


# Convenience function for quick usage
def compare_websites(
    website_a_urls: List[str],
    website_b_urls: List[str],
    website_a_name: str = "Website A",
    website_b_name: str = "Website B",
    output_pdf: str = None
):
    """
    Convenience function untuk menjalankan perbandingan
    
    Args:
        website_a_urls: List URL untuk Website A
        website_b_urls: List URL untuk Website B
        website_a_name: Nama Website A
        website_b_name: Nama Website B
        output_pdf: Path output PDF (optional)
    
    Returns:
        Dict dengan hasil perbandingan dan path ke PDF
    """
    
    comparator = WebsiteComparator()
    return comparator.compare(
        website_a_urls=website_a_urls,
        website_b_urls=website_b_urls,
        website_a_name=website_a_name,
        website_b_name=website_b_name,
        output_pdf=output_pdf
    )


if __name__ == "__main__":
    # Example usage
    print("Website Comparator")
    print("=" * 70)
    print("\nUsage:")
    print("  from website_comparator import compare_websites")
    print("\n  result = compare_websites(")
    print("      website_a_urls=['https://example-a.com'],")
    print("      website_b_urls=['https://example-b.com'],")
    print("      website_a_name='Example A',")
    print("      website_b_name='Example B'")
    print("  )")
    print("\nSee example.py for complete example")
    print("=" * 70)

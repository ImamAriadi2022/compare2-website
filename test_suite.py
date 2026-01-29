"""
Test Suite untuk Website Comparator
Menguji setiap modul secara terpisah
"""

import asyncio
import os
import sys


def test_imports():
    """Test apakah semua module bisa diimport"""
    print("\n" + "="*70)
    print("TEST 1: Import Modules")
    print("="*70)
    
    try:
        from web_scraper import WebScraper
        print("✓ web_scraper imported")
    except Exception as e:
        print(f"✗ web_scraper failed: {e}")
        return False
    
    try:
        from capability_analyzer import CapabilityAnalyzer
        print("✓ capability_analyzer imported")
    except Exception as e:
        print(f"✗ capability_analyzer failed: {e}")
        return False
    
    try:
        from pdf_generator import PDFGenerator
        print("✓ pdf_generator imported")
    except Exception as e:
        print(f"✗ pdf_generator failed: {e}")
        return False
    
    try:
        from website_comparator import WebsiteComparator
        print("✓ website_comparator imported")
    except Exception as e:
        print(f"✗ website_comparator failed: {e}")
        return False
    
    print("\n✓ All modules imported successfully!")
    return True


def test_dependencies():
    """Test apakah semua dependencies terinstall"""
    print("\n" + "="*70)
    print("TEST 2: Check Dependencies")
    print("="*70)
    
    dependencies = [
        ('playwright', 'playwright.async_api'),
        ('beautifulsoup4', 'bs4'),
        ('reportlab', 'reportlab'),
        ('Pillow', 'PIL')
    ]
    
    all_ok = True
    for package_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✓ {package_name} installed")
        except ImportError:
            print(f"✗ {package_name} NOT installed")
            all_ok = False
    
    if all_ok:
        print("\n✓ All dependencies installed!")
    else:
        print("\n✗ Some dependencies missing. Run: pip install -r requirements.txt")
    
    return all_ok


async def test_scraper():
    """Test web scraper dengan URL sederhana"""
    print("\n" + "="*70)
    print("TEST 3: Web Scraper")
    print("="*70)
    
    try:
        from web_scraper import WebScraper
        
        scraper = WebScraper(screenshot_dir="test_screenshots")
        
        print("Testing with example.com...")
        result = await scraper.scrape_url("https://example.com", "Test")
        
        # Check result structure
        required_keys = ['url', 'html', 'screenshot_path', 'network_requests', 
                        'dom_elements', 'javascript_libraries']
        
        for key in required_keys:
            if key in result:
                print(f"✓ Result has '{key}'")
            else:
                print(f"✗ Result missing '{key}'")
                return False
        
        # Check screenshot created
        if result['screenshot_path'] and os.path.exists(result['screenshot_path']):
            print(f"✓ Screenshot created: {result['screenshot_path']}")
        else:
            print("✗ Screenshot not created")
            return False
        
        print("\n✓ Web scraper working correctly!")
        return True
        
    except Exception as e:
        print(f"\n✗ Web scraper test failed: {e}")
        return False


def test_analyzer():
    """Test capability analyzer"""
    print("\n" + "="*70)
    print("TEST 4: Capability Analyzer")
    print("="*70)
    
    try:
        from capability_analyzer import CapabilityAnalyzer
        
        analyzer = CapabilityAnalyzer()
        
        # Create mock data
        mock_data = {
            'url': 'https://test.com',
            'html': '<html><body><canvas id="chart"></canvas></body></html>',
            'dom_elements': {
                'canvas_count': 1,
                'svg_count': 0,
                'table_count': 0,
                'tables': [],
                'chart_containers': [{'tag': 'canvas', 'width': 400, 'height': 300}],
                'inputs': {'select': 0, 'checkbox': 0}
            },
            'javascript_libraries': ['Chart.js'],
            'network_requests': [],
            'websocket_detected': False
        }
        
        print("Analyzing mock data...")
        result = analyzer.analyze_all_capabilities(mock_data)
        
        # Check result structure
        expected_capabilities = [
            'output_grafik_chart',
            'output_data_tabel',
            'output_file',
            'output_dinamis_realtime',
            'output_interaktif',
            'output_berbasis_api'
        ]
        
        for cap in expected_capabilities:
            if cap in result:
                print(f"✓ Capability '{cap}' analyzed")
            else:
                print(f"✗ Capability '{cap}' missing")
                return False
        
        # Check if chart detected
        if result['output_grafik_chart']['supported']:
            print("✓ Chart capability correctly detected!")
        else:
            print("✗ Chart capability not detected (should be detected)")
            return False
        
        print("\n✓ Capability analyzer working correctly!")
        return True
        
    except Exception as e:
        print(f"\n✗ Capability analyzer test failed: {e}")
        return False


def test_pdf_generator():
    """Test PDF generator"""
    print("\n" + "="*70)
    print("TEST 5: PDF Generator")
    print("="*70)
    
    try:
        from pdf_generator import PDFGenerator
        
        generator = PDFGenerator()
        
        # Create mock capabilities
        mock_cap_a = {
            'output_grafik_chart': {
                'supported': True,
                'confidence': 'tinggi',
                'url_count': 1,
                'urls_with_evidence': [{
                    'url': 'https://test-a.com',
                    'screenshot': None,
                    'evidence': ['Ditemukan Chart.js library'],
                    'indicators': {'chart_libraries': ['Chart.js']}
                }]
            },
            'output_data_tabel': {
                'supported': False,
                'confidence': 'rendah',
                'url_count': 0,
                'urls_with_evidence': []
            }
        }
        
        mock_cap_b = {
            'output_grafik_chart': {
                'supported': False,
                'confidence': 'rendah',
                'url_count': 0,
                'urls_with_evidence': []
            },
            'output_data_tabel': {
                'supported': True,
                'confidence': 'tinggi',
                'url_count': 1,
                'urls_with_evidence': [{
                    'url': 'https://test-b.com',
                    'screenshot': None,
                    'evidence': ['Ditemukan DataTables library'],
                    'indicators': {'table_libraries': ['DataTables']}
                }]
            }
        }
        
        # Fill in other capabilities
        for cap in ['output_file', 'output_dinamis_realtime', 
                   'output_interaktif', 'output_berbasis_api']:
            mock_cap_a[cap] = {
                'supported': False,
                'confidence': 'rendah',
                'url_count': 0,
                'urls_with_evidence': []
            }
            mock_cap_b[cap] = {
                'supported': False,
                'confidence': 'rendah',
                'url_count': 0,
                'urls_with_evidence': []
            }
        
        print("Generating test PDF...")
        test_pdf = "test_output/test_report.pdf"
        os.makedirs("test_output", exist_ok=True)
        
        generator.generate_report(
            website_a_name="Test Website A",
            website_b_name="Test Website B",
            website_a_capabilities=mock_cap_a,
            website_b_capabilities=mock_cap_b,
            output_path=test_pdf
        )
        
        if os.path.exists(test_pdf):
            file_size = os.path.getsize(test_pdf)
            print(f"✓ PDF created: {test_pdf} ({file_size} bytes)")
            print("\n✓ PDF generator working correctly!")
            return True
        else:
            print("✗ PDF not created")
            return False
        
    except Exception as e:
        print(f"\n✗ PDF generator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                  WEBSITE COMPARATOR TEST SUITE                    ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    results = []
    
    # Test 1: Imports
    results.append(("Import Modules", test_imports()))
    
    # Test 2: Dependencies
    results.append(("Check Dependencies", test_dependencies()))
    
    # Test 3: Web Scraper (requires internet)
    print("\n⚠ Test 3 requires internet connection and may take 10-15 seconds...")
    confirm = input("Run web scraper test? (y/n): ").strip().lower()
    if confirm == 'y':
        results.append(("Web Scraper", asyncio.run(test_scraper())))
    else:
        print("Skipped web scraper test")
        results.append(("Web Scraper", None))
    
    # Test 4: Analyzer
    results.append(("Capability Analyzer", test_analyzer()))
    
    # Test 5: PDF Generator
    results.append(("PDF Generator", test_pdf_generator()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, result in results:
        if result is True:
            print(f"✓ {test_name}: PASSED")
        elif result is False:
            print(f"✗ {test_name}: FAILED")
        else:
            print(f"⊘ {test_name}: SKIPPED")
    
    passed = sum(1 for _, r in results if r is True)
    failed = sum(1 for _, r in results if r is False)
    skipped = sum(1 for _, r in results if r is None)
    total = len(results)
    
    print("\n" + "="*70)
    print(f"Total: {total} tests | Passed: {passed} | Failed: {failed} | Skipped: {skipped}")
    print("="*70)
    
    if failed == 0:
        print("\n✓ All tests passed! Tool is ready to use.")
    else:
        print("\n✗ Some tests failed. Please fix issues before using the tool.")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

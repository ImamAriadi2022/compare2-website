"""Test scraping dengan ChromeDriver"""
from web_scraper import WebScraper

print("Testing ChromeDriver dengan URL Anda...")
print("=" * 70)

scraper = WebScraper(screenshot_dir="test_screenshots")

# Test dengan salah satu URL
test_url = "https://iot-fakeapi.vercel.app/petengoran/station1"
print(f"\nTesting: {test_url}")

result = scraper.scrape_url(test_url, "Test")

print(f"\n✓ URL: {result['url']}")
print(f"✓ Screenshot: {result.get('screenshot_path', 'N/A')}")
print(f"✓ DOM Elements:")
print(f"  - Canvas: {result['dom_elements'].get('canvas_count', 0)}")
print(f"  - SVG: {result['dom_elements'].get('svg_count', 0)}")
print(f"  - Tables: {result['dom_elements'].get('table_count', 0)}")
print(f"  - Charts detected: {len(result['dom_elements'].get('chart_containers', []))}")
print(f"✓ JS Libraries: {', '.join(result['javascript_libraries']) if result['javascript_libraries'] else 'None detected'}")
print(f"✓ HTML Length: {len(result.get('html', ''))} characters")

print("\n" + "=" * 70)
print("✓ Test selesai! Cek folder test_screenshots/ untuk screenshot.")

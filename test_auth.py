"""Test scraping dengan auth dan interaction"""
from web_scraper import WebScraper

print("Testing ChromeDriver dengan auth dan interaction...")
print("=" * 70)

scraper = WebScraper(screenshot_dir="test_screenshots")

# Test 1: URL dengan download (ada auth)
print("\n[TEST 1] URL dengan auth (download page)")
test_url1 = "https://iot-fakeapi.vercel.app/petengoran/download"
result1 = scraper.scrape_url(test_url1, "IoT-Auth")

print(f"\n✓ URL: {result1['url']}")
print(f"✓ Screenshot: {result1.get('screenshot_path', 'N/A')}")
print(f"✓ DOM Elements:")
print(f"  - Canvas: {result1['dom_elements'].get('canvas_count', 0)}")
print(f"  - SVG: {result1['dom_elements'].get('svg_count', 0)}")
print(f"  - Tables: {result1['dom_elements'].get('table_count', 0)}")
print(f"  - Download buttons: {len(result1['dom_elements'].get('download_elements', []))}")
print(f"✓ HTML Length: {len(result1.get('html', ''))} characters")

# Test 2: Grafana dashboard
print("\n" + "=" * 70)
print("[TEST 2] Grafana dashboard (dengan verification)")
test_url2 = "https://danigrafana.grafana.net/public-dashboards/f007adeb80044a9c9e2dac43ac0ea77a"
result2 = scraper.scrape_url(test_url2, "Grafana")

print(f"\n✓ URL: {result2['url']}")
print(f"✓ Screenshot: {result2.get('screenshot_path', 'N/A')}")
print(f"✓ DOM Elements:")
print(f"  - Canvas: {result2['dom_elements'].get('canvas_count', 0)}")
print(f"  - SVG: {result2['dom_elements'].get('svg_count', 0)}")
print(f"  - Charts detected: {len(result2['dom_elements'].get('chart_containers', []))}")
print(f"✓ JS Libraries: {', '.join(result2['javascript_libraries']) if result2['javascript_libraries'] else 'None'}")
print(f"✓ HTML Length: {len(result2.get('html', ''))} characters")

print("\n" + "=" * 70)
print("✓ Test selesai! Cek folder test_screenshots/")

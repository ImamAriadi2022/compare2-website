"""Simple test - non-headless untuk debug"""
import undetected_chromedriver as uc
import time

print("Testing undetected-chromedriver...")
print("Browser akan terbuka sebentar...")

try:
    # Create driver tanpa headless untuk debug
    options = uc.ChromeOptions()
    # options.add_argument('--headless=new')  # Disable headless untuk test
    
    driver = uc.Chrome(options=options, version_main=None)
    print("✓ ChromeDriver berhasil dibuat")
    
    print("\nMengakses URL...")
    driver.get("https://iot-fakeapi.vercel.app/petengoran/station1")
    print("✓ URL berhasil diakses")
    
    time.sleep(5)  # Wait for page load
    
    # Get page title
    title = driver.title
    print(f"✓ Page Title: {title}")
    
    # Get HTML length
    html = driver.page_source
    print(f"✓ HTML Length: {len(html)} characters")
    
    # Take screenshot
    driver.save_screenshot("test_debug.png")
    print("✓ Screenshot saved: test_debug.png")
    
    driver.quit()
    print("\n✓ Test berhasil!")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

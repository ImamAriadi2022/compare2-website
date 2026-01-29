"""
Web Scraper Module
Menggunakan Selenium ChromeDriver untuk scraping website dinamis dengan JavaScript
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os
from typing import List, Dict, Any
from datetime import datetime
import time
import re
import subprocess
import sys


class WebScraper:
    """Web scraper dengan Selenium ChromeDriver untuk website dinamis"""
    
    def __init__(self, screenshot_dir: str = "screenshots"):
        self.screenshot_dir = screenshot_dir
        os.makedirs(screenshot_dir, exist_ok=True)
    
    def _get_chrome_driver_path(self):
        """Get ChromeDriver path - will download if not exists"""
        try:
            # Check if chromedriver exists in PATH
            result = subprocess.run(['where', 'chromedriver'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                return 'chromedriver'  # Use from PATH
        except:
            pass
        
        # Try to use webdriver-manager
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.core.os_manager import ChromeType
            path = ChromeDriverManager().install()
            return path
        except ImportError:
            print("[INFO] Installing webdriver-manager...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'webdriver-manager'])
            from webdriver_manager.chrome import ChromeDriverManager
            return ChromeDriverManager().install()
    
    def _create_driver(self):
        """Create Chrome WebDriver instance"""
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Try with service (using webdriver-manager)
            driver_path = self._get_chrome_driver_path()
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"[WARNING] Gagal dengan service: {e}")
            # Fallback: try without explicit service (Selenium 4.6+ auto-downloads)
            driver = webdriver.Chrome(options=options)
        
        driver.set_page_load_timeout(30)
        return driver
        
    def scrape_url(self, url: str, website_name: str) -> Dict[str, Any]:
        """
        Scrape satu URL dan kumpulkan semua data teknis
        
        Returns:
            Dict berisi:
            - url: URL yang diakses
            - html: HTML content
            - screenshot_path: Path ke screenshot
            - dom_elements: Elemen DOM penting
            - javascript_libraries: Library JS yang terdeteksi
        """
        driver = None
        try:
            print(f"[INFO] Mengakses {url}")
            
            # Create driver
            driver = self._create_driver()
            
            # Navigate to URL
            print(f"[INFO] Loading page...")
            driver.get(url)
            
            # Wait for page to load - wait for body element
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print(f"[INFO] Page loaded, checking for auth/captcha...")
            
            # Handle auth untuk halaman download (admin/admin123)
            if 'download' in url.lower():
                self._handle_auth(driver, username='admin', password='admin123')
            
            # Handle Grafana CAPTCHA / verification
            if 'grafana' in url.lower():
                self._handle_grafana_verification(driver)
            
            # Additional wait for dynamic content
            print(f"[INFO] Waiting for JavaScript to render...")
            time.sleep(8)  # Increased wait time for JS-heavy pages
            
            # More aggressive scrolling and interaction
            print(f"[INFO] Scrolling and interacting...")
            self._scroll_and_interact(driver)
            
            # Get HTML content after JavaScript execution
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            print(f"[INFO] HTML captured: {len(html_content)} characters")
            
            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_url = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')[:50]
            screenshot_filename = f"{website_name}_{safe_url}_{timestamp}.png"
            screenshot_path = os.path.join(self.screenshot_dir, screenshot_filename)
            driver.save_screenshot(screenshot_path)
            print(f"[INFO] Screenshot saved: {screenshot_path}")
            
            # Analisis DOM
            dom_analysis = self._analyze_dom(soup, html_content, driver)
            
            # Deteksi JavaScript libraries
            js_libraries = self._detect_js_libraries(html_content, soup, driver)
            
            # Deteksi WebSocket
            websocket_detected = self._detect_websocket(html_content)
            
            result = {
                'url': url,
                'website_name': website_name,
                'html': html_content,
                'screenshot_path': screenshot_path,
                'network_requests': [],  # Could be enhanced with browser logs
                'console_logs': [],
                'dom_elements': dom_analysis,
                'javascript_libraries': js_libraries,
                'websocket_detected': websocket_detected,
                'timestamp': timestamp
            }
            
            print(f"[SUCCESS] Selesai scraping {url}")
            return result
            
        except Exception as e:
            print(f"[ERROR] Gagal scraping {url}: {str(e)}")
            return {
                'url': url,
                'website_name': website_name,
                'error': str(e),
                'screenshot_path': None,
                'network_requests': [],
                'console_logs': [],
                'dom_elements': {},
                'javascript_libraries': [],
                'websocket_detected': False
            }
        finally:
            if driver:
                driver.quit()
    
    def _handle_auth(self, driver, username='admin', password='admin123'):
        """Handle basic auth atau login form"""
        try:
            # Check if there's a login form
            time.sleep(2)
            
            # Try to find username/password fields
            username_selectors = [
                "input[name='username']", "input[name='user']", "input[name='email']",
                "input[type='text']", "input[id*='user']", "input[id*='login']"
            ]
            password_selectors = [
                "input[name='password']", "input[type='password']", 
                "input[id*='pass']", "input[id*='pwd']"
            ]
            
            username_field = None
            password_field = None
            
            # Find username field
            for selector in username_selectors:
                try:
                    username_field = driver.find_element(By.CSS_SELECTOR, selector)
                    if username_field.is_displayed():
                        break
                except:
                    continue
            
            # Find password field
            for selector in password_selectors:
                try:
                    password_field = driver.find_element(By.CSS_SELECTOR, selector)
                    if password_field.is_displayed():
                        break
                except:
                    continue
            
            if username_field and password_field:
                print(f"[INFO] Login form detected, logging in...")
                username_field.clear()
                username_field.send_keys(username)
                time.sleep(0.5)
                
                password_field.clear()
                password_field.send_keys(password)
                time.sleep(0.5)
                
                # Find and click submit button
                submit_selectors = [
                    "button[type='submit']", "input[type='submit']",
                    "button:contains('Login')", "button:contains('Sign')",
                    "button", "input[value='Login']"
                ]
                
                for selector in submit_selectors:
                    try:
                        submit_btn = driver.find_element(By.CSS_SELECTOR, selector)
                        if submit_btn.is_displayed():
                            submit_btn.click()
                            print(f"[INFO] Clicked login button, waiting...")
                            time.sleep(3)
                            break
                    except:
                        continue
                
                print(f"[SUCCESS] Login attempted")
        except Exception as e:
            print(f"[INFO] No login form found or already logged in: {e}")
    
    def _handle_grafana_verification(self, driver):
        """Handle Grafana CAPTCHA/verification"""
        try:
            print(f"[INFO] Checking for Grafana verification...")
            time.sleep(3)
            
            # Look for iframe with CAPTCHA
            try:
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                for iframe in iframes:
                    if 'recaptcha' in iframe.get_attribute('src').lower() or 'captcha' in iframe.get_attribute('src').lower():
                        print(f"[INFO] CAPTCHA detected, waiting longer...")
                        time.sleep(10)
                        break
            except:
                pass
            
            # Try to find and click any "verify" or "I'm not a robot" buttons
            verify_selectors = [
                "//button[contains(text(), 'Verify')]",
                "//button[contains(text(), 'verify')]",
                "//div[@class='recaptcha-checkbox-border']",
                "//span[contains(text(), 'not a robot')]"
            ]
            
            for selector in verify_selectors:
                try:
                    element = driver.find_element(By.XPATH, selector)
                    if element.is_displayed():
                        print(f"[INFO] Found verification element, clicking...")
                        element.click()
                        time.sleep(5)
                        break
                except:
                    continue
            
            # Wait longer for Grafana to load
            print(f"[INFO] Waiting for Grafana dashboard to fully load...")
            time.sleep(10)
            
        except Exception as e:
            print(f"[INFO] Grafana verification handling: {e}")
    
    def _scroll_and_interact(self, driver):
        """Aggressive scrolling and interaction to trigger all content"""
        try:
            # Get page height
            page_height = driver.execute_script("return document.body.scrollHeight")
            
            # Scroll down in multiple steps
            scroll_steps = 10
            for i in range(scroll_steps):
                scroll_position = (page_height / scroll_steps) * (i + 1)
                driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(0.5)
            
            # Scroll back to top
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Scroll to bottom again
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Try to click any visible buttons (for interactive content)
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                clickable_count = 0
                for button in buttons[:5]:  # Limit to first 5 buttons
                    try:
                        if button.is_displayed() and button.is_enabled():
                            # Skip buttons with certain texts
                            btn_text = button.text.lower()
                            if any(skip in btn_text for skip in ['delete', 'remove', 'logout', 'close']):
                                continue
                            
                            button.click()
                            clickable_count += 1
                            time.sleep(1)
                    except:
                        continue
                
                if clickable_count > 0:
                    print(f"[INFO] Clicked {clickable_count} interactive elements")
            except:
                pass
            
            # Hover over elements to trigger tooltips/popovers
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                hoverable_elements = driver.find_elements(By.CSS_SELECTOR, "canvas, svg, .chart, [data-tooltip]")
                for element in hoverable_elements[:3]:
                    try:
                        ActionChains(driver).move_to_element(element).perform()
                        time.sleep(0.5)
                    except:
                        continue
            except:
                pass
            
            # Scroll back to top for final screenshot
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
        except Exception as e:
            print(f"[INFO] Scroll and interact: {e}")
    
    def _analyze_dom(self, soup: BeautifulSoup, html_content: str, driver=None) -> Dict[str, Any]:
        """Analisis elemen DOM yang relevan untuk capability detection"""
        
        result = {
            'canvas_count': len(soup.find_all('canvas')),
            'svg_count': len(soup.find_all('svg')),
            'table_count': len(soup.find_all('table')),
            'chart_containers': [],
            'tables': [],
            'download_elements': [],
            'inputs': {
                'select': len(soup.find_all('select')),
                'checkbox': len(soup.find_all('input', {'type': 'checkbox'})),
                'radio': len(soup.find_all('input', {'type': 'radio'})),
                'range': len(soup.find_all('input', {'type': 'range'})),
                'date': len(soup.find_all('input', {'type': 'date'}))
            },
            'form_count': len(soup.find_all('form'))
        }
        
        # Deteksi chart containers (canvas dan svg)
        for canvas in soup.find_all('canvas')[:10]:  # Limit 10
            parent = canvas.parent
            result['chart_containers'].append({
                'tag': 'canvas',
                'id': canvas.get('id', ''),
                'class': ' '.join(canvas.get('class', [])),
                'parent_class': ' '.join(parent.get('class', [])) if parent else '',
                'width': canvas.get('width', ''),
                'height': canvas.get('height', '')
            })
        
        for svg in soup.find_all('svg')[:10]:  # Limit 10
            result['chart_containers'].append({
                'tag': 'svg',
                'id': svg.get('id', ''),
                'class': ' '.join(svg.get('class', [])),
                'width': svg.get('width', ''),
                'height': svg.get('height', '')
            })
        
        # Deteksi tables dengan data
        for table in soup.find_all('table')[:20]:  # Limit 20
            rows = table.find_all('tr')
            if len(rows) > 1:
                result['tables'].append({
                    'rows': len(rows),
                    'cols': len(table.find_all(['th', 'td'])),
                    'class': ' '.join(table.get('class', [])),
                    'id': table.get('id', ''),
                    'has_header': len(table.find_all(['thead', 'th'])) > 0
                })
        
        # Deteksi download elements
        download_selectors = [
            soup.find_all('a', href=re.compile(r'download', re.I)),
            soup.find_all('a', attrs={'download': True}),
            soup.find_all('button', attrs={'data-download': True}),
            soup.find_all(text=re.compile(r'(download|unduh|export|ekspor)', re.I))
        ]
        
        for selector_result in download_selectors:
            if isinstance(selector_result, list):
                for el in selector_result[:10]:  # Limit 10
                    if hasattr(el, 'name'):
                        result['download_elements'].append({
                            'tag': el.name,
                            'text': el.get_text()[:50].strip(),
                            'href': el.get('href', el.get('data-url', '')),
                            'download_attr': el.has_attr('download')
                        })
        
        return result
    
    def _detect_js_libraries(self, html_content: str, soup: BeautifulSoup, driver=None) -> List[str]:
        """Deteksi JavaScript libraries dari kode HTML dan script tags"""
        detected = []
        
        # Pattern matching di HTML content
        library_patterns = {
            'Chart.js': r'chart\.js|chartjs',
            'Highcharts': r'highcharts',
            'ApexCharts': r'apexcharts',
            'ECharts': r'echarts',
            'D3.js': r'd3\.js|d3\.min\.js',
            'Plotly': r'plotly',
            'Google Charts': r'google.*charts|charts\.load',
            'DataTables': r'datatables|dataTables',
            'AG Grid': r'ag-grid',
            'React': r'react\.js|react\.min\.js|react-dom',
            'Vue.js': r'vue\.js|vue\.min\.js',
            'Angular': r'angular\.js|angular\.min\.js',
            'jQuery': r'jquery\.js|jquery\.min\.js',
            'Axios': r'axios\.js|axios\.min\.js'
        }
        
        for lib_name, pattern in library_patterns.items():
            if re.search(pattern, html_content, re.IGNORECASE):
                detected.append(lib_name)
        
        # Check script src attributes
        for script in soup.find_all('script', src=True):
            src = script['src'].lower()
            for lib_name, pattern in library_patterns.items():
                if re.search(pattern, src, re.IGNORECASE) and lib_name not in detected:
                    detected.append(lib_name)
        
        return detected
    
    def _detect_websocket(self, html_content: str) -> bool:
        """Deteksi penggunaan WebSocket dari kode HTML"""
        websocket_patterns = [
            r'new WebSocket\(',
            r'socket\.io',
            r'ws://',
            r'wss://',
            r'WebSocketClient',
            r'\.on\(["\']connect["\']',
            r'\.emit\(',
            r'SignalR'
        ]
        
        for pattern in websocket_patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return True
        
        return False
    
    def scrape_multiple_urls(self, urls: List[str], website_name: str) -> List[Dict[str, Any]]:
        """Scrape multiple URLs secara sequential"""
        results = []
        for url in urls:
            result = self.scrape_url(url, website_name)
            results.append(result)
            time.sleep(2)  # Delay antar request
        return results

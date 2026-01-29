"""
Web Scraper Module
Menggunakan Playwright untuk render halaman dan mengumpulkan data teknis
"""

import asyncio
import json
from typing import List, Dict, Any
from playwright.async_api import async_playwright, Page
import os
from datetime import datetime


class WebScraper:
    """Browser headless untuk scraping dan analisis halaman web"""
    
    def __init__(self, screenshot_dir: str = "screenshots"):
        self.screenshot_dir = screenshot_dir
        os.makedirs(screenshot_dir, exist_ok=True)
        
    async def scrape_url(self, url: str, website_name: str) -> Dict[str, Any]:
        """
        Scrape satu URL dan kumpulkan semua data teknis
        
        Returns:
            Dict berisi:
            - url: URL yang diakses
            - html: HTML content
            - screenshot_path: Path ke screenshot
            - network_requests: List request network
            - console_logs: Console logs dari browser
            - dom_elements: Elemen DOM penting
            - javascript_libraries: Library JS yang terdeteksi
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()
            
            # Storage untuk monitoring
            network_requests = []
            console_logs = []
            websocket_detected = False
            
            # Monitor network activity
            async def handle_request(request):
                network_requests.append({
                    'url': request.url,
                    'method': request.method,
                    'resource_type': request.resource_type,
                    'headers': dict(request.headers)
                })
            
            async def handle_response(response):
                if response.url in [req['url'] for req in network_requests]:
                    for req in network_requests:
                        if req['url'] == response.url:
                            req['status'] = response.status
                            req['content_type'] = response.headers.get('content-type', '')
                            try:
                                # Coba simpan body untuk response API
                                if 'json' in req.get('content_type', '').lower():
                                    req['response_body'] = await response.text()
                            except:
                                pass
            
            # Monitor console logs
            page.on('console', lambda msg: console_logs.append({
                'type': msg.type,
                'text': msg.text
            }))
            
            # Monitor WebSocket
            page.on('websocket', lambda ws: websocket_detected or setattr(locals(), 'websocket_detected', True))
            
            page.on('request', handle_request)
            page.on('response', handle_response)
            
            try:
                # Navigate ke halaman
                print(f"[INFO] Mengakses {url}")
                await page.goto(url, wait_until='networkidle', timeout=30000)
                
                # Wait for dynamic content
                await asyncio.sleep(3)
                
                # Scroll untuk trigger lazy loading
                await page.evaluate("""
                    window.scrollTo(0, document.body.scrollHeight / 2);
                """)
                await asyncio.sleep(1)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(2)
                
                # Kembali ke atas
                await page.evaluate("window.scrollTo(0, 0);")
                await asyncio.sleep(1)
                
                # Ambil HTML content
                html_content = await page.content()
                
                # Ambil screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_url = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')[:50]
                screenshot_filename = f"{website_name}_{safe_url}_{timestamp}.png"
                screenshot_path = os.path.join(self.screenshot_dir, screenshot_filename)
                await page.screenshot(path=screenshot_path, full_page=True)
                
                # Analisis DOM
                dom_analysis = await self._analyze_dom(page)
                
                # Deteksi JavaScript libraries
                js_libraries = await self._detect_js_libraries(page)
                
                # Cek WebSocket di window
                has_websocket = await page.evaluate("""
                    () => {
                        return typeof WebSocket !== 'undefined' && 
                               (window.ws !== undefined || 
                                document.querySelectorAll('[data-websocket]').length > 0);
                    }
                """)
                
                websocket_detected = websocket_detected or has_websocket
                
                result = {
                    'url': url,
                    'website_name': website_name,
                    'html': html_content,
                    'screenshot_path': screenshot_path,
                    'network_requests': network_requests,
                    'console_logs': console_logs,
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
                await browser.close()
    
    async def _analyze_dom(self, page: Page) -> Dict[str, Any]:
        """Analisis elemen DOM yang relevan untuk capability detection"""
        
        analysis = await page.evaluate("""
            () => {
                const result = {
                    canvas_count: document.querySelectorAll('canvas').length,
                    svg_count: document.querySelectorAll('svg').length,
                    table_count: document.querySelectorAll('table').length,
                    
                    // Chart elements
                    chart_containers: [],
                    
                    // Table elements
                    tables: [],
                    
                    // Download links/buttons
                    download_elements: [],
                    
                    // Interactive inputs
                    inputs: {
                        select: document.querySelectorAll('select').length,
                        checkbox: document.querySelectorAll('input[type="checkbox"]').length,
                        radio: document.querySelectorAll('input[type="radio"]').length,
                        range: document.querySelectorAll('input[type="range"]').length,
                        date: document.querySelectorAll('input[type="date"]').length
                    },
                    
                    // Form elements
                    form_count: document.querySelectorAll('form').length
                };
                
                // Deteksi chart containers
                document.querySelectorAll('canvas, svg').forEach(el => {
                    const parent = el.parentElement;
                    result.chart_containers.push({
                        tag: el.tagName.toLowerCase(),
                        id: el.id,
                        class: el.className,
                        parent_class: parent ? parent.className : '',
                        width: el.width || el.clientWidth,
                        height: el.height || el.clientHeight
                    });
                });
                
                // Deteksi tables dengan data
                document.querySelectorAll('table').forEach(table => {
                    const rows = table.querySelectorAll('tr').length;
                    const cols = table.querySelectorAll('th, td').length;
                    if (rows > 1 && cols > 1) {
                        result.tables.push({
                            rows: rows,
                            cols: cols,
                            class: table.className,
                            id: table.id,
                            has_header: table.querySelectorAll('thead, th').length > 0
                        });
                    }
                });
                
                // Deteksi download elements
                document.querySelectorAll('a[href*="download"], a[download], button[data-download]').forEach(el => {
                    result.download_elements.push({
                        tag: el.tagName.toLowerCase(),
                        text: el.textContent.trim().substring(0, 50),
                        href: el.href || el.getAttribute('data-url') || '',
                        download_attr: el.hasAttribute('download')
                    });
                });
                
                return result;
            }
        """)
        
        return analysis
    
    async def _detect_js_libraries(self, page: Page) -> List[str]:
        """Deteksi JavaScript libraries yang digunakan"""
        
        libraries = await page.evaluate("""
            () => {
                const detected = [];
                
                // Chart libraries
                if (typeof Chart !== 'undefined') detected.push('Chart.js');
                if (typeof Highcharts !== 'undefined') detected.push('Highcharts');
                if (typeof ApexCharts !== 'undefined') detected.push('ApexCharts');
                if (typeof echarts !== 'undefined') detected.push('ECharts');
                if (typeof d3 !== 'undefined') detected.push('D3.js');
                if (typeof Plotly !== 'undefined') detected.push('Plotly');
                if (typeof google !== 'undefined' && google.charts) detected.push('Google Charts');
                
                // Table/Grid libraries
                if (typeof $ !== 'undefined' && $.fn && $.fn.DataTable) detected.push('DataTables');
                if (typeof agGrid !== 'undefined') detected.push('AG Grid');
                if (window.GridStack) detected.push('GridStack');
                
                // Framework detection
                if (typeof React !== 'undefined') detected.push('React');
                if (typeof Vue !== 'undefined') detected.push('Vue.js');
                if (typeof angular !== 'undefined') detected.push('Angular');
                
                // Utility libraries
                if (typeof axios !== 'undefined') detected.push('Axios');
                if (typeof $ !== 'undefined' && $.fn && $.fn.jquery) detected.push('jQuery');
                
                return detected;
            }
        """)
        
        return libraries
    
    async def scrape_multiple_urls(self, urls: List[str], website_name: str) -> List[Dict[str, Any]]:
        """Scrape multiple URLs secara sequential"""
        results = []
        for url in urls:
            result = await self.scrape_url(url, website_name)
            results.append(result)
            await asyncio.sleep(2)  # Delay antar request
        return results

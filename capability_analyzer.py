"""
Capability Analyzer Module
Menganalisis data scraping untuk mendeteksi output capability
"""

from typing import Dict, List, Any
from bs4 import BeautifulSoup
import re


class CapabilityAnalyzer:
    """Analyzer untuk mendeteksi output capability dari data scraping"""
    
    CAPABILITIES = [
        'output_grafik_chart',
        'output_data_tabel',
        'output_file',
        'output_dinamis_realtime',
        'output_interaktif',
        'output_berbasis_api'
    ]
    
    def __init__(self):
        self.capability_names = {
            'output_grafik_chart': 'Output Grafik / Chart',
            'output_data_tabel': 'Output Data Tabel',
            'output_file': 'Output File (CSV, Excel, PDF, Gambar)',
            'output_dinamis_realtime': 'Output Dinamis / Real-time',
            'output_interaktif': 'Output Interaktif',
            'output_berbasis_api': 'Output Berbasis API'
        }
    
    def analyze_all_capabilities(self, scrape_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisis semua capability dari data scraping
        
        Returns:
            Dict dengan key capability dan value berisi:
            - supported: bool
            - confidence: 'tinggi' | 'sedang' | 'rendah'
            - evidence: List[str] bukti teknis
            - indicators: Dict detail teknis
        """
        
        if 'error' in scrape_data:
            return self._empty_capabilities()
        
        results = {}
        
        # Analisis setiap capability
        results['output_grafik_chart'] = self._analyze_chart_output(scrape_data)
        results['output_data_tabel'] = self._analyze_table_output(scrape_data)
        results['output_file'] = self._analyze_file_output(scrape_data)
        results['output_dinamis_realtime'] = self._analyze_realtime_output(scrape_data)
        results['output_interaktif'] = self._analyze_interactive_output(scrape_data)
        results['output_berbasis_api'] = self._analyze_api_output(scrape_data)
        
        return results
    
    def _empty_capabilities(self) -> Dict[str, Any]:
        """Return empty capabilities untuk error case"""
        return {
            cap: {
                'supported': False,
                'confidence': 'rendah',
                'evidence': [],
                'indicators': {}
            }
            for cap in self.CAPABILITIES
        }
    
    def _analyze_chart_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Deteksi Output Grafik / Chart"""
        
        evidence = []
        indicators = {}
        confidence = 'rendah'
        
        dom = data.get('dom_elements', {})
        js_libs = data.get('javascript_libraries', [])
        
        # Cek canvas dan SVG
        canvas_count = dom.get('canvas_count', 0)
        svg_count = dom.get('svg_count', 0)
        chart_containers = dom.get('chart_containers', [])
        
        if canvas_count > 0:
            evidence.append(f"Ditemukan {canvas_count} elemen <canvas>")
            indicators['canvas_count'] = canvas_count
        
        if svg_count > 0:
            evidence.append(f"Ditemukan {svg_count} elemen <svg>")
            indicators['svg_count'] = svg_count
        
        # Cek chart libraries
        chart_libs = [lib for lib in js_libs if any(x in lib.lower() for x in 
                     ['chart', 'd3', 'highchart', 'echarts', 'apex', 'plotly', 'google charts'])]
        
        if chart_libs:
            evidence.append(f"Terdeteksi library chart: {', '.join(chart_libs)}")
            indicators['chart_libraries'] = chart_libs
            confidence = 'tinggi'
        
        # Analisis chart containers
        if chart_containers:
            large_charts = [c for c in chart_containers if c.get('width', 0) > 200 and c.get('height', 0) > 200]
            if large_charts:
                evidence.append(f"Ditemukan {len(large_charts)} chart dengan dimensi signifikan")
                indicators['large_charts'] = len(large_charts)
                if confidence == 'rendah':
                    confidence = 'sedang'
        
        # Cek HTML untuk class/id chart
        html = data.get('html', '')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            chart_elements = soup.find_all(class_=re.compile(r'chart|graph|plot|visualization', re.I))
            if chart_elements:
                evidence.append(f"Ditemukan {len(chart_elements)} elemen dengan class chart/graph")
                indicators['chart_css_classes'] = len(chart_elements)
                if confidence == 'rendah':
                    confidence = 'sedang'
        
        supported = len(evidence) > 0 and (canvas_count > 0 or svg_count > 0 or len(chart_libs) > 0)
        
        return {
            'supported': supported,
            'confidence': confidence if supported else 'rendah',
            'evidence': evidence,
            'indicators': indicators
        }
    
    def _analyze_table_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Deteksi Output Data Tabel"""
        
        evidence = []
        indicators = {}
        confidence = 'rendah'
        
        dom = data.get('dom_elements', {})
        js_libs = data.get('javascript_libraries', [])
        
        # Cek tabel dari DOM analysis
        tables = dom.get('tables', [])
        table_count = dom.get('table_count', 0)
        
        if tables:
            # Filter tabel dengan data signifikan
            significant_tables = [t for t in tables if t.get('rows', 0) > 2 and t.get('cols', 0) > 2]
            
            if significant_tables:
                evidence.append(f"Ditemukan {len(significant_tables)} tabel dengan data signifikan")
                indicators['significant_tables'] = len(significant_tables)
                confidence = 'sedang'
                
                # Cek header
                tables_with_header = [t for t in significant_tables if t.get('has_header', False)]
                if tables_with_header:
                    evidence.append(f"{len(tables_with_header)} tabel memiliki header")
                    indicators['tables_with_header'] = len(tables_with_header)
                    confidence = 'tinggi'
        
        # Cek table/grid libraries
        table_libs = [lib for lib in js_libs if any(x in lib.lower() for x in 
                     ['datatable', 'ag grid', 'gridstack'])]
        
        if table_libs:
            evidence.append(f"Terdeteksi library tabel/grid: {', '.join(table_libs)}")
            indicators['table_libraries'] = table_libs
            confidence = 'tinggi'
        
        # Cek class CSS untuk grid/table
        html = data.get('html', '')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            grid_elements = soup.find_all(class_=re.compile(r'grid|datatable|table-responsive', re.I))
            if grid_elements and len(grid_elements) > 0:
                evidence.append(f"Ditemukan {len(grid_elements)} elemen dengan class grid/datatable")
                indicators['grid_css_classes'] = len(grid_elements)
        
        supported = len(evidence) > 0 and (len(tables) > 0 or len(table_libs) > 0)
        
        return {
            'supported': supported,
            'confidence': confidence if supported else 'rendah',
            'evidence': evidence,
            'indicators': indicators
        }
    
    def _analyze_file_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Deteksi Output File (Download)"""
        
        evidence = []
        indicators = {}
        confidence = 'rendah'
        
        dom = data.get('dom_elements', {})
        network = data.get('network_requests', [])
        
        # Cek download elements dari DOM
        download_elements = dom.get('download_elements', [])
        
        if download_elements:
            evidence.append(f"Ditemukan {len(download_elements)} elemen download")
            indicators['download_elements'] = len(download_elements)
            
            # Group by file type
            file_types = set()
            for elem in download_elements:
                href = elem.get('href', '').lower()
                if '.csv' in href or 'csv' in elem.get('text', '').lower():
                    file_types.add('CSV')
                if '.xls' in href or 'excel' in elem.get('text', '').lower():
                    file_types.add('Excel')
                if '.pdf' in href or 'pdf' in elem.get('text', '').lower():
                    file_types.add('PDF')
                if any(ext in href for ext in ['.jpg', '.png', '.gif', '.svg']):
                    file_types.add('Image')
            
            if file_types:
                evidence.append(f"Jenis file: {', '.join(file_types)}")
                indicators['file_types'] = list(file_types)
                confidence = 'tinggi'
        
        # Cek network requests untuk download
        download_requests = []
        for req in network:
            content_type = req.get('content_type', '').lower()
            url = req.get('url', '').lower()
            
            # Cek content-type yang indicate file download
            if any(x in content_type for x in [
                'application/csv',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/pdf',
                'application/octet-stream',
                'image/'
            ]):
                download_requests.append(req)
            
            # Cek URL pattern
            elif any(x in url for x in ['download', 'export', '.csv', '.xlsx', '.pdf']):
                download_requests.append(req)
        
        if download_requests:
            evidence.append(f"Ditemukan {len(download_requests)} request download di network")
            indicators['download_requests'] = len(download_requests)
            if confidence == 'rendah':
                confidence = 'sedang'
        
        supported = len(evidence) > 0
        
        return {
            'supported': supported,
            'confidence': confidence if supported else 'rendah',
            'evidence': evidence,
            'indicators': indicators
        }
    
    def _analyze_realtime_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Deteksi Output Dinamis / Real-time"""
        
        evidence = []
        indicators = {}
        confidence = 'rendah'
        
        websocket = data.get('websocket_detected', False)
        network = data.get('network_requests', [])
        
        # Cek WebSocket
        if websocket:
            evidence.append("WebSocket terdeteksi")
            indicators['websocket'] = True
            confidence = 'tinggi'
        
        # Cek SSE (Server-Sent Events)
        sse_requests = [req for req in network if 'text/event-stream' in req.get('content_type', '')]
        if sse_requests:
            evidence.append(f"Ditemukan {len(sse_requests)} koneksi Server-Sent Events")
            indicators['sse_connections'] = len(sse_requests)
            confidence = 'tinggi'
        
        # Cek polling (multiple requests ke endpoint yang sama)
        url_counts = {}
        for req in network:
            if req.get('resource_type') in ['xhr', 'fetch']:
                url = req.get('url', '')
                url_counts[url] = url_counts.get(url, 0) + 1
        
        polling_urls = {url: count for url, count in url_counts.items() if count >= 3}
        if polling_urls:
            evidence.append(f"Terdeteksi {len(polling_urls)} endpoint dengan polling pattern")
            indicators['polling_endpoints'] = len(polling_urls)
            if confidence == 'rendah':
                confidence = 'sedang'
        
        # Cek dari console logs
        console = data.get('console_logs', [])
        realtime_keywords = ['websocket', 'socket.io', 'sse', 'realtime', 'live update']
        realtime_logs = [log for log in console if any(kw in log.get('text', '').lower() for kw in realtime_keywords)]
        
        if realtime_logs:
            evidence.append(f"Ditemukan {len(realtime_logs)} log terkait real-time")
            indicators['realtime_logs'] = len(realtime_logs)
        
        supported = len(evidence) > 0
        
        return {
            'supported': supported,
            'confidence': confidence if supported else 'rendah',
            'evidence': evidence,
            'indicators': indicators
        }
    
    def _analyze_interactive_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Deteksi Output Interaktif"""
        
        evidence = []
        indicators = {}
        confidence = 'rendah'
        
        dom = data.get('dom_elements', {})
        inputs = dom.get('inputs', {})
        
        # Hitung total interactive inputs
        total_inputs = sum(inputs.values())
        
        if total_inputs > 0:
            evidence.append(f"Ditemukan {total_inputs} elemen input interaktif")
            indicators['total_inputs'] = total_inputs
            indicators['input_breakdown'] = inputs
            
            # Jika ada berbagai jenis input, lebih mungkin interaktif
            input_types = [k for k, v in inputs.items() if v > 0]
            if len(input_types) >= 2:
                evidence.append(f"Beragam tipe input: {', '.join(input_types)}")
                confidence = 'sedang'
        
        # Cek form elements
        form_count = dom.get('form_count', 0)
        if form_count > 0:
            evidence.append(f"Ditemukan {form_count} form")
            indicators['form_count'] = form_count
        
        # Cek event listeners dari network (XHR/fetch setelah interaction)
        network = data.get('network_requests', [])
        xhr_requests = [req for req in network if req.get('resource_type') in ['xhr', 'fetch']]
        
        if xhr_requests and total_inputs > 0:
            evidence.append(f"Ditemukan {len(xhr_requests)} XHR/Fetch request (kemungkinan dari interaksi)")
            indicators['xhr_requests'] = len(xhr_requests)
            confidence = 'tinggi'
        
        # Cek dari HTML untuk event handlers
        html = data.get('html', '')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            interactive_elements = soup.find_all(attrs={'onclick': True})
            interactive_elements += soup.find_all(attrs={'onchange': True})
            
            if interactive_elements:
                evidence.append(f"Ditemukan {len(interactive_elements)} elemen dengan event handler")
                indicators['event_handlers'] = len(interactive_elements)
                if confidence == 'rendah':
                    confidence = 'sedang'
        
        supported = len(evidence) > 0 and total_inputs > 0
        
        return {
            'supported': supported,
            'confidence': confidence if supported else 'rendah',
            'evidence': evidence,
            'indicators': indicators
        }
    
    def _analyze_api_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Deteksi Output Berbasis API"""
        
        evidence = []
        indicators = {}
        confidence = 'rendah'
        
        network = data.get('network_requests', [])
        
        # Filter API requests
        api_requests = []
        for req in network:
            resource_type = req.get('resource_type', '')
            content_type = req.get('content_type', '')
            url = req.get('url', '')
            
            # Cek JSON API
            if 'json' in content_type.lower():
                api_requests.append(req)
            # Cek XHR/Fetch
            elif resource_type in ['xhr', 'fetch']:
                api_requests.append(req)
            # Cek URL pattern API
            elif any(x in url.lower() for x in ['/api/', '/rest/', '/graphql', '/v1/', '/v2/']):
                api_requests.append(req)
        
        if api_requests:
            evidence.append(f"Ditemukan {len(api_requests)} API request")
            indicators['api_request_count'] = len(api_requests)
            
            # Count successful responses
            successful = [req for req in api_requests if req.get('status', 0) == 200]
            if successful:
                evidence.append(f"{len(successful)} API request berhasil (200 OK)")
                indicators['successful_api_requests'] = len(successful)
                confidence = 'tinggi'
            
            # Check for JSON responses with data
            json_responses = []
            for req in api_requests:
                if 'response_body' in req:
                    try:
                        import json
                        body = json.loads(req['response_body'])
                        if isinstance(body, (dict, list)) and body:
                            json_responses.append(req)
                    except:
                        pass
            
            if json_responses:
                evidence.append(f"{len(json_responses)} response JSON dengan data")
                indicators['json_responses_with_data'] = len(json_responses)
                confidence = 'tinggi'
        
        # Cek dari JavaScript libraries
        js_libs = data.get('javascript_libraries', [])
        api_libs = [lib for lib in js_libs if any(x in lib.lower() for x in ['axios', 'fetch'])]
        
        if api_libs:
            evidence.append(f"Terdeteksi library HTTP: {', '.join(api_libs)}")
            indicators['http_libraries'] = api_libs
        
        supported = len(api_requests) > 0
        
        return {
            'supported': supported,
            'confidence': confidence if supported else 'rendah',
            'evidence': evidence,
            'indicators': indicators
        }
    
    def aggregate_website_capabilities(self, all_scrape_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Agregasi capability dari multiple URLs untuk satu website
        
        Returns:
            Dict dengan key capability dan agregasi dari semua URL
        """
        
        aggregated = {}
        
        for capability in self.CAPABILITIES:
            # Collect all analyses for this capability
            capability_results = []
            urls_with_evidence = []
            
            for result in all_scrape_results:
                analysis = self.analyze_all_capabilities(result)
                cap_data = analysis.get(capability, {})
                
                if cap_data.get('supported', False):
                    capability_results.append(cap_data)
                    urls_with_evidence.append({
                        'url': result.get('url'),
                        'screenshot': result.get('screenshot_path'),
                        'evidence': cap_data.get('evidence', []),
                        'indicators': cap_data.get('indicators', {}),
                        'confidence': cap_data.get('confidence', 'rendah')
                    })
            
            # Determine overall support
            supported = len(capability_results) > 0
            
            # Determine overall confidence
            if supported:
                confidences = [r.get('confidence', 'rendah') for r in capability_results]
                if 'tinggi' in confidences:
                    overall_confidence = 'tinggi'
                elif 'sedang' in confidences:
                    overall_confidence = 'sedang'
                else:
                    overall_confidence = 'rendah'
            else:
                overall_confidence = 'rendah'
            
            aggregated[capability] = {
                'supported': supported,
                'confidence': overall_confidence,
                'url_count': len(urls_with_evidence),
                'urls_with_evidence': urls_with_evidence,
                'total_urls_analyzed': len(all_scrape_results)
            }
        
        return aggregated

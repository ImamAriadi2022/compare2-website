# Dokumentasi Teknis

## Arsitektur Sistem

### Overview
Tool ini terdiri dari 4 modul utama yang bekerja secara sequential:

```
┌─────────────────┐
│  User Input     │
│  (URLs)         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Web Scraper    │  ← Playwright browser headless
│                 │    - Render halaman
│                 │    - Monitor network
│                 │    - Ambil screenshot
│                 │    - Analisis DOM
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Capability     │  ← Analisis teknis
│  Analyzer       │    - Deteksi elemen
│                 │    - Verifikasi bukti
│                 │    - Agregasi hasil
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PDF Generator  │  ← ReportLab
│                 │    - Format laporan
│                 │    - Embed screenshot
│                 │    - Generate PDF
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PDF Output     │
└─────────────────┘
```

---

## Modul Details

### 1. Web Scraper (`web_scraper.py`)

**Technology Stack:**
- Playwright (Browser automation)
- BeautifulSoup (HTML parsing)

**Key Functions:**
- `scrape_url()`: Scrape single URL
- `scrape_multiple_urls()`: Scrape multiple URLs sequentially
- `_analyze_dom()`: Analisis DOM elements
- `_detect_js_libraries()`: Deteksi JavaScript libraries

**Data Collected:**
```python
{
    'url': str,
    'website_name': str,
    'html': str,  # Full HTML content
    'screenshot_path': str,
    'network_requests': List[Dict],  # Network activity
    'console_logs': List[Dict],  # Browser console
    'dom_elements': Dict,  # Parsed DOM structure
    'javascript_libraries': List[str],  # Detected libraries
    'websocket_detected': bool,
    'timestamp': str
}
```

**DOM Analysis Details:**
- Canvas elements (untuk charts)
- SVG elements (untuk vector graphics)
- Table elements dengan row/col count
- Input elements (select, checkbox, radio, range)
- Download links/buttons
- Form elements

**Network Monitoring:**
- Semua HTTP requests
- Response status dan content-type
- Response body untuk JSON APIs
- WebSocket connections

---

### 2. Capability Analyzer (`capability_analyzer.py`)

**Purpose:** 
Menganalisis data scraping untuk mendeteksi 6 jenis output capability dengan bukti teknis.

**Detection Methods:**

#### a. Output Grafik/Chart
**Indikator Teknis:**
- `<canvas>` elements dengan size > 200x200px
- `<svg>` elements untuk vector charts
- Chart libraries: Chart.js, D3.js, Highcharts, ECharts, ApexCharts, Plotly
- CSS classes: `.chart`, `.graph`, `.plot`, `.visualization`

**Confidence Level:**
- Tinggi: Library terdeteksi + Canvas/SVG
- Sedang: Canvas/SVG tanpa library
- Rendah: Hanya CSS class

#### b. Output Data Tabel
**Indikator Teknis:**
- `<table>` dengan rows > 2 dan cols > 2
- Table libraries: DataTables, AG Grid, GridStack
- Table dengan `<thead>` atau `<th>` (header)
- CSS classes: `.grid`, `.datatable`, `.table-responsive`

**Confidence Level:**
- Tinggi: Library terdeteksi atau table dengan header
- Sedang: Table tanpa header
- Rendah: Hanya CSS class

#### c. Output File
**Indikator Teknis:**
- Elements dengan `download` attribute
- Links dengan pattern `/download`, `/export`
- Network requests dengan content-type:
  - `application/csv`
  - `application/vnd.ms-excel`
  - `application/pdf`
  - `image/*`
- URL patterns: `.csv`, `.xlsx`, `.pdf`

**Confidence Level:**
- Tinggi: Download attribute + network request
- Sedang: Network request saja
- Rendah: Hanya link pattern

#### d. Output Dinamis/Real-time
**Indikator Teknis:**
- WebSocket connection detected
- Server-Sent Events (`text/event-stream`)
- Polling pattern (3+ requests ke endpoint sama)
- Console logs dengan keywords: `websocket`, `socket.io`, `sse`, `realtime`

**Confidence Level:**
- Tinggi: WebSocket atau SSE
- Sedang: Polling pattern
- Rendah: Hanya console logs

#### e. Output Interaktif
**Indikator Teknis:**
- Input elements: select, checkbox, radio, range, date
- Form elements
- Event handlers: `onclick`, `onchange`
- XHR/Fetch requests (kemungkinan dari interaksi)

**Confidence Level:**
- Tinggi: Inputs + XHR/Fetch requests
- Sedang: Inputs + event handlers
- Rendah: Hanya inputs

#### f. Output Berbasis API
**Indikator Teknis:**
- XHR/Fetch requests
- Response dengan `content-type: application/json`
- URL patterns: `/api/`, `/rest/`, `/graphql`, `/v1/`, `/v2/`
- HTTP libraries: Axios, Fetch API
- Response body berisi data JSON

**Confidence Level:**
- Tinggi: JSON response dengan data + status 200
- Sedang: API request tanpa response body
- Rendah: Hanya URL pattern

---

### 3. PDF Generator (`pdf_generator.py`)

**Technology Stack:**
- ReportLab (PDF generation)
- Pillow (Image processing)

**PDF Structure:**

```
1. Cover Page
   - Title
   - Website names
   - Analysis date

2. Methodology
   - Verification approach
   - Technical evidence criteria
   - Analysis limitations

3. Summary Table
   ┌────────────────┬──────────┬──────────┬───────────┐
   │ Capability     │ Website A│ Website B│ Advantage │
   ├────────────────┼──────────┼──────────┼───────────┤
   │ Grafik/Chart   │ ✓ (high) │ ✗        │ Website A │
   │ ...            │ ...      │ ...      │ ...       │
   └────────────────┴──────────┴──────────┴───────────┘

4. Detailed Sections (per capability)
   For each capability:
   - Capability name
   - Website A:
     * Status
     * URL source
     * Technical indicators (bullets)
     * Screenshot (embedded)
   - Website B:
     * Same structure
   - Analysis notes

5. Conclusion
   - Unique capabilities Website A
   - Unique capabilities Website B
   - Shared capabilities
   - Overall summary
```

**Screenshot Handling:**
- Embedded in PDF (base64)
- Resized to fit page (max 5 inches width)
- Proportional scaling
- Caption with filename

---

## Workflow

### Step-by-Step Process

1. **Initialization**
   ```python
   comparator = WebsiteComparator()
   ```
   - Create screenshot directory
   - Create output directory
   - Initialize modules

2. **Scraping Website A**
   ```python
   website_a_data = await scraper.scrape_multiple_urls(urls_a, "Website A")
   ```
   - For each URL:
     * Launch headless browser
     * Navigate to URL
     * Wait for networkidle
     * Scroll to trigger lazy loading
     * Monitor network activity
     * Capture console logs
     * Analyze DOM
     * Detect JS libraries
     * Take screenshot
     * Save data

3. **Scraping Website B**
   - Same process as Website A

4. **Analyze Capabilities**
   ```python
   capabilities_a = analyzer.aggregate_website_capabilities(website_a_data)
   ```
   - For each scraped URL:
     * Run all capability detectors
     * Collect evidence
     * Determine confidence level
   - Aggregate across all URLs:
     * Overall support status
     * Best confidence level
     * List URLs with evidence

5. **Generate PDF**
   ```python
   pdf_generator.generate_report(...)
   ```
   - Build PDF structure
   - Format text and tables
   - Embed screenshots
   - Apply styling
   - Save to file

---

## Configuration Options

### WebsiteComparator

```python
WebsiteComparator(
    screenshot_dir="screenshots",  # Directory untuk screenshots
    output_dir="output"            # Directory untuk PDF output
)
```

### compare() Parameters

```python
comparator.compare(
    website_a_urls=["url1", "url2"],  # Required
    website_b_urls=["url1", "url2"],  # Required
    website_a_name="Website A",       # Optional
    website_b_name="Website B",       # Optional
    output_pdf="custom.pdf"           # Optional (auto-generated)
)
```

---

## Performance Considerations

### Timing
- Per URL scraping: ~10-15 seconds
- Network wait: ~3-5 seconds
- Screenshot capture: ~1-2 seconds
- PDF generation: ~5-10 seconds

**Example:**
- 3 URLs Website A: ~45 seconds
- 3 URLs Website B: ~45 seconds
- Analysis: ~5 seconds
- PDF generation: ~10 seconds
- **Total: ~105 seconds (~2 minutes)**

### Memory Usage
- Per page screenshot: ~1-5 MB
- HTML content: ~500 KB - 2 MB
- Network data: ~100 KB - 1 MB
- PDF output: ~5-20 MB (with screenshots)

### Optimization Tips
1. Limit URLs per website (3-5 recommended)
2. Use specific pages with known features
3. Avoid pages with heavy media
4. Use fast network connection

---

## Error Handling

### Common Issues

**1. Page Load Timeout**
```
Error: Navigation timeout
Solution: 
- Check URL accessibility
- Increase timeout in web_scraper.py (line ~77)
- Check internet connection
```

**2. Screenshot Fail**
```
Error: Cannot capture screenshot
Solution:
- Check disk space
- Check directory permissions
- Verify page rendered successfully
```

**3. Playwright Not Installed**
```
Error: Executable doesn't exist
Solution:
- Run: playwright install chromium
```

**4. PDF Generation Fail**
```
Error: Cannot load image
Solution:
- Verify screenshot files exist
- Check file path correctness
- Ensure reportlab installed correctly
```

---

## Extending the Tool

### Adding New Capability

1. **Update CapabilityAnalyzer**
   ```python
   # capability_analyzer.py
   
   CAPABILITIES = [
       # ... existing
       'output_new_capability'
   ]
   
   def _analyze_new_capability(self, data: Dict) -> Dict:
       evidence = []
       indicators = {}
       
       # Add detection logic
       
       return {
           'supported': bool,
           'confidence': 'tinggi|sedang|rendah',
           'evidence': evidence,
           'indicators': indicators
       }
   ```

2. **Update analyze_all_capabilities()**
   ```python
   results['output_new_capability'] = self._analyze_new_capability(scrape_data)
   ```

3. **Update PDF Generator**
   ```python
   # pdf_generator.py
   
   capability_names = {
       # ... existing
       'output_new_capability': 'Output New Capability'
   }
   ```

### Custom Styling

Edit `pdf_generator.py` in `_setup_custom_styles()`:

```python
self.styles.add(ParagraphStyle(
    name='CustomStyle',
    fontSize=12,
    textColor=HexColor('#000000'),
    # ... more options
))
```

---

## Troubleshooting

### Debug Mode

Enable verbose output in `web_scraper.py`:

```python
# Add at top of scrape_url()
print(f"[DEBUG] Navigating to: {url}")
print(f"[DEBUG] Network requests: {len(network_requests)}")
print(f"[DEBUG] Console logs: {len(console_logs)}")
```

### View Raw Data

Save scraping data to JSON:

```python
import json

# After scraping
with open('debug_data.json', 'w') as f:
    json.dump(website_a_data, f, indent=2, default=str)
```

### Test Individual Components

```python
# Test scraper only
from web_scraper import WebScraper
scraper = WebScraper()
result = asyncio.run(scraper.scrape_url("https://example.com", "Test"))
print(result.keys())

# Test analyzer only
from capability_analyzer import CapabilityAnalyzer
analyzer = CapabilityAnalyzer()
capabilities = analyzer.analyze_all_capabilities(result)
print(capabilities)
```

---

## Best Practices

1. **URL Selection**
   - Choose pages with clear features
   - Avoid login-required pages
   - Prefer pages with visible data/charts
   - Include diverse page types

2. **Naming Convention**
   - Use descriptive website names
   - Avoid special characters in names
   - Keep names short (< 30 chars)

3. **Screenshot Quality**
   - Ensure pages fully loaded
   - Check viewport size (default 1920x1080)
   - Verify screenshot clarity before analysis

4. **Result Validation**
   - Always review PDF output
   - Check screenshot relevance
   - Verify technical evidence makes sense
   - Compare with manual inspection

---

## API Reference

### WebsiteComparator

```python
class WebsiteComparator:
    def __init__(screenshot_dir: str, output_dir: str)
    def compare(
        website_a_urls: List[str],
        website_b_urls: List[str],
        website_a_name: str,
        website_b_name: str,
        output_pdf: str
    ) -> Dict
```

### WebScraper

```python
class WebScraper:
    def __init__(screenshot_dir: str)
    async def scrape_url(url: str, website_name: str) -> Dict
    async def scrape_multiple_urls(urls: List[str], website_name: str) -> List[Dict]
```

### CapabilityAnalyzer

```python
class CapabilityAnalyzer:
    def analyze_all_capabilities(scrape_data: Dict) -> Dict
    def aggregate_website_capabilities(all_scrape_results: List[Dict]) -> Dict
```

### PDFGenerator

```python
class PDFGenerator:
    def generate_report(
        website_a_name: str,
        website_b_name: str,
        website_a_capabilities: Dict,
        website_b_capabilities: Dict,
        output_path: str
    )
```

---

## License & Credits

This tool uses:
- Playwright (Apache 2.0)
- BeautifulSoup (MIT)
- ReportLab (BSD)
- Pillow (HPND)

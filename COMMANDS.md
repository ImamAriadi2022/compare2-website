# Command Cheat Sheet - Website Comparator

## 🚀 Setup Commands

### Windows
```bash
# Setup
setup.bat

# Activate environment
venv\Scripts\activate.bat

# Install Playwright
playwright install chromium

# Test installation
python test_suite.py
```

### Linux/Mac
```bash
# Setup
chmod +x setup.sh
./setup.sh

# Activate environment
source venv/bin/activate

# Install Playwright
playwright install chromium

# Test installation
python test_suite.py
```

---

## ⚡ Quick Run Commands

### Fastest Way
```bash
# Edit quick_start.py first, then:
python quick_start.py
```

### With Examples
```bash
python example.py
```

### Direct Python Import
```python
from website_comparator import compare_websites

result = compare_websites(
    website_a_urls=["https://a.com"],
    website_b_urls=["https://b.com"]
)
```

---

## 🔧 Development Commands

### Run Tests
```bash
# Full test suite
python test_suite.py

# Test specific module
python -c "from web_scraper import WebScraper; print('OK')"
python -c "from capability_analyzer import CapabilityAnalyzer; print('OK')"
python -c "from pdf_generator import PDFGenerator; print('OK')"
```

### Debug Mode
```python
# In Python script
import logging
logging.basicConfig(level=logging.DEBUG)

from website_comparator import compare_websites
# ... your code
```

### Check Dependencies
```bash
# List installed packages
pip list

# Check specific package
pip show playwright
pip show reportlab
pip show beautifulsoup4
```

---

## 📦 Dependency Management

### Install/Update
```bash
# Install all dependencies
pip install -r requirements.txt

# Update all dependencies
pip install --upgrade -r requirements.txt

# Install specific package
pip install playwright==1.41.0

# Update specific package
pip install --upgrade playwright
```

### Virtual Environment
```bash
# Create new venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate.bat

# Activate (Linux/Mac)
source venv/bin/activate

# Deactivate
deactivate

# Remove venv
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows
```

---

## 🖼️ Working with Screenshots

### View Screenshots
```bash
# List all screenshots
ls screenshots/  # Linux/Mac
dir screenshots\  # Windows

# Open screenshot folder
open screenshots/  # Mac
xdg-open screenshots/  # Linux
start screenshots\  # Windows
```

### Clean Screenshots
```bash
# Remove all screenshots
rm -rf screenshots/*  # Linux/Mac
del /Q screenshots\*  # Windows

# Clean old screenshots (> 7 days)
find screenshots/ -type f -mtime +7 -delete  # Linux/Mac
forfiles /p screenshots /d -7 /c "cmd /c del @file"  # Windows
```

---

## 📄 Working with PDFs

### View PDFs
```bash
# List all PDFs
ls output/*.pdf  # Linux/Mac
dir output\*.pdf  # Windows

# Open PDF folder
open output/  # Mac
xdg-open output/  # Linux
start output\  # Windows

# Open specific PDF
open output/comparison_*.pdf  # Mac
xdg-open output/comparison_*.pdf  # Linux
start output\comparison_*.pdf  # Windows
```

### Clean PDFs
```bash
# Remove all PDFs
rm output/*.pdf  # Linux/Mac
del output\*.pdf  # Windows

# Archive old PDFs
mkdir archive
mv output/*.pdf archive/  # Linux/Mac
move output\*.pdf archive\  # Windows
```

---

## 🧹 Cleanup Commands

### Full Cleanup
```bash
# Remove all generated files
rm -rf screenshots/* output/* test_screenshots/* test_output/*  # Linux/Mac
rmdir /s /q screenshots output test_screenshots test_output  # Windows (then recreate)

# Recreate directories
mkdir screenshots output
```

### Clean Cache
```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +  # Linux/Mac
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"  # Windows

# Remove .pyc files
find . -type f -name "*.pyc" -delete  # Linux/Mac
del /s *.pyc  # Windows
```

---

## 📊 Useful Python Snippets

### Quick Test
```python
# test_quick.py
from website_comparator import compare_websites

compare_websites(
    website_a_urls=["https://example.com"],
    website_b_urls=["https://example.org"],
    output_pdf="test_output.pdf"
)
```

### Check Scraping Only
```python
# test_scrape.py
import asyncio
from web_scraper import WebScraper

async def test():
    scraper = WebScraper()
    result = await scraper.scrape_url("https://example.com", "Test")
    print(f"Keys: {result.keys()}")
    print(f"Screenshot: {result['screenshot_path']}")

asyncio.run(test())
```

### Analyze Existing Data
```python
# test_analyze.py
from capability_analyzer import CapabilityAnalyzer
import json

# Load scraped data
with open('scraped_data.json', 'r') as f:
    data = json.load(f)

analyzer = CapabilityAnalyzer()
capabilities = analyzer.analyze_all_capabilities(data)

for cap, result in capabilities.items():
    if result['supported']:
        print(f"✓ {cap}: {result['confidence']}")
```

### Generate PDF from Existing Analysis
```python
# test_pdf.py
from pdf_generator import PDFGenerator
import json

# Load analysis results
with open('analysis_a.json', 'r') as f:
    cap_a = json.load(f)
with open('analysis_b.json', 'r') as f:
    cap_b = json.load(f)

generator = PDFGenerator()
generator.generate_report(
    website_a_name="Site A",
    website_b_name="Site B",
    website_a_capabilities=cap_a,
    website_b_capabilities=cap_b,
    output_path="manual_report.pdf"
)
```

---

## 🐛 Troubleshooting Commands

### Check Python Version
```bash
python --version
# Should be 3.8 or higher
```

### Check Playwright Installation
```bash
playwright --version
playwright list
```

### Verify Package Imports
```bash
python -c "import playwright; print('Playwright OK')"
python -c "import bs4; print('BeautifulSoup OK')"
python -c "import reportlab; print('ReportLab OK')"
python -c "from PIL import Image; print('Pillow OK')"
```

### Check Disk Space
```bash
# Linux/Mac
df -h .

# Windows
dir
```

### Network Test
```bash
# Test internet connection
ping google.com

# Test specific URL
curl -I https://example.com  # Linux/Mac
Invoke-WebRequest -Uri https://example.com -Method Head  # Windows PowerShell
```

---

## 📝 Git Commands (Optional)

### Initialize Git
```bash
git init
git add .
git commit -m "Initial commit"
```

### Ignore Generated Files
```bash
# .gitignore already includes:
# - screenshots/
# - output/
# - venv/
# - __pycache__/
```

### Common Git Operations
```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Your message"

# View history
git log --oneline
```

---

## 🔄 Update Commands

### Update Tool
```bash
# Backup data first
cp -r screenshots screenshots_backup
cp -r output output_backup

# Pull updates (if using Git)
git pull

# Update dependencies
pip install --upgrade -r requirements.txt

# Re-test
python test_suite.py
```

### Update Playwright Browsers
```bash
playwright install --update
```

---

## 💾 Export Commands

### Export to JSON
```python
# export_json.py
import json
from website_comparator import compare_websites

result = compare_websites(
    website_a_urls=["https://a.com"],
    website_b_urls=["https://b.com"]
)

# Export capabilities
with open('export.json', 'w') as f:
    json.dump({
        'website_a': result['website_a_capabilities'],
        'website_b': result['website_b_capabilities']
    }, f, indent=2)
```

### Export Screenshots List
```bash
# List screenshots with details
ls -lh screenshots/  # Linux/Mac
dir screenshots\  # Windows

# Export to file
ls -lh screenshots/ > screenshots_list.txt  # Linux/Mac
dir screenshots\ > screenshots_list.txt  # Windows
```

---

## 🎯 Performance Commands

### Measure Execution Time
```bash
# Linux/Mac
time python quick_start.py

# Windows (PowerShell)
Measure-Command { python quick_start.py }
```

### Profile Python Script
```python
import cProfile
from website_comparator import compare_websites

cProfile.run('''
compare_websites(
    website_a_urls=["https://example.com"],
    website_b_urls=["https://example.org"]
)
''')
```

---

## 📱 One-Liner Commands

### Quick Analysis
```bash
python -c "from website_comparator import compare_websites; compare_websites(['https://a.com'], ['https://b.com'])"
```

### Quick Test
```bash
python -c "import asyncio; from web_scraper import WebScraper; asyncio.run(WebScraper().scrape_url('https://example.com', 'Test'))"
```

### Check Everything
```bash
python --version && pip list && playwright list && python test_suite.py
```

---

## 🚀 Production Commands

### Run in Background (Linux/Mac)
```bash
nohup python quick_start.py > analysis.log 2>&1 &
```

### Run in Background (Windows)
```bash
start /B python quick_start.py > analysis.log 2>&1
```

### Schedule Analysis (Cron - Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add line (run daily at 2 AM)
0 2 * * * cd /path/to/compare2-website && source venv/bin/activate && python quick_start.py
```

### Schedule Analysis (Task Scheduler - Windows)
```powershell
# Create task via GUI or:
schtasks /create /tn "WebsiteComparison" /tr "C:\path\to\venv\Scripts\python.exe C:\path\to\quick_start.py" /sc daily /st 02:00
```

---

## 📚 Help Commands

### Python Help
```python
# In Python interpreter
from website_comparator import WebsiteComparator
help(WebsiteComparator)
help(WebsiteComparator.compare)
```

### Module Documentation
```bash
# View README
cat README.md | less  # Linux/Mac
type README.md | more  # Windows

# View guide
cat GUIDE.md | less  # Linux/Mac
type GUIDE.md | more  # Windows
```

---

**Quick Reference: Save this file for instant command access! 📌**

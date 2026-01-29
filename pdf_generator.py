"""
PDF Generator Module
Menghasilkan laporan PDF komprehensif dari hasil analisis
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.colors import HexColor
from datetime import datetime
from typing import Dict, List, Any
import os


class PDFGenerator:
    """Generator laporan PDF untuk hasil perbandingan website"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom styles untuk PDF"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#4a4a4a'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#2563eb'),
            spaceAfter=10,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=8
        ))
        
        # Caption
        self.styles.add(ParagraphStyle(
            name='Caption',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=HexColor('#666666'),
            alignment=TA_CENTER,
            spaceAfter=6
        ))
    
    def generate_report(
        self,
        website_a_name: str,
        website_b_name: str,
        website_a_capabilities: Dict[str, Any],
        website_b_capabilities: Dict[str, Any],
        output_path: str
    ):
        """
        Generate comprehensive PDF report
        
        Args:
            website_a_name: Nama Website A
            website_b_name: Nama Website B
            website_a_capabilities: Hasil analisis capability Website A
            website_b_capabilities: Hasil analisis capability Website B
            output_path: Path output PDF
        """
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        
        story = []
        
        # 1. Halaman Sampul
        story.extend(self._create_cover_page(website_a_name, website_b_name))
        story.append(PageBreak())
        
        # 2. Metodologi
        story.extend(self._create_methodology_section())
        story.append(PageBreak())
        
        # 3. Tabel Ringkasan
        story.extend(self._create_summary_table(
            website_a_name, website_b_name,
            website_a_capabilities, website_b_capabilities
        ))
        story.append(PageBreak())
        
        # 4. Detail Per Capability
        story.extend(self._create_detailed_sections(
            website_a_name, website_b_name,
            website_a_capabilities, website_b_capabilities
        ))
        
        # 5. Kesimpulan
        story.append(PageBreak())
        story.extend(self._create_conclusion_section(
            website_a_name, website_b_name,
            website_a_capabilities, website_b_capabilities
        ))
        
        # Build PDF
        doc.build(story)
        print(f"[SUCCESS] PDF generated: {output_path}")
    
    def _create_cover_page(self, website_a: str, website_b: str) -> List:
        """Buat halaman sampul"""
        
        elements = []
        
        # Spacer to center content
        elements.append(Spacer(1, 2.5 * inch))
        
        # Title
        title = Paragraph(
            "Perbandingan Output Capability<br/>Website A vs Website B",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.5 * inch))
        
        # Website names
        website_info = Paragraph(
            f"<b>Website A:</b> {website_a}<br/><b>Website B:</b> {website_b}",
            self.styles['CustomBody']
        )
        elements.append(website_info)
        elements.append(Spacer(1, 0.5 * inch))
        
        # Date
        date_text = Paragraph(
            f"Tanggal Analisis: {datetime.now().strftime('%d %B %Y')}",
            self.styles['CustomBody']
        )
        elements.append(date_text)
        
        return elements
    
    def _create_methodology_section(self) -> List:
        """Buat section metodologi"""
        
        elements = []
        
        # Section title
        elements.append(Paragraph("Metodologi Analisis", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Pendekatan
        elements.append(Paragraph("<b>Pendekatan Verifikasi:</b>", self.styles['CustomBody']))
        approach_text = """
        Analisis dilakukan menggunakan browser headless (Playwright) untuk merender setiap halaman 
        dan mengumpulkan data teknis secara komprehensif. Setiap capability diverifikasi melalui 
        bukti teknis yang dapat diamati dan screenshot visual.
        """
        elements.append(Paragraph(approach_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.15 * inch))
        
        # Kriteria bukti teknis
        elements.append(Paragraph("<b>Kriteria Bukti Teknis:</b>", self.styles['CustomBody']))
        criteria = [
            "Analisis DOM (Document Object Model) untuk deteksi elemen HTML",
            "Inspeksi JavaScript runtime untuk deteksi library dan framework",
            "Monitoring network activity untuk deteksi API calls dan file downloads",
            "Capture screenshot sebagai bukti visual",
            "Deteksi WebSocket dan Server-Sent Events untuk fitur real-time"
        ]
        
        for criterion in criteria:
            elements.append(Paragraph(f"• {criterion}", self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.15 * inch))
        
        # Batasan
        elements.append(Paragraph("<b>Batasan Analisis:</b>", self.styles['CustomBody']))
        limitations = [
            "Hanya menganalisis halaman yang dapat diakses publik (tanpa login)",
            "Fitur yang memerlukan interaksi kompleks mungkin tidak terdeteksi",
            "Analisis dilakukan pada waktu tertentu (state snapshot)",
            "Fitur tersembunyi atau belum di-load tidak akan terdeteksi"
        ]
        
        for limitation in limitations:
            elements.append(Paragraph(f"• {limitation}", self.styles['CustomBody']))
        
        return elements
    
    def _create_summary_table(
        self,
        website_a: str,
        website_b: str,
        cap_a: Dict[str, Any],
        cap_b: Dict[str, Any]
    ) -> List:
        """Buat tabel ringkasan perbandingan"""
        
        elements = []
        
        elements.append(Paragraph("Ringkasan Perbandingan", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Prepare table data
        data = [
            ['Capability', website_a, website_b, 'Keunggulan']
        ]
        
        capability_names = {
            'output_grafik_chart': 'Output Grafik/Chart',
            'output_data_tabel': 'Output Data Tabel',
            'output_file': 'Output File',
            'output_dinamis_realtime': 'Output Dinamis/Real-time',
            'output_interaktif': 'Output Interaktif',
            'output_berbasis_api': 'Output Berbasis API'
        }
        
        for key, name in capability_names.items():
            a_data = cap_a.get(key, {})
            b_data = cap_b.get(key, {})
            
            a_supported = a_data.get('supported', False)
            b_supported = b_data.get('supported', False)
            
            a_confidence = a_data.get('confidence', 'rendah')
            b_confidence = b_data.get('confidence', 'rendah')
            
            # Status dengan confidence
            a_status = f"{'✓' if a_supported else '✗'} ({a_confidence})" if a_supported else '✗'
            b_status = f"{'✓' if b_supported else '✗'} ({b_confidence})" if b_supported else '✗'
            
            # Determine advantage
            if a_supported and not b_supported:
                advantage = website_a
            elif b_supported and not a_supported:
                advantage = website_b
            elif a_supported and b_supported:
                if a_confidence == 'tinggi' and b_confidence != 'tinggi':
                    advantage = f"{website_a}*"
                elif b_confidence == 'tinggi' and a_confidence != 'tinggi':
                    advantage = f"{website_b}*"
                else:
                    advantage = "Setara"
            else:
                advantage = "-"
            
            data.append([name, a_status, b_status, advantage])
        
        # Create table
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f3f4f6')]),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.15 * inch))
        
        # Legend
        legend = Paragraph(
            "<i>* = Tingkat kepercayaan lebih tinggi</i>",
            self.styles['Caption']
        )
        elements.append(legend)
        
        return elements
    
    def _create_detailed_sections(
        self,
        website_a: str,
        website_b: str,
        cap_a: Dict[str, Any],
        cap_b: Dict[str, Any]
    ) -> List:
        """Buat detail section untuk setiap capability"""
        
        elements = []
        
        capability_names = {
            'output_grafik_chart': 'Output Grafik / Chart',
            'output_data_tabel': 'Output Data Tabel',
            'output_file': 'Output File (CSV, Excel, PDF, Gambar)',
            'output_dinamis_realtime': 'Output Dinamis / Real-time',
            'output_interaktif': 'Output Interaktif',
            'output_berbasis_api': 'Output Berbasis API'
        }
        
        for i, (key, name) in enumerate(capability_names.items()):
            if i > 0:
                elements.append(PageBreak())
            
            elements.extend(self._create_capability_detail(
                name, key, website_a, website_b, cap_a, cap_b
            ))
        
        return elements
    
    def _create_capability_detail(
        self,
        capability_name: str,
        capability_key: str,
        website_a: str,
        website_b: str,
        cap_a: Dict[str, Any],
        cap_b: Dict[str, Any]
    ) -> List:
        """Buat detail untuk satu capability"""
        
        elements = []
        
        # Capability title
        elements.append(Paragraph(capability_name, self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 0.2 * inch))
        
        a_data = cap_a.get(capability_key, {})
        b_data = cap_b.get(capability_key, {})
        
        # Website A section
        elements.append(Paragraph(f"<b>{website_a}</b>", self.styles['SectionHeader']))
        elements.extend(self._create_website_capability_detail(a_data, website_a))
        
        elements.append(Spacer(1, 0.3 * inch))
        
        # Website B section
        elements.append(Paragraph(f"<b>{website_b}</b>", self.styles['SectionHeader']))
        elements.extend(self._create_website_capability_detail(b_data, website_b))
        
        elements.append(Spacer(1, 0.3 * inch))
        
        # Analysis notes
        elements.append(Paragraph("<b>Catatan Analisis:</b>", self.styles['CustomBody']))
        analysis = self._generate_capability_analysis(
            capability_name, a_data, b_data, website_a, website_b
        )
        elements.append(Paragraph(analysis, self.styles['CustomBody']))
        
        return elements
    
    def _create_website_capability_detail(self, data: Dict[str, Any], website_name: str) -> List:
        """Buat detail capability untuk satu website"""
        
        elements = []
        
        supported = data.get('supported', False)
        confidence = data.get('confidence', 'rendah')
        urls_with_evidence = data.get('urls_with_evidence', [])
        
        # Status
        status_text = f"<b>Status:</b> {'DIDUKUNG' if supported else 'TIDAK DIDUKUNG'}"
        if supported:
            status_text += f" (Tingkat Kepercayaan: {confidence.upper()})"
        
        elements.append(Paragraph(status_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.1 * inch))
        
        if supported and urls_with_evidence:
            # Show first URL with evidence as primary example
            primary = urls_with_evidence[0]
            
            elements.append(Paragraph(f"<b>URL Sumber:</b> {primary['url']}", self.styles['CustomBody']))
            elements.append(Spacer(1, 0.05 * inch))
            
            # Evidence
            elements.append(Paragraph("<b>Indikator Teknis:</b>", self.styles['CustomBody']))
            for evidence in primary['evidence']:
                elements.append(Paragraph(f"• {evidence}", self.styles['CustomBody']))
            
            elements.append(Spacer(1, 0.1 * inch))
            
            # Screenshot
            screenshot_path = primary['screenshot']
            if screenshot_path and os.path.exists(screenshot_path):
                try:
                    # Resize image to fit page
                    img = Image(screenshot_path, width=5*inch, height=3*inch, kind='proportional')
                    elements.append(img)
                    elements.append(Paragraph(
                        f"Screenshot: {os.path.basename(screenshot_path)}",
                        self.styles['Caption']
                    ))
                except Exception as e:
                    elements.append(Paragraph(
                        f"<i>Screenshot tidak dapat dimuat: {str(e)}</i>",
                        self.styles['Caption']
                    ))
            else:
                elements.append(Paragraph(
                    "<i>Screenshot tidak tersedia</i>",
                    self.styles['Caption']
                ))
            
            # Additional URLs if any
            if len(urls_with_evidence) > 1:
                elements.append(Spacer(1, 0.1 * inch))
                elements.append(Paragraph(
                    f"<i>Capability ini juga ditemukan di {len(urls_with_evidence) - 1} URL lainnya</i>",
                    self.styles['Caption']
                ))
        else:
            elements.append(Paragraph(
                "<i>Tidak ditemukan bukti teknis untuk capability ini</i>",
                self.styles['CustomBody']
            ))
        
        return elements
    
    def _generate_capability_analysis(
        self,
        capability_name: str,
        a_data: Dict[str, Any],
        b_data: Dict[str, Any],
        website_a: str,
        website_b: str
    ) -> str:
        """Generate analysis text untuk capability"""
        
        a_supported = a_data.get('supported', False)
        b_supported = b_data.get('supported', False)
        
        if a_supported and not b_supported:
            return f"{website_a} memiliki {capability_name} yang dapat diverifikasi secara teknis, " \
                   f"sementara {website_b} tidak menunjukkan bukti capability ini."
        
        elif b_supported and not a_supported:
            return f"{website_b} memiliki {capability_name} yang dapat diverifikasi secara teknis, " \
                   f"sementara {website_a} tidak menunjukkan bukti capability ini."
        
        elif a_supported and b_supported:
            a_conf = a_data.get('confidence', 'rendah')
            b_conf = b_data.get('confidence', 'rendah')
            
            if a_conf == b_conf:
                return f"Kedua website memiliki {capability_name} dengan tingkat kepercayaan yang sama ({a_conf})."
            elif a_conf == 'tinggi' and b_conf != 'tinggi':
                return f"Kedua website memiliki {capability_name}, namun {website_a} menunjukkan " \
                       f"implementasi yang lebih kuat dengan bukti teknis lebih komprehensif."
            else:
                return f"Kedua website memiliki {capability_name}, namun {website_b} menunjukkan " \
                       f"implementasi yang lebih kuat dengan bukti teknis lebih komprehensif."
        
        else:
            return f"Kedua website tidak menunjukkan bukti {capability_name} pada halaman yang dianalisis."
    
    def _create_conclusion_section(
        self,
        website_a: str,
        website_b: str,
        cap_a: Dict[str, Any],
        cap_b: Dict[str, Any]
    ) -> List:
        """Buat section kesimpulan"""
        
        elements = []
        
        elements.append(Paragraph("Kesimpulan", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Find unique and shared capabilities
        a_unique = []
        b_unique = []
        shared = []
        
        for key in cap_a.keys():
            a_supported = cap_a[key].get('supported', False)
            b_supported = cap_b[key].get('supported', False)
            
            cap_name = key.replace('_', ' ').title()
            
            if a_supported and not b_supported:
                a_unique.append(cap_name)
            elif b_supported and not a_supported:
                b_unique.append(cap_name)
            elif a_supported and b_supported:
                shared.append(cap_name)
        
        # Unique to Website A
        elements.append(Paragraph(f"<b>Capability Unik {website_a}:</b>", self.styles['CustomBody']))
        if a_unique:
            for cap in a_unique:
                elements.append(Paragraph(f"• {cap}", self.styles['CustomBody']))
        else:
            elements.append(Paragraph("<i>Tidak ada capability unik</i>", self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.15 * inch))
        
        # Unique to Website B
        elements.append(Paragraph(f"<b>Capability Unik {website_b}:</b>", self.styles['CustomBody']))
        if b_unique:
            for cap in b_unique:
                elements.append(Paragraph(f"• {cap}", self.styles['CustomBody']))
        else:
            elements.append(Paragraph("<i>Tidak ada capability unik</i>", self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.15 * inch))
        
        # Shared capabilities
        elements.append(Paragraph("<b>Capability yang Sama:</b>", self.styles['CustomBody']))
        if shared:
            for cap in shared:
                elements.append(Paragraph(f"• {cap}", self.styles['CustomBody']))
        else:
            elements.append(Paragraph("<i>Tidak ada capability yang sama</i>", self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.2 * inch))
        
        # Overall summary
        elements.append(Paragraph("<b>Ringkasan Keunggulan:</b>", self.styles['CustomBody']))
        
        a_count = len(a_unique)
        b_count = len(b_unique)
        shared_count = len(shared)
        
        summary = f"{website_a} memiliki {a_count + shared_count} dari 6 capability yang dianalisis " \
                  f"({a_count} unik). {website_b} memiliki {b_count + shared_count} dari 6 capability " \
                  f"({b_count} unik). Kedua website berbagi {shared_count} capability yang sama."
        
        elements.append(Paragraph(summary, self.styles['CustomBody']))
        
        return elements

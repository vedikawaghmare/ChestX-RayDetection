#!/usr/bin/env python3
"""
PDF Report Generator with Charts for Chest X-Ray Analysis
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import base64
from io import BytesIO
from datetime import datetime
import os

# Set matplotlib to use non-interactive backend
plt.switch_backend('Agg')

class XRayReportGenerator:
    def __init__(self):
        self.colors = {
            'detected': '#e74c3c',
            'clear': '#27ae60',
            'background': '#f8f9fa',
            'text': '#2c3e50',
            'accent': '#3498db'
        }
        
    def create_analysis_charts(self, results, detected_conditions):
        """Create various charts for the analysis"""
        charts = {}
        
        # 1. Horizontal Bar Chart - All Conditions
        charts['bar_chart'] = self._create_bar_chart(results)
        
        # 2. Pie Chart - Detected vs Clear
        charts['pie_chart'] = self._create_pie_chart(results)
        
        # 3. Radar Chart - Top Conditions
        charts['radar_chart'] = self._create_radar_chart(results[:8])  # Top 8 for readability
        
        # 4. Severity Distribution
        charts['severity_chart'] = self._create_severity_chart(results)
        
        return charts
    
    def _create_bar_chart(self, results):
        """Create horizontal bar chart of all conditions"""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        diseases = [r['disease'] for r in results]
        probabilities = [r['probability'] * 100 for r in results]
        colors = [self.colors['detected'] if r['detected'] else self.colors['clear'] for r in results]
        
        bars = ax.barh(diseases, probabilities, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
        
        # Add percentage labels
        for i, (bar, prob) in enumerate(zip(bars, probabilities)):
            ax.text(prob + 1, bar.get_y() + bar.get_height()/2, 
                   f'{prob:.1f}%', va='center', fontweight='bold', fontsize=9)
        
        ax.set_xlabel('Probability (%)', fontsize=12, fontweight='bold')
        ax.set_title('Chest X-Ray Analysis - All Conditions', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlim(0, 100)
        
        # Add threshold line
        ax.axvline(x=50, color='red', linestyle='--', alpha=0.7, linewidth=2, label='Detection Threshold (50%)')
        ax.legend()
        
        # Styling
        ax.grid(axis='x', alpha=0.3)
        ax.set_facecolor(self.colors['background'])
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def _create_pie_chart(self, results):
        """Create pie chart showing detected vs clear conditions"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        detected_count = len([r for r in results if r['detected']])
        clear_count = len(results) - detected_count
        
        sizes = [detected_count, clear_count]
        labels = [f'Detected\n({detected_count} conditions)', f'Clear\n({clear_count} conditions)']
        colors = [self.colors['detected'], self.colors['clear']]
        explode = (0.1, 0) if detected_count > 0 else (0, 0)
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                         startangle=90, explode=explode, shadow=True,
                                         textprops={'fontsize': 12, 'fontweight': 'bold'})
        
        ax.set_title('Detection Summary', fontsize=16, fontweight='bold', pad=20)
        
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        
        return self._fig_to_base64(fig)
    
    def _create_radar_chart(self, top_results):
        """Create radar chart for top conditions"""
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        diseases = [r['disease'] for r in top_results]
        probabilities = [r['probability'] * 100 for r in top_results]
        
        # Number of variables
        N = len(diseases)
        
        # Compute angle for each axis
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the circle
        
        # Add values
        probabilities += probabilities[:1]  # Complete the circle
        
        # Plot
        ax.plot(angles, probabilities, 'o-', linewidth=2, color=self.colors['accent'])
        ax.fill(angles, probabilities, alpha=0.25, color=self.colors['accent'])
        
        # Add labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(diseases, fontsize=10)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
        ax.grid(True)
        
        ax.set_title('Top Conditions - Radar View', fontsize=16, fontweight='bold', pad=30)
        
        return self._fig_to_base64(fig)
    
    def _create_severity_chart(self, results):
        """Create severity distribution chart"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Severity counts
        severity_counts = {'High': 0, 'Medium': 0, 'Low': 0}
        for r in results:
            severity_counts[r['severity']] += 1
        
        # Bar chart of severity distribution
        severities = list(severity_counts.keys())
        counts = list(severity_counts.values())
        colors_sev = ['#e74c3c', '#f39c12', '#27ae60']
        
        bars = ax1.bar(severities, counts, color=colors_sev, alpha=0.8, edgecolor='white', linewidth=2)
        ax1.set_title('Severity Distribution', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Number of Conditions', fontweight='bold')
        
        # Add count labels on bars
        for bar, count in zip(bars, counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom', fontweight='bold')
        
        # Confidence distribution histogram
        confidences = [r['probability'] * 100 for r in results]
        ax2.hist(confidences, bins=10, color=self.colors['accent'], alpha=0.7, edgecolor='white', linewidth=1)
        ax2.set_title('Confidence Distribution', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Confidence (%)', fontweight='bold')
        ax2.set_ylabel('Number of Conditions', fontweight='bold')
        ax2.axvline(x=50, color='red', linestyle='--', alpha=0.7, linewidth=2, label='Threshold')
        ax2.legend()
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 string"""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        return image_base64
    
    def generate_pdf_report(self, analysis_data, patient_info=None):
        """Generate comprehensive PDF report"""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors as rl_colors
            from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
            
            # Create PDF buffer
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                                  topMargin=72, bottomMargin=18)
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=rl_colors.HexColor('#2c3e50')
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                textColor=rl_colors.HexColor('#3498db')
            )
            
            # Story container
            story = []
            
            # Title
            story.append(Paragraph("🏥 CHEST X-RAY ANALYSIS REPORT", title_style))
            story.append(Spacer(1, 20))
            
            # Patient/Analysis Info
            info_data = [
                ['Analysis Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['AI Model:', 'DenseNet-121 Deep Learning Architecture'],
                ['Conditions Analyzed:', '14 Pathological Conditions'],
                ['Analysis Type:', 'Multi-label Classification']
            ]
            
            if patient_info:
                info_data.insert(0, ['Patient ID:', patient_info.get('id', 'N/A')])
                info_data.insert(1, ['Patient Name:', patient_info.get('name', 'N/A')])
            
            info_table = Table(info_data, colWidths=[2*inch, 3*inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), rl_colors.HexColor('#ecf0f1')),
                ('TEXTCOLOR', (0, 0), (-1, -1), rl_colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, rl_colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(info_table)
            story.append(Spacer(1, 30))
            
            # Summary
            summary = analysis_data.get('summary', {})
            story.append(Paragraph("📊 ANALYSIS SUMMARY", heading_style))
            
            summary_text = f"""
            <b>Overall Status:</b> {summary.get('status', 'Unknown')}<br/>
            <b>Total Conditions Checked:</b> {analysis_data.get('total_conditions_checked', 0)}<br/>
            <b>Conditions Detected:</b> {summary.get('detected_count', 0)}<br/>
            <b>Highest Probability:</b> {summary.get('highest_probability', {}).get('disease', 'N/A')} 
            ({summary.get('highest_probability', {}).get('confidence', 'N/A')})
            """
            
            story.append(Paragraph(summary_text, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Detected Conditions Table
            detected = analysis_data.get('detected_conditions', [])
            if detected:
                story.append(Paragraph("🚨 DETECTED CONDITIONS", heading_style))
                
                detected_data = [['Condition', 'Probability', 'Confidence', 'Severity']]
                for condition in detected:
                    detected_data.append([
                        condition['disease'],
                        f"{condition['probability']:.3f}",
                        condition['confidence'],
                        condition['severity']
                    ])
                
                detected_table = Table(detected_data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch])
                detected_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor('#e74c3c')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, rl_colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BACKGROUND', (0, 1), (-1, -1), rl_colors.HexColor('#fdf2f2')),
                ]))
                
                story.append(detected_table)
                story.append(Spacer(1, 20))
            
            # Complete Results Table
            story.append(Paragraph("📋 COMPLETE ANALYSIS RESULTS", heading_style))
            
            results_data = [['Condition', 'Probability', 'Confidence', 'Status', 'Severity']]
            for result in analysis_data.get('results', []):
                status = 'DETECTED' if result['detected'] else 'CLEAR'
                results_data.append([
                    result['disease'],
                    f"{result['probability']:.3f}",
                    result['confidence'],
                    status,
                    result['severity']
                ])
            
            results_table = Table(results_data, colWidths=[1.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
            results_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, rl_colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            # Color code rows based on detection
            for i, result in enumerate(analysis_data.get('results', []), 1):
                if result['detected']:
                    results_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, i), (-1, i), rl_colors.HexColor('#fdf2f2'))
                    ]))
                else:
                    results_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, i), (-1, i), rl_colors.HexColor('#f2fdf2'))
                    ]))
            
            story.append(results_table)
            story.append(PageBreak())
            
            # Charts Page
            story.append(Paragraph("📈 VISUAL ANALYSIS", title_style))
            story.append(Spacer(1, 20))
            
            # Generate charts
            charts = self.create_analysis_charts(analysis_data.get('results', []), 
                                               analysis_data.get('detected_conditions', []))
            
            # Add charts to PDF
            chart_titles = {
                'bar_chart': 'Probability Distribution - All Conditions',
                'pie_chart': 'Detection Summary',
                'radar_chart': 'Top Conditions - Radar View',
                'severity_chart': 'Severity and Confidence Distribution'
            }
            
            for chart_key, chart_base64 in charts.items():
                if chart_base64:
                    story.append(Paragraph(chart_titles.get(chart_key, 'Chart'), heading_style))
                    
                    # Convert base64 to image
                    chart_buffer = BytesIO(base64.b64decode(chart_base64))
                    chart_img = Image(chart_buffer, width=6*inch, height=4*inch)
                    story.append(chart_img)
                    story.append(Spacer(1, 20))
            
            # Medical Disclaimer
            story.append(PageBreak())
            story.append(Paragraph("⚠️ MEDICAL DISCLAIMER", heading_style))
            
            disclaimer_text = """
            <b>IMPORTANT NOTICE:</b><br/><br/>
            
            This AI-powered chest X-ray analysis is provided for <b>educational and research purposes only</b>. 
            The results should <b>NOT</b> be used as a substitute for professional medical diagnosis, treatment, 
            or advice.<br/><br/>
            
            <b>Key Points:</b><br/>
            • This system is designed for educational demonstration of AI in medical imaging<br/>
            • Results are generated by a DenseNet-121 deep learning model<br/>
            • The model may produce false positives or false negatives<br/>
            • Clinical correlation and professional medical evaluation are essential<br/>
            • Always consult qualified healthcare professionals for medical decisions<br/><br/>
            
            <b>Limitations:</b><br/>
            • AI models are not infallible and may miss conditions or produce false alarms<br/>
            • Image quality, positioning, and technical factors can affect results<br/>
            • The model was trained on specific datasets and may not generalize to all populations<br/>
            • This tool does not replace radiologist expertise and clinical judgment<br/><br/>
            
            <b>For Medical Professionals:</b><br/>
            This tool may serve as a supplementary aid but should never replace clinical expertise, 
            proper medical imaging protocols, or comprehensive patient evaluation.
            """
            
            story.append(Paragraph(disclaimer_text, styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            # Get PDF data
            pdf_data = buffer.getvalue()
            buffer.close()
            
            return pdf_data
            
        except ImportError:
            # Fallback to simple text report if reportlab not available
            return self._generate_simple_text_report(analysis_data)
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None
    
    def _generate_simple_text_report(self, analysis_data):
        """Generate simple text report as fallback"""
        report = f"""
CHEST X-RAY ANALYSIS REPORT
===========================

Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
AI Model: DenseNet-121 Deep Learning Architecture

SUMMARY:
--------
Status: {analysis_data.get('summary', {}).get('status', 'Unknown')}
Total Conditions Checked: {analysis_data.get('total_conditions_checked', 0)}
Conditions Detected: {analysis_data.get('summary', {}).get('detected_count', 0)}

DETECTED CONDITIONS:
-------------------
"""
        
        detected = analysis_data.get('detected_conditions', [])
        if detected:
            for condition in detected:
                report += f"• {condition['disease']}: {condition['confidence']} ({condition['severity']} severity)\n"
        else:
            report += "No significant abnormalities detected.\n"
        
        report += "\nCOMPLETE RESULTS:\n"
        report += "-" * 50 + "\n"
        
        for result in analysis_data.get('results', []):
            status = "DETECTED" if result['detected'] else "CLEAR"
            report += f"{result['disease']:<20} {result['confidence']:<8} {status:<10} {result['severity']}\n"
        
        report += "\nMEDICAL DISCLAIMER:\n"
        report += "This analysis is for educational purposes only. Always consult healthcare professionals.\n"
        
        return report.encode('utf-8')

# Global instance
report_generator = XRayReportGenerator()
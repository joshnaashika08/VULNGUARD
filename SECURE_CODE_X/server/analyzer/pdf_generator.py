from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
import datetime

def generate_pdf_report(analysis_results):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "Vulnerability Analysis Report")

    # Metadata
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 100, f"Language Detected: {analysis_results.get('language', 'Unknown')}")
    
    # Scores
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 140, "Scores:")
    c.setFont("Helvetica", 12)
    c.drawString(70, height - 160, f"Security Score: {analysis_results.get('security_score', 'N/A')}")
    c.drawString(70, height - 180, f"Quality Score: {analysis_results.get('code_quality_score', 'N/A')}")
    c.drawString(70, height - 200, f"Confidence: {analysis_results.get('overall_confidence', 'N/A')}")

    # Vulnerabilities
    y_position = height - 240
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "Detected Vulnerabilities:")
    y_position -= 30
    
    c.setFont("Helvetica", 10)
    
    vulns = analysis_results.get('vulnerabilities', [])
    if not vulns:
        c.drawString(70, y_position, "No vulnerabilities detected.")
    else:
        for vuln in vulns:
            if y_position < 100:
                c.showPage()
                y_position = height - 50
            
            severity = vuln.get('severity', 'Unknown')
            if severity == 'Critical' or severity == 'High':
                c.setFillColor(colors.red)
            elif severity == 'Medium':
                c.setFillColor(colors.orange)
            else:
                c.setFillColor(colors.green)
                
            c.drawString(70, y_position, f"[{severity}] {vuln.get('type', 'Unknown')}")
            c.setFillColor(colors.black)
            y_position -= 15
            c.drawString(90, y_position, f"Line {vuln.get('line', '?')}: {vuln.get('description', '')}")
            y_position -= 15
            c.drawString(90, y_position, f"Fix: {vuln.get('suggested_fix', '')}")
            y_position -= 25

    c.save()
    buffer.seek(0)
    return buffer

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io
from typing import Dict, Any

def generate_support_summary_pdf(session_data: Dict[str, Any], language: str) -> bytes:
    """
    Generate a support summary PDF from session data
    """
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0D9488'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#4F46E5'),
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=12,
        spaceAfter=12
    )
    
    # Translations
    translations = {
        'en': {
            'title': 'AidAssist Support Summary',
            'session_info': 'Session Information',
            'session_id': 'Session ID',
            'date': 'Date',
            'complaint': 'User Complaint',
            'issue_category': 'Issue Category',
            'device_info': 'Device Information',
            'device_type': 'Device Type',
            'power_type': 'Power Type',
            'side': 'Affected Side',
            'exposed': 'Exposed to Water/Dropped',
            'steps_attempted': 'Troubleshooting Steps Attempted',
            'outcome': 'Outcome',
            'status': 'Status',
            'note': 'Note: This summary is for informational purposes only and should be shared with your hearing care professional.'
        },
        'hi': {
            'title': 'AidAssist सहायता सारांश',
            'session_info': 'सत्र जानकारी',
            'session_id': 'सत्र आईडी',
            'date': 'तारीख',
            'complaint': 'उपयोगकर्ता शिकायत',
            'issue_category': 'समस्या श्रेणी',
            'device_info': 'डिवाइस जानकारी',
            'device_type': 'डिवाइस प्रकार',
            'power_type': 'पावर प्रकार',
            'side': 'प्रभावित पक्ष',
            'exposed': 'पानी/गिरने के संपर्क में',
            'steps_attempted': 'प्रयास किए गए समस्या निवारण कदम',
            'outcome': 'परिणाम',
            'status': 'स्थिति',
            'note': 'नोट: यह सारांश केवल जानकारी के उद्देश्यों के लिए है और इसे आपके हियरिंग केयर पेशेवर के साथ साझा किया जाना चाहिए।'
        },
        'kn': {
            'title': 'AidAssist ಬೆಂಬಲ ಸಾರಾಂಶ',
            'session_info': 'ಸತ್ರದ ಮಾಹಿತಿ',
            'session_id': 'ಸತ್ರ ಐಡಿ',
            'date': 'ದಿನಾಂಕ',
            'complaint': 'ಬೃಹಸ್ಪತಿಯವರ ಗಾಯನ',
            'issue_category': 'ಸಮಸ್ಯೆ ವರ್ಗ',
            'device_info': 'ಸಾಧನದ ಮಾಹಿತಿ',
            'device_type': 'ಸಾಧನದ ಪ್ರಕಾರ',
            'power_type': 'ವಿದ್ಯುತ್ ಪ್ರಕಾರ',
            'side': 'ಪ್ರಭಾವಿತ ಬಾಜು',
            'exposed': 'ನೀರು/ಬಿಡುವಿಕೆಗೆ ಪ್ರತ್ಯಕ್ಷ',
            'steps_attempted': 'ಪ್ರಯತ್ನಿಸಿದ ದೋಷಪರಿಹಾರ ಹಂತಗಳು',
            'outcome': 'ಪರಿಣಾಮ',
            'status': 'ಸ್ಥಿತಿ',
            'note': 'ನೋಂದಣಿ: ಈ ಸಾರಾಂಶವು ಕೇವಲ ಮಾಹಿತಿಗಾಗಿ ಮತ್ತು ನಿಮ್ಮ ಶ್ರವಣ ಆರೈಕೆ ವೃತ್ತಿಪರರೊಂದಿಗೆ ಹಂಚಿಕೊಳ್ಳಬೇಕು.'
        }
    }
    
    t = translations.get(language, translations['en'])
    
    # Title
    elements.append(Paragraph(t['title'], title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Session Info
    elements.append(Paragraph(t['session_info'], heading_style))
    session_table_data = [
        [t['session_id'], session_data.get('id', 'N/A')],
        [t['date'], datetime.fromisoformat(session_data.get('created_at', '')).strftime('%Y-%m-%d %H:%M') if session_data.get('created_at') else 'N/A'],
    ]
    session_table = Table(session_table_data, colWidths=[2*inch, 4*inch])
    session_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(session_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Complaint
    elements.append(Paragraph(t['complaint'], heading_style))
    triage_data = session_data.get('triage_data', {})
    classification = session_data.get('classification_result', {})
    complaint_text = triage_data.get('additional_details', 'No additional details provided')
    elements.append(Paragraph(complaint_text, body_style))
    elements.append(Paragraph(f"<b>{t['issue_category']}:</b> {classification.get('issue_category', 'Unknown')}", body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Device Info
    elements.append(Paragraph(t['device_info'], heading_style))
    device_table_data = [
        [t['device_type'], triage_data.get('device_type', 'N/A')],
        [t['power_type'], triage_data.get('power_type', 'N/A')],
        [t['side'], triage_data.get('side', 'N/A')],
        [t['exposed'], 'Yes' if triage_data.get('exposed_to_water') else 'No'],
    ]
    device_table = Table(device_table_data, colWidths=[2*inch, 4*inch])
    device_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(device_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Steps Attempted
    elements.append(Paragraph(t['steps_attempted'], heading_style))
    steps = session_data.get('steps_attempted', [])
    if steps:
        for i, step in enumerate(steps, 1):
            step_text = f"{i}. {step.get('step_id', 'Unknown')} - {step.get('action', 'N/A')}"
            elements.append(Paragraph(step_text, body_style))
    else:
        elements.append(Paragraph('No steps attempted yet.', body_style))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # Status
    elements.append(Paragraph(t['status'], heading_style))
    status_text = session_data.get('status', 'in_progress').replace('_', ' ').title()
    elements.append(Paragraph(status_text, body_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Note
    note_style = ParagraphStyle(
        'Note',
        parent=styles['Italic'],
        fontSize=10,
        textColor=colors.grey
    )
    elements.append(Paragraph(t['note'], note_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

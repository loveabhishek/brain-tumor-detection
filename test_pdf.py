#!/usr/bin/env python3
"""
Test script for PDF report generation functionality
"""

import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

def test_pdf_generation():
    """Test the PDF generation functionality"""
    
    # Create test data
    patient_info = {
        'name': 'John Doe',
        'age': '45',
        'sex': 'Male'
    }
    
    prediction_result = "Yes Brain Tumor"
    
    tumor_data = {
        'size': 2.5,
        'is_dangerous': False,
        'life_span': 15,
        'treatment_timeframe': 'within 6 months'
    }
    
    # Create PDF
    pdf_filename = "test_report.pdf"
    pdf_path = os.path.join('uploads', pdf_filename)
    
    # Ensure uploads directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    normal_style = styles['Normal']
    
    # Build PDF content
    story = []
    
    # Title
    story.append(Paragraph("BRAIN TUMOR DETECTION REPORT", title_style))
    story.append(Spacer(1, 20))
    
    # Report metadata
    story.append(Paragraph(f"Report Date: {datetime.now().strftime('%B %d, %Y')}", normal_style))
    story.append(Paragraph(f"Report Time: {datetime.now().strftime('%I:%M %p')}", normal_style))
    story.append(Spacer(1, 20))
    
    # Patient Information
    story.append(Paragraph("PATIENT INFORMATION", heading_style))
    patient_data = [
        ['Name:', patient_info['name']],
        ['Age:', f"{patient_info['age']} years"],
        ['Sex:', patient_info['sex']]
    ]
    patient_table = Table(patient_data, colWidths=[1.5*inch, 3*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    # Analysis Results
    story.append(Paragraph("ANALYSIS RESULTS", heading_style))
    detection_color = colors.red if "Yes" in prediction_result else colors.green
    story.append(Paragraph(f"<b>Tumor Detection:</b> <font color='{detection_color}'>{prediction_result}</font>", normal_style))
    story.append(Spacer(1, 12))
    
    # Tumor details
    story.append(Paragraph("TUMOR CHARACTERISTICS", heading_style))
    tumor_data_table = [
        ['Characteristic', 'Value'],
        ['Tumor Size', f"{tumor_data['size']} cm"],
        ['Danger Level', 'HIGH' if tumor_data['is_dangerous'] else 'LOW'],
        ['Estimated Life Span', f"{tumor_data['life_span']} years"],
        ['Recommended Treatment Timeframe', tumor_data['treatment_timeframe']]
    ]
    
    tumor_table = Table(tumor_data_table, colWidths=[2.5*inch, 2*inch])
    tumor_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey)
    ]))
    story.append(tumor_table)
    story.append(Spacer(1, 20))
    
    # Medical recommendations
    story.append(Paragraph("MEDICAL RECOMMENDATIONS", heading_style))
    if tumor_data['is_dangerous']:
        story.append(Paragraph("• <b>URGENT:</b> Immediate medical consultation required", normal_style))
        story.append(Paragraph("• Schedule MRI follow-up within 2 weeks", normal_style))
        story.append(Paragraph("• Consider neurosurgical consultation", normal_style))
    else:
        story.append(Paragraph("• Schedule follow-up MRI within 3 months", normal_style))
        story.append(Paragraph("• Regular monitoring recommended", normal_style))
        story.append(Paragraph("• Consult with neurologist for treatment options", normal_style))
    
    story.append(Spacer(1, 20))
    
    # Disclaimer
    story.append(Paragraph("DISCLAIMER", heading_style))
    story.append(Paragraph("This report is generated by an AI system for preliminary screening purposes only. "
                          "It should not replace professional medical diagnosis. Please consult with a qualified "
                          "healthcare provider for proper medical evaluation and treatment.", normal_style))
    
    # Build PDF
    doc.build(story)
    
    print(f"✅ Test PDF generated successfully: {pdf_path}")
    print(f"📄 File size: {os.path.getsize(pdf_path)} bytes")
    return True

if __name__ == "__main__":
    try:
        test_pdf_generation()
        print("🎉 PDF generation test completed successfully!")
    except Exception as e:
        print(f"❌ Error during PDF generation test: {e}")
        sys.exit(1) 
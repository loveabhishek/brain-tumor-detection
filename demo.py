#!/usr/bin/env python3
"""
Demo script for the Brain Tumor Detection & Report Generation System
This script demonstrates the core functionality without needing the web interface.
"""

import os
import random
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
import uuid

def generate_tumor_data():
    """Generate random tumor data for demonstration purposes"""
    tumor_size = round(random.uniform(0.5, 5.0), 2)  # Size in cm
    is_dangerous = tumor_size > 3.0
    
    if is_dangerous:
        life_span = random.randint(1, 5)  # 1-5 years if dangerous
        treatment_timeframe = "within 1 month" if tumor_size > 4.0 else "within 3 months"
    else:
        life_span = random.randint(10, 30)  # 10-30 years if not dangerous
        treatment_timeframe = "within 6 months"
    
    return {
        'size': tumor_size,
        'is_dangerous': is_dangerous,
        'life_span': life_span,
        'treatment_timeframe': treatment_timeframe
    }

def generate_pdf_report(patient_info, prediction_result, tumor_data=None):
    """Generate a medical report PDF"""
    # Create unique filename for PDF
    pdf_filename = f"demo_report_{uuid.uuid4().hex[:8]}.pdf"
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
    
    if tumor_data and "Yes" in prediction_result:
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
    else:
        story.append(Paragraph("No tumor detected. Continue with regular health monitoring.", normal_style))
    
    story.append(Spacer(1, 20))
    
    # Disclaimer
    story.append(Paragraph("DISCLAIMER", heading_style))
    story.append(Paragraph("This report is generated by an AI system for preliminary screening purposes only. "
                          "It should not replace professional medical diagnosis. Please consult with a qualified "
                          "healthcare provider for proper medical evaluation and treatment.", normal_style))
    
    # Build PDF
    doc.build(story)
    return pdf_filename

def demo_scenarios():
    """Demonstrate different scenarios"""
    print("🧠 Brain Tumor Detection & Report Generation System - Demo")
    print("=" * 60)
    
    # Scenario 1: No tumor detected
    print("\n📋 Scenario 1: No Tumor Detected")
    print("-" * 40)
    
    patient1 = {
        'name': 'Sarah Johnson',
        'age': '32',
        'sex': 'Female'
    }
    
    prediction1 = "No Brain Tumor"
    pdf1 = generate_pdf_report(patient1, prediction1)
    print(f"✅ Generated report: {pdf1}")
    print(f"📄 Patient: {patient1['name']}, Age: {patient1['age']}, Result: {prediction1}")
    
    # Scenario 2: Small tumor detected (low risk)
    print("\n📋 Scenario 2: Small Tumor Detected (Low Risk)")
    print("-" * 40)
    
    patient2 = {
        'name': 'Michael Chen',
        'age': '45',
        'sex': 'Male'
    }
    
    prediction2 = "Yes Brain Tumor"
    tumor_data2 = generate_tumor_data()
    # Ensure it's a small tumor for this scenario
    tumor_data2['size'] = 1.8
    tumor_data2['is_dangerous'] = False
    tumor_data2['life_span'] = 20
    tumor_data2['treatment_timeframe'] = "within 6 months"
    
    pdf2 = generate_pdf_report(patient2, prediction2, tumor_data2)
    print(f"✅ Generated report: {pdf2}")
    print(f"📄 Patient: {patient2['name']}, Age: {patient2['age']}, Result: {prediction2}")
    print(f"🔍 Tumor Size: {tumor_data2['size']} cm, Danger Level: LOW")
    
    # Scenario 3: Large tumor detected (high risk)
    print("\n📋 Scenario 3: Large Tumor Detected (High Risk)")
    print("-" * 40)
    
    patient3 = {
        'name': 'Robert Williams',
        'age': '58',
        'sex': 'Male'
    }
    
    prediction3 = "Yes Brain Tumor"
    tumor_data3 = generate_tumor_data()
    # Ensure it's a large tumor for this scenario
    tumor_data3['size'] = 4.2
    tumor_data3['is_dangerous'] = True
    tumor_data3['life_span'] = 3
    tumor_data3['treatment_timeframe'] = "within 1 month"
    
    pdf3 = generate_pdf_report(patient3, prediction3, tumor_data3)
    print(f"✅ Generated report: {pdf3}")
    print(f"📄 Patient: {patient3['name']}, Age: {patient3['age']}, Result: {prediction3}")
    print(f"🔍 Tumor Size: {tumor_data3['size']} cm, Danger Level: HIGH")
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed successfully!")
    print("📁 All reports saved in the 'uploads' folder")
    print("🌐 Start the Flask app with 'python app.py' to use the web interface")

if __name__ == "__main__":
    demo_scenarios() 
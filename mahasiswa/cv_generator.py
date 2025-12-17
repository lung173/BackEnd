from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from mahasiswa.models import Mahasiswa
from datetime import datetime

@api_view(['GET'])
@permission_classes([AllowAny])
def download_cv(request, pk):
    """Generate and download CV as PDF"""
    try:
        # Removed is_active filter - allow CV download for all mahasiswa
        mahasiswa = Mahasiswa.objects.get(pk=pk)
    except Mahasiswa.DoesNotExist:
        return HttpResponse("Mahasiswa tidak ditemukan", status=404)
    
    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for PDF elements
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Header - Nama
    elements.append(Paragraph(mahasiswa.nama, title_style))
    elements.append(Paragraph(f"NIM: {mahasiswa.nim}", styles['Normal']))
    elements.append(Paragraph(f"{mahasiswa.prodi} - {mahasiswa.fakultas}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Contact Info
    contact_info = f"""
    Email: {mahasiswa.email}<br/>
    Telepon: {mahasiswa.telepon or '-'}<br/>
    LinkedIn: {mahasiswa.linkedin or '-'}<br/>
    GitHub: {mahasiswa.github or '-'}
    """
    elements.append(Paragraph(contact_info, styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Bio
    if mahasiswa.bio:
        elements.append(Paragraph("TENTANG SAYA", heading_style))
        elements.append(Paragraph(mahasiswa.bio, styles['Normal']))
        elements.append(Spacer(1, 20))
    
    # Skills
    skills = mahasiswa.skills.all()
    if skills.exists():
        elements.append(Paragraph("KEAHLIAN", heading_style))
        skills_data = [[skill.nama, skill.level or '-'] for skill in skills]
        skills_table = Table(skills_data, colWidths=[3*inch, 2*inch])
        skills_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(skills_table)
        elements.append(Spacer(1, 20))
    
    # Portfolio/Experiences
    talents = mahasiswa.talents.all().order_by('-tanggal_mulai')
    if talents.exists():
        elements.append(Paragraph("PORTFOLIO & PENGALAMAN", heading_style))
        for talent in talents:
            talent_title = Paragraph(f"<b>{talent.judul}</b>", styles['Normal'])
            elements.append(talent_title)
            
            if talent.kategori:
                elements.append(Paragraph(f"<i>{talent.kategori}</i>", styles['Normal']))
            
            periode = ""
            if talent.tanggal_mulai:
                periode = talent.tanggal_mulai.strftime('%B %Y')
                if talent.tanggal_selesai:
                    periode += f" - {talent.tanggal_selesai.strftime('%B %Y')}"
                else:
                    periode += " - Sekarang"
                elements.append(Paragraph(periode, styles['Normal']))
            
            elements.append(Paragraph(talent.deskripsi, styles['Normal']))
            
            if talent.link_portfolio:
                elements.append(Paragraph(f"Link: {talent.link_portfolio}", styles['Normal']))
            
            elements.append(Spacer(1, 12))
    
    # Footer
    elements.append(Spacer(1, 30))
    footer_text = f"<i>CV ini dibuat otomatis dari Talenta Mahasiswa UMS pada {datetime.now().strftime('%d %B %Y')}</i>"
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF value
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create response with CORS headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{mahasiswa.nama}_CV.pdf"'
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.write(pdf)
    
    return response

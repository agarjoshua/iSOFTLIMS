from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from io import BytesIO
from django.core.mail import send_mail

def generate_table_pdf(data, institution):
    # Create a BytesIO buffer for the PDF
    buffer = BytesIO()

    # Set up the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Add the institution logo
    if institution.logo:
        logo_path = institution.logo.path
        logo_image = Image(logo_path, width=200, height=100)
        elements.append(logo_image)

    # Create the table
    table_data = [[column for column in data[0].keys()]]
    for row in data:
        table_data.append([str(row[column]) for column in data[0].keys()])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'grey'),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), 'white'),
        ('TEXTCOLOR', (0, 1), (-1, -1), 'black'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    # Add the table to the PDF document
    elements.append(table)
    doc.build(elements)

    # Reset the buffer's file pointer
    buffer.seek(0)

    return buffer


def generate_pdf_and_send_email(request):
    # Generate the PDF
    data = [
        {"Name": "John", "Age": 25, "Country": "USA"},
        {"Name": "Emma", "Age": 30, "Country": "UK"},
        {"Name": "Mike", "Age": 35, "Country": "Canada"}
    ]
    return generate_table_pdf(data)


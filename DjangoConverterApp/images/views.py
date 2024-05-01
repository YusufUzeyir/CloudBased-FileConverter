from django.shortcuts import render, HttpResponse
import img2pdf
from PIL import Image
import fpdf
import io
from docx import Document
from docx2pdf import convert
import uuid
import pythoncom
import os

def imgtopdf(request):
    if request.method == 'POST':
        img = request.FILES['img']
        pdf = img2pdf.convert(img)

        return HttpResponse(pdf, content_type='application/pdf')
    return render(request, 'imgtopdf.html')

def txttopdf(request):
    if request.method == 'POST':
        txt = request.FILES['txt']
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt.read().decode('utf-8'), 0, 1)
        return HttpResponse(pdf.output(dest='S'), content_type='application/pdf')
    return render(request, 'txttopdf.html')

def jpgtopng(request):
    if request.method == 'POST':
        img = request.FILES['img']
        im = Image.open(img)
        response = HttpResponse(content_type="image/png")
        im.save(response, "PNG")
        return response
    return render(request, 'jpgtopng.html')

def png(request):
    if request.method == 'POST':
        convertedimage = request.FILES['img']
        type = request.POST.get('convert-type')
        if type == 'jpg':
            im = Image.open(convertedimage)
            response = HttpResponse(content_type="image/jpeg")
            im.convert('RGB').save(response, "JPEG")
            return response
        elif type == 'webp':
            im = Image.open(convertedimage)
            response = HttpResponse(content_type="image/webp")
            im.convert('RGB').save(response, "WEBP")
            return response

        return HttpResponse('not jpg')
    return render(request, 'png.html')


def docxtopdf(request):
    if request.method == 'POST':
        pythoncom.CoInitialize()  # CoInitialize çağrısı
        try:
            
            # Generate a unique ID for the file and filename
            file_id = str(uuid.uuid4())
            docx_filename = f"uploaded_{file_id}.docx"  # Örnek dosya adı
            pdf_filename = f"converted_{file_id}.pdf"

            # Get the uploaded DOCX file
            docx_file = request.FILES['docx']

            # Save the uploaded DOCX file
            with open(docx_filename, 'wb') as f:
                f.write(docx_file.read())

            # Perform the conversion
            convert(docx_filename, pdf_filename)  # Remove extension for output PDF

            # Generate the PDF content as a byte stream
            with open(pdf_filename, 'rb') as f:
                pdf_data = f.read()

            # Set the content type and response headers for PDF display
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename={pdf_filename}'

            os.remove(docx_filename)
            os.remove(pdf_filename)

            return response
        except Exception as e:
            # Handle errors here
            return HttpResponse(f"An error occurred: {e}")

    # Handle displaying the conversion form or other relevant logic
    # ...
    return render(request, 'docxtopdf.html')

from django.shortcuts import render, HttpResponse
import img2pdf
from PIL import Image
from fpdf import FPDF
import io
from docx import Document
from docx2pdf import convert
from pdf2docx import Converter
import uuid
import os
import logging
from django.shortcuts import render
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def index(request):
    
    return render(request, 'index.html')

def imgtopdf(request):
    if request.method == 'POST':
        img = request.FILES['img']
        pdf = img2pdf.convert(img)

        return HttpResponse(pdf, content_type='application/pdf')
    return render(request, 'imgtopdf.html')


def docxtopdf(request):
    if request.method == 'POST':
        try:
            
            file_id = str(uuid.uuid4())
            docx_filename = f"uploaded_{file_id}.docx" 
            pdf_filename = f"converted_{file_id}.pdf"

            docx_file = request.FILES['docx']

            with open(docx_filename, 'wb') as f:
                f.write(docx_file.read())


            with open(pdf_filename, 'rb') as f:
                pdf_data = f.read()

            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename={pdf_filename}'

            os.remove(docx_filename)
            os.remove(pdf_filename)

            return response
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    return render(request, 'docxtopdf.html')

def pdftodocx(request):
    if request.method == 'POST':
        try:
            pdf_file = request.FILES['pdf']
            
            file_id = str(uuid.uuid4())
            pdf_filename = f"uploaded_{file_id}.pdf"
            docx_filename = f"converted_{file_id}.docx"

            with open(pdf_filename, 'wb') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)

            cv = Converter(pdf_filename)
            cv.convert(docx_filename, start=0, end=None)
            cv.close()

            with open(docx_filename, 'rb') as f:
                docx_data = f.read()

            return HttpResponse(docx_data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
           

            os.remove(pdf_filename)
            os.remove(docx_filename)

            return response
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    return render(request, 'pdftodocx.html')

def txttopdf(request):
    if request.method == 'POST':
        txt_file = request.FILES['txt']
        content = txt_file.read().decode('ISO-8859-9')

        # Create a buffer to store PDF data
        pdf_buffer = BytesIO()

        # Create a canvas object with a PDF buffer
        pdf = canvas.Canvas(pdf_buffer)

        # Set font and size with a TrueType font supporting Turkish characters
        pdf.setFont("Times-Roman", 12)  # Replace "Times-Roman" with an appropriate TrueType font

        lines = content.splitlines()
        y_position = 750  # Initial y position for the first line

        for line in lines:
            # Encode the line to bytes with the same encoding used for reading the file
            encoded_line = line.encode('ISO-8859-9', errors='replace')  # Change encoding if needed
            pdf.drawString(100, y_position, encoded_line.decode('ISO-8859-9', errors='replace'))  # Draw the line
            y_position -= 15  # Move to the next line with spacing

        # Save the PDF content to the buffer
        pdf.save()

        # Create a Django HttpResponse with appropriate content type and headers
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="download.pdf"'

        # Close the buffer and return the response
        pdf_buffer.close()
        return response

    else:
        return render(request, 'txttopdf.html')

def txttodocx(request):
    if request.method == 'POST':
        txt_file = request.FILES['txt']
        content = txt_file.read().decode('utf-8')  # Assuming the text file is UTF-8 encoded

        # Generate a unique ID for the file and filename
        file_id = str(uuid.uuid4())
        docx_filename = f"converted_{file_id}.docx"

        # Create a new Document
        doc = Document()
        doc.add_paragraph(content)  # Add the text content to the document

        # Save the document to a temporary path
        doc.save(docx_filename)

        # Read the generated DOCX file and send it as a response
        with open(docx_filename, 'rb') as f:
            docx_data = f.read()

        return HttpResponse(docx_data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        

        # Clean up the file from the server after sending it
        os.remove(docx_filename)

        return response

    # Display the form to upload a text file
    return render(request, 'txttodocx.html')

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
        try:
            docx_file = request.FILES['docx']

            file_id = str(uuid.uuid4())
            docx_filename = f"uploaded_{file_id}.docx"
            pdf_filename = f"converted_{file_id}.pdf"

            # Write the uploaded DOCX file to disk
            with open(docx_filename, 'wb') as f:
                f.write(docx_file.read())

            # Convert DOCX to PDF using LibreOffice and unoconv
            cmd = f"libreoffice --headless --convert-to pdf {pdf_filename} --outdir {os.getcwd()} --nologo --norestore --nodefault"
            run(cmd, shell=True, stdout=PIPE, stderr=PIPE, check=True)
            # Read the generated PDF file and send it as a response
            with open(pdf_filename, 'rb') as f:
                pdf_data = f.read()

            # Create a Django HttpResponse and set the appropriate headers
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename={pdf_filename}'


            # Clean up temporary files
            os.remove(docx_filename)
            os.remove(pdf_filename)

            return response
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    return render(request, 'docxtopdf.html')
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

        pdf_buffer = BytesIO()

        pdf = canvas.Canvas(pdf_buffer)

        pdf.setFont("Times-Roman", 12)  

        lines = content.splitlines()
        y_position = 750  

        for line in lines:
           
            encoded_line = line.encode('ISO-8859-9', errors='replace') 
            pdf.drawString(100, y_position, encoded_line.decode('ISO-8859-9', errors='replace')) 
            y_position -= 15 

        pdf.save()

        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="download.pdf"'

        pdf_buffer.close()
        return response

    else:
        return render(request, 'txttopdf.html')

def txttodocx(request):
    if request.method == 'POST':
        txt_file = request.FILES['txt']
        content = txt_file.read().decode('utf-8') 

        
        file_id = str(uuid.uuid4())
        docx_filename = f"converted_{file_id}.docx"

      
        doc = Document()
        doc.add_paragraph(content)  

        
        doc.save(docx_filename)

      
        with open(docx_filename, 'rb') as f:
            docx_data = f.read()

        return HttpResponse(docx_data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        

       
        os.remove(docx_filename)

        return response

  
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

            with open(docx_filename, 'wb') as f:
                f.write(docx_file.read())

            
            cmd = f"libreoffice --headless --convert-to pdf {pdf_filename} --outdir {os.getcwd()} --nologo --norestore --nodefault"
            run(cmd, shell=True, stdout=PIPE, stderr=PIPE, check=True)
            
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

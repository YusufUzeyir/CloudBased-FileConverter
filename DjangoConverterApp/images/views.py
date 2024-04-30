from django.shortcuts import render, HttpResponse
import img2pdf
from PIL import Image
import fpdf
import io
from docx import Document
from docx2pdf import convert

def imgtopdf(request):
    if request.method == 'POST':
        img = request.FILES['img']
        pdf = img2pdf.convert(img)

        return HttpResponse(pdf, content_type='application/pdf')
    return render(request, 'imgtopdf.html')


def docxtopdf(request):
    if request.method == 'POST':
        docx_file = request.FILES['docx']

        # Docx dosyasını oku
        docx_content = docx_file.read()

        # Docx içeriğini PDF'ye dönüştür
        document = Document(io.BytesIO(docx_content))
        pdf_bytes = io.BytesIO()
        document.save(pdf_bytes)

        # PDF'yi HttpResponse nesnesine ekleyerek dön
        response = HttpResponse(pdf_bytes.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="converted_document.pdf"'
        return response

    return render(request, 'docxtopdf.html')

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

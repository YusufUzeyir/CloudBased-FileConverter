# File Convert

This repository contains a Python function for file extension conversion.

**Note:** This function is currently designed for use on Linux Based operating systems.

## Usage for Windows

1. **Add** `import pythoncom` to /images/views.py.
2. `docxtopdf` function should be replaced with the function given below.
3. Python Version: `3.10.11`
## Code

```python
def docxtopdf(request):
    if request.method == 'POST':
        pythoncom.CoInitialize()  
        try:
            
            file_id = str(uuid.uuid4())
            docx_filename = f"uploaded_{file_id}.docx" 
            pdf_filename = f"converted_{file_id}.pdf"

            docx_file = request.FILES['docx']

            with open(docx_filename, 'wb') as f:
                f.write(docx_file.read())

            convert(docx_filename, pdf_filename)  

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
```

### Run Locally

To run **File Converter** locally, run this command on your git bash:

Linux and macOS:

```bash
sudo git clone https://github.com/YusufUzeyir/CloudBased-FileConverter.git
```

Windows:

```bash
git clone https://github.com/YusufUzeyir/CloudBased-FileConverter.git
```
```bash
python manage.py runserver
```
### Application Images

![Ekran Görüntüsü (98)](https://github.com/YusufUzeyir/CloudBased-FileConverter/assets/92249669/9a1c54b6-cfd4-41d6-be40-cf00098c1a58)<br>
![Ekran Görüntüsü (99)](https://github.com/YusufUzeyir/CloudBased-FileConverter/assets/92249669/7cc52328-b30d-444b-897d-e2abeb100096)<br>
![Ekran Görüntüsü (100)](https://github.com/YusufUzeyir/CloudBased-FileConverter/assets/92249669/adb8311a-0007-478e-a1bf-5d5f7bf46ab2)




